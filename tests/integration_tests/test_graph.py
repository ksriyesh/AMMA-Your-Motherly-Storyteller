import pytest
from langsmith import unit

from amma import graph
from amma.context import Context


@pytest.mark.asyncio
@unit
async def test_amma_conversation() -> None:
    res = await graph.ainvoke(
        {"messages": [("user", "Hi, I'm Emma and I'd like a fairy tale story")]},  # type: ignore
        context=Context(),
    )

    # Should have some response from AMMA
    assert len(res["messages"]) > 0
