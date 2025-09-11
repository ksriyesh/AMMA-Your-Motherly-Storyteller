"""Define the state structures for AMMA."""

from __future__ import annotations

from typing import Optional, Sequence

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep
from pydantic import BaseModel, Field
from typing_extensions import Annotated


class InputState(BaseModel):
    """Defines the input state for AMMA, representing a narrower interface to the outside world."""

    messages: Annotated[Sequence[AnyMessage], add_messages] = Field(
        default_factory=list,
        description="Messages tracking the primary execution state of AMMA."
    )


class State(InputState):
    """Represents the complete state of AMMA, extending InputState with story-specific attributes."""

    is_last_step: IsLastStep = Field(
        default=False,
        description="Indicates whether the current step is the last one before the graph raises an error."
    )

    child_name: Optional[str] = Field(
        default=None,
        description="The name of the child for whom the story is being created."
    )

    story_theme: Optional[str] = Field(
        default=None,
        description="The theme or type of story the child wants to hear."
    )

    generated_story: Optional[str] = Field(
        default=None,
        description="The final generated bedtime story for the child."
    )

    suggested_revisions: Optional[str] = Field(
        default=None,
        description="User's suggestions for revising the current story."
    )

    current_story: Optional[str] = Field(
        default=None,
        description="The story currently being evaluated."
    )

    evaluation_result: Optional[str] = Field(
        default=None,
        description="Result of story evaluation: 'approved' or 'needs_revision'."
    )

    evaluation_feedback: Optional[str] = Field(
        default=None,
        description="Detailed feedback from story evaluation."
    )

    revision_count: int = Field(
        default=0,
        description="Number of revision cycles attempted."
    )
