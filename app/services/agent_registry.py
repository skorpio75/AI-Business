from app.models.agent_contract import AgentContract, AgentRegistry, DEFAULT_AGENT_REGISTRY


class AgentRegistryService:
    def __init__(self, registry: AgentRegistry | None = None) -> None:
        self.registry = registry or DEFAULT_AGENT_REGISTRY

    def list_agents(self) -> list[AgentContract]:
        return self.registry.agents

    def get_agent(self, agent_id: str) -> AgentContract | None:
        for agent in self.registry.agents:
            if agent.agent_id == agent_id:
                return agent
        return None
