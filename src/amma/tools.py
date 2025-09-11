"""Tools for AMMA - the conversational bedtime story agent."""

from typing import Any, Callable, List, Optional

def update_story_preferences(
    child_name: Optional[str] = None, 
    story_theme: Optional[str] = None,
    suggested_revisions: Optional[str] = None
) -> str:
    """Update the story preferences and revision suggestions for the child.
    
    Args:
        child_name: The name of the child for whom the story is being created
        story_theme: The theme or type of story the child wants to hear
        suggested_revisions: Suggestions for revising the current story
    
    Returns:
        Success message
    """
    # Return a simple success message
    # State updates will be handled in the custom tool handler
    updates = []
    if child_name is not None:
        updates.append(f"name: {child_name}")
    if story_theme is not None:
        updates.append(f"theme: {story_theme}")
    if suggested_revisions is not None:
        updates.append(f"revisions: {suggested_revisions}")
    
    return f"Successfully updated - {', '.join(updates)}"


def request_new_story(
    child_name: Optional[str] = None,
    story_theme: Optional[str] = None
) -> str:
    """Request a completely new story, clearing previous story and revisions.
    
    Args:
        child_name: The name of the child for whom the story is being created
        story_theme: The theme or type of story the child wants to hear
    
    Returns:
        Success message
    """
    updates = []
    if child_name is not None:
        updates.append(f"name: {child_name}")
    if story_theme is not None:
        updates.append(f"theme: {story_theme}")
    
    return f"Starting new story - {', '.join(updates) if updates else 'with current preferences'}"


TOOLS: List[Callable[..., Any]] = [update_story_preferences, request_new_story]
