from the_disaster_response_agent.agent import DisasterResponseAgent


def test_agent_initialization():
    agent = DisasterResponseAgent()
    assert agent.model_name is not None
    assert agent.classifier is not None