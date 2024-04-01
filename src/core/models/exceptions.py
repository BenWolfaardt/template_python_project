from uuid import UUID


class DataAlreadyExists(Exception):
    def __init__(self, id: UUID) -> None:
        self.id = id
        super().__init__(f"Data with ID '{id}' already exists.")


class DataIDNotFound(Exception):
    def __init__(self, id: UUID) -> None:
        self.id = id
        super().__init__(f"Data with ID '{id}' not found.")


class DataEmpty(Exception):
    def __init__(self) -> None:
        super().__init__("No data found.")
