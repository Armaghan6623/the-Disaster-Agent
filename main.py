from the_disaster_response_agent.agent import DisasterResponseAgent
from the_disaster_response_agent.utils import settings


def main():
    print(f"Hello from the-disaster-response-agent v{settings.model_name}")
    agent = DisasterResponseAgent(settings.model_name)
    return agent


if __name__ == "__main__":
    main()
