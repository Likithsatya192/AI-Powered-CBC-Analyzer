"""LangGraph pipeline entry (starter stub)."""
from typing import Optional

from .graph_state import GraphState


def create_pipeline(state: Optional[GraphState] = None):
    """Return a minimal pipeline representation for local development.

    This is a placeholder where the LangGraph pipeline wiring will be implemented.
    """
    state = state or GraphState()
    return {"pipeline": "stub", "state": state.dict()}


if __name__ == "__main__":
    print(create_pipeline())
