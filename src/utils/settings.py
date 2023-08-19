import argparse

from enum import Enum

from envyaml import EnvYAML


class Environment(str, Enum):
    LOCAL = "local"
    TEST = "test"
    PRODUCTION = "production"


class InvalidEnvironmentError(argparse.ArgumentTypeError):
    def __init__(self, value: str, choices: list[str]):
        self.value = value
        self.choices = choices
        super().__init__(
            f"You have entered an incorrect choice: {value}. Your options are \"{', '.join(choices)}\""
        )


def parse_env_arg(value: str) -> str:
    if value not in [e.value for e in Environment]:
        raise InvalidEnvironmentError(value, [e.value for e in Environment])
    return Environment(value)


def load_settings() -> "Settings":
    parser = argparse.ArgumentParser(description="App environment")
    parser.add_argument(
        "--env",
        type=parse_env_arg,
        help="Configuration environment for the app",
        metavar="ENV",
    )
    cli_args = parser.parse_args()

    yaml_config = EnvYAML(f"configs/{cli_args.env.value}.yml", strict=False)
    return Settings(yaml_config)


class Settings:
    def __init__(self, yaml_config: EnvYAML) -> None:
        self.config = yaml_config

    def section_1(self) -> dict:
        return dict(self.config["section_1"])
