from rc_agent import RCAgent
from config import Config

if __name__ == "__main__":

    config = Config()

    rc_agent = RCAgent(config)
    rc_agent.run()