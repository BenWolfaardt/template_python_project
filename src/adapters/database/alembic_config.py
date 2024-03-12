from alembic.config import Config


class AlembicConfig:
    def __init__(self, script_location: str, connection_url: str) -> None:
        self.config: Config = Config()
        self.connection_url: str = connection_url
        self.script_location: str = script_location

    def create(self) -> Config:
        self.config.set_main_option("script_location", self.script_location)
        self.config.set_main_option("sqlalchemy.url", self.connection_url)
        self.config.set_main_option("post_write_hooks", "black")
        self.config.set_section_option(
            "alembic",
            "file_template",
            "%%(year)d%%(month).2d%%(day).2d-%%(slug)s",
        )
        self.config.set_section_option("black", "type", "console_scripts")
        self.config.set_section_option("black", "entrypoint", "black")
        self.config.set_section_option("black", "options", "-l 110 REVISION_SCRIPT_FILENAME")
        self.config.set_section_option("logger_root", "level", "WARN")
        self.config.set_section_option("logger_root", "handlers", "console")
        self.config.set_section_option("logger_sqlalchemy", "level", "WARN")
        self.config.set_section_option("logger_sqlalchemy", "qualname", "sqlalchemy.engine")
        self.config.set_section_option("logger_alembic", "level", "INFO")
        self.config.set_section_option("logger_alembic", "qualname", "alembic")
        self.config.set_section_option("handler_console", "class", "StreamHandler")
        self.config.set_section_option("handler_console", "args", "(sys.stderr,)")
        self.config.set_section_option("handler_console", "level", "NOTSET")
        self.config.set_section_option("handler_console", "formatter", "generic")
        # self.config.set_section_option("formatter_generic", "format", "%(levelname)-5.5s [%(name)s] %(message)s")
        # self.config.set_section_option("formatter_generic", "datefmt", "%H:%M:%S")

        return self.config
