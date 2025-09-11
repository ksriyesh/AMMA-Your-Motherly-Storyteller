"""Define the configurable parameters for the agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated


@dataclass(kw_only=True)
class Context:
    """Configuration context for the AMMA agent."""

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="openai/gpt-3.5-turbo",
        metadata={
            "description": "The language model to use. Format: provider/model-name."
        },
    )

    def __post_init__(self) -> None:
        """Load configuration from environment variables."""
        for f in fields(self):
            if not f.init:
                continue
            if getattr(self, f.name) == f.default:
                setattr(self, f.name, os.environ.get(f.name.upper(), f.default))
