#!/usr/bin/env python3
"""Simple CLI interface for AMMA - Bedtime Story Agent
Pure conversation interface - just chat with AMMA!

Before submitting the assignment, describe here in a few sentences what you would have built next if you spent 2 more hours on this project:
 i would properly integrate a voice module maybe eleven labs in it as well look around for any mcps to fetch stories to gegnerate classic stories 
"""

import asyncio
import sys
from typing import Any, Dict

from src.amma.context import Context
from src.amma.graph import graph
from src.amma.state import State


class AMMACLI:
    """Simple command-line interface for AMMA agent."""
    
    def __init__(self):
        self.context = Context()
        self.state_data: Dict[str, Any] = {
            "messages": [],
            "is_last_step": False,
            "child_name": None,
            "story_theme": None,
            "generated_story": None,
            "suggested_revisions": None,
            "current_story": None,
            "evaluation_result": None,
            "evaluation_feedback": None,
            "revision_count": 0
        }
    
    async def process_message(self, user_input: str) -> str:
        """Process user message through AMMA agent."""
        try:
            # Add user message to state
            from langchain_core.messages import HumanMessage
            self.state_data["messages"].append(HumanMessage(content=user_input))
            
            # Create state object
            current_state = State(**self.state_data)
            
            # Run the agent
            result = await graph.ainvoke(current_state, config={"context": self.context})
            
            # Update our state data with the result
            self.state_data.update(result)
            
            # Get the last AI message
            messages = result.get("messages", [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, 'content'):
                    return last_message.content
            
            return "I'm processing your request..."
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def run(self):
        """Main conversation loop."""
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Process the message
                response = await self.process_message(user_input)
                
                # Print response with typing effect
                for char in response:
                    await asyncio.sleep(0.02)
                
            except KeyboardInterrupt:
                break
            except Exception:
                pass


async def main():
    """Main entry point."""
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    
    # Check for API key
    import os
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit(1)
    
    # Run the CLI
    try:
        cli = AMMACLI()
        await cli.run()
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
