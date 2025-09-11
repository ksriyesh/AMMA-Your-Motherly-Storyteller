import os

from amma.context import Context


def test_context_init() -> None:
    context = Context(model="openai/gpt-4o-mini")
    assert context.model == "openai/gpt-4o-mini"


def test_context_init_with_env_vars() -> None:
    os.environ["MODEL"] = "openai/gpt-4o-mini"
    context = Context()
    assert context.model == "openai/gpt-4o-mini"
