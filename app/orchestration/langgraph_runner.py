from typing import Any, TypedDict

from app.models.workflow_state import WorkflowState

from langgraph.graph import END, START, StateGraph


class WorkflowGraphState(TypedDict, total=False):
    workflow: WorkflowState
    payload: Any
    result: Any
    approval_id: str
    error: str


class BaseLangGraphRunner:
    def __init__(self) -> None:
        graph = StateGraph(WorkflowGraphState)
        self.register_nodes(graph)
        self.register_edges(graph)
        self._compiled = graph.compile()

    def register_nodes(self, graph: StateGraph) -> None:
        raise NotImplementedError

    def register_edges(self, graph: StateGraph) -> None:
        raise NotImplementedError

    def invoke(self, state: WorkflowGraphState) -> WorkflowGraphState:
        return self._compiled.invoke(state)


__all__ = ["BaseLangGraphRunner", "END", "START", "StateGraph", "WorkflowGraphState"]
