"""AMMA - Conversational bedtime story agent with improved multi-agent architecture."""

from datetime import UTC, datetime
from typing import Any, Dict, List, Literal, cast

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

from src.amma.context import Context
from src.amma.prompts import AMMA_PROMPT, STORY_CREATOR_PROMPT, STORY_EDITOR_PROMPT
from src.amma.state import InputState, State
from src.amma.tools import TOOLS, update_story_preferences
from src.amma.utils import load_chat_model

# ============================================================================
# AGENT NODES
# ============================================================================

async def amma(state: State, runtime: Runtime[Context]) -> Dict[str, List[AIMessage]]:
    """AMMA - conversational agent that collects preferences and handles conversation."""
    context = runtime.context if runtime.context else Context()
    model = load_chat_model(context.model).bind_tools(TOOLS)

    system_message = AMMA_PROMPT.format(
        child_name=state.child_name or "None",
        story_theme=state.story_theme or "None",
        generated_story=state.generated_story or "None",
        suggested_revisions=state.suggested_revisions or "None",
        system_time=datetime.now(tz=UTC).isoformat()
    )

    response = cast(AIMessage, await model.ainvoke([
        {"role": "system", "content": system_message}, 
        *state.messages
    ]))

    # Handle last step gracefully
    if state.is_last_step and response.tool_calls:
        model_without_tools = load_chat_model(context.model)
        response = cast(AIMessage, await model_without_tools.ainvoke([
            {"role": "system", "content": system_message + "\n\nRespond naturally without using tools."},
            *state.messages
        ]))

    return {"messages": [response]}


async def story_creator(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """Creates personalized bedtime stories or revisions based on state."""
    context = runtime.context if runtime.context else Context()
    model = load_chat_model(context.model)
    
    system_message = STORY_CREATOR_PROMPT.format(
        child_name=state.child_name or "little one",
        child_age="5-10 years old",
        story_theme=state.story_theme or "magical adventure",
        generated_story=state.generated_story or "",
        suggested_revisions=state.suggested_revisions or "",
        system_time=datetime.now(tz=UTC).isoformat()
    )
    
    # Include editor feedback if available
    messages = [{"role": "system", "content": system_message}]
    if state.messages:
        for msg in state.messages[-3:]:
            if hasattr(msg, 'content') and "NEEDS_REVISION" in str(msg.content):
                messages.append({"role": "user", "content": f"Revise based on: {msg.content}"})
                break
    
    response = cast(AIMessage, await model.ainvoke(messages))
    return {
        "messages": [response],
        "current_story": response.content  # Store current story for evaluation
    }


async def story_evaluator(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """Evaluates story quality and returns structured decision."""
    context = runtime.context if runtime.context else Context()
    model = load_chat_model(context.model)
    
    # Get the story to evaluate
    current_story = state.current_story or ""
    if not current_story and state.messages:
        current_story = state.messages[-1].content
    
    system_message = STORY_EDITOR_PROMPT.format(
        story_theme=state.story_theme or "magical adventure",
        generated_story=current_story,
        suggested_revisions=state.suggested_revisions or "None",
        system_time=datetime.now(tz=UTC).isoformat()
    )
    
    response = cast(AIMessage, await model.ainvoke([
        {"role": "system", "content": system_message}
    ]))
    
    # Determine if approved based on response
    is_approved = "approved" in response.content.lower()
    
    return {
        # Don't add evaluation messages to conversation history - keep them internal
        "evaluation_result": "approved" if is_approved else "needs_revision",
        "current_story": current_story,  # Pass story along
        "evaluation_feedback": response.content
    }


async def story_presenter(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """Presents the final approved story to the user."""
    current_story = state.current_story or ""
    
    # Simple, clean presentation of just the story
    final_message = AIMessage(content=current_story)
    
    return {
        "messages": [final_message],
        "generated_story": current_story,
        "suggested_revisions": None,  # Clear revisions after successful presentation
        "evaluation_result": None,  # Clear evaluation result
        "evaluation_feedback": None,  # Clear evaluation feedback
        "current_story": None,  # Clear current story
        "revision_count": 0  # Reset revision count for next story
    }


async def revision_handler(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """Handles revision feedback and prepares for next iteration."""
    # Clear evaluation results for next iteration and increment revision count
    return {
        "revision_count": state.revision_count + 1,
        "evaluation_result": None,
        "current_story": None,  # Clear current story so creator generates new one
        # Keep suggested_revisions for the story_creator to see
    }


async def handle_tools(state: State, runtime: Runtime[Context]) -> Dict[str, Any]:
    """Processes tool calls and updates state."""
    last_message = state.messages[-1]
    
    if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
        return {"messages": []}
    
    tool_messages = []
    state_updates = {}
    
    for tool_call in last_message.tool_calls:
        if tool_call['name'] == 'update_story_preferences':
            # Execute tool
            result = update_story_preferences(**tool_call['args'])
            
            # Update state
            args = tool_call['args']
            if args.get('child_name'):
                state_updates['child_name'] = args['child_name']
            if args.get('story_theme'):
                state_updates['story_theme'] = args['story_theme']
            if args.get('suggested_revisions'):
                state_updates['suggested_revisions'] = args['suggested_revisions']
            
            # Create tool message
            tool_messages.append(ToolMessage(
                content=result,
                tool_call_id=tool_call['id']
            ))
            
        elif tool_call['name'] == 'request_new_story':
            # Execute tool
            from src.amma.tools import request_new_story
            result = request_new_story(**tool_call['args'])
            
            # Update state - clear existing story and revisions for fresh start
            args = tool_call['args']
            if args.get('child_name'):
                state_updates['child_name'] = args['child_name']
            if args.get('story_theme'):
                state_updates['story_theme'] = args['story_theme']
            
            # Clear previous story and revisions - full reset
            state_updates['generated_story'] = None
            state_updates['suggested_revisions'] = None
            state_updates['current_story'] = None
            state_updates['evaluation_result'] = None
            state_updates['evaluation_feedback'] = None
            state_updates['revision_count'] = 0
            
            # Create tool message
            tool_messages.append(ToolMessage(
                content=result,
                tool_call_id=tool_call['id']
            ))
    
    return {"messages": tool_messages, **state_updates}


# ============================================================================
# ROUTING LOGIC
# ============================================================================

def route_from_amma(state: State) -> Literal["__end__", "tools", "story_creator"]:
    """Routes from AMMA based on output and conversation context."""
    last_message = state.messages[-1]
    
    if not isinstance(last_message, AIMessage):
        raise ValueError(f"Expected AIMessage, got {type(last_message).__name__}")
    
    # Tool calls → execute tools
    if last_message.tool_calls:
        return "tools"

    # Get user's last message for context analysis
    user_message = None
    for msg in reversed(state.messages[:-1]):
        if hasattr(msg, 'content') and msg.content and not hasattr(msg, 'tool_calls'):
            user_message = msg.content.lower()
            break
    
    # Let AMMA naturally understand when conversations should end
    # based on context and flow, rather than enforcing specific phrases
    
    # Priority routing based on state:
    
    # 1. If we have suggested revisions, create revised story
    if state.suggested_revisions and state.generated_story:
        return "story_creator"
    
    # 2. If we have preferences but no story yet, create new story
    if (state.child_name or state.story_theme) and not state.generated_story:
        return "story_creator"
    
    # 3. Check if user is indicating they want to end (natural bedtime cues)
    if user_message:
        natural_endings = ["good night", "goodnight", "bye", "goodbye", "sleep", "tired", "bedtime"]
        if any(ending in user_message for ending in natural_endings):
            # User wants to end - let AMMA respond with a gentle goodbye
            return "__end__"
    
    # 4. Check if AMMA is indicating conversation should end
    # Look for natural ending cues in AMMA's response  
    amma_response = last_message.content.lower() if last_message.content else ""
    ending_indicators = ["sweet dreams", "sleep well", "goodnight", "time for bed", "close your eyes"]
    if any(indicator in amma_response for indicator in ending_indicators):
        return "__end__"
    
    # Default: continue conversation (wait for user input)
    return "__end__"


def route_from_evaluator(state: State) -> Literal["story_presenter", "revision_handler"]:
    """Routes based on story evaluation result."""
    evaluation_result = state.evaluation_result or 'needs_revision'
    revision_count = state.revision_count
    
    # If approved or max revisions reached, present the story
    if evaluation_result == "approved" or revision_count >= 3:
        return "story_presenter"
    
    # Otherwise, handle revision
    return "revision_handler"


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

# Build the graph
builder = StateGraph(State, input_schema=InputState, context_schema=Context)

# Add nodes
builder.add_node("amma", amma)
builder.add_node("tools", handle_tools)
builder.add_node("story_creator", story_creator)
builder.add_node("story_evaluator", story_evaluator)
builder.add_node("story_presenter", story_presenter)
builder.add_node("revision_handler", revision_handler)

# Add edges
builder.add_edge("__start__", "amma")
builder.add_edge("tools", "amma")
builder.add_edge("story_creator", "story_evaluator")
builder.add_edge("revision_handler", "story_creator")  # Revision loop
builder.add_edge("story_presenter", "__end__")

# Add conditional edges
builder.add_conditional_edges("amma", route_from_amma)
builder.add_conditional_edges("story_evaluator", route_from_evaluator)

# Compile
graph = builder.compile(name="AMMA - Bedtime Story Agent")