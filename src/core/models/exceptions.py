from uuid import UUID


class DataAlreadyExists(RuntimeError):
    def __init__(self, id: UUID) -> None:
        self.id = id


class DataIDNotFound(RuntimeError):
    def __init__(self, id: UUID) -> None:
        self.id = id


class DataEmpty(RuntimeError):
    def __init__(self) -> None:
        pass
        # TODO figure out what to put here
        # logging.exception("Empty DB")
