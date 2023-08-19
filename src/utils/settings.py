import argparse
import sys

from enum import Enum

from envyaml import EnvYAML


class Environment(str, Enum):
    LOCAL = "local"
    TEST = "test"
    PRODUCTION = "production"


def parse_env_arg() -> Environment:
    parser = argparse.ArgumentParser(description="App environment")
    parser.add_argument(
        "environment",
        metavar="env",
        type=Environment,
        help="Configuration environment for the app",
        choices=Environment.__members__.values(),
    )
    cli_args = parser.parse_args()
    environment: Environment = cli_args.environment
    if environment not in Environment.__members__:
        print(f"Environment: {environment} does not exist")
        sys.exit(1)
    return environment


def load_settings() -> "Settings":
    yaml_config = EnvYAML(f"configs/{parse_env_arg().value}.yml", strict=False)
    return Settings(yaml_config)


class Settings:
    def __init__(self, yaml_config: EnvYAML):
        self.config = yaml_config

    def get_section_1(self) -> dict:
        settings = self.config["section_1"]
        return {
            "setting_1": settings["setting_1"],
        }
