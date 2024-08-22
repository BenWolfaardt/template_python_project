from uuid import UUID


class DataAlreadyExists(Exception):
    def __init__(self, id: UUID) -> None:
        self.id = id
        super().__init__(f"Data with ID '{id}' already exists.")


class DataIDNotFound(Exception):
    def __init__(self, id: UUID) -> None:
        self.id = id
        super().__init__(f"Data with ID '{id}' not found.")


class DataIDNotDeleted(Exception):
    def __init__(self, id: UUID) -> None:
        self.id = id
        super().__init__(f"Data with ID {id}' not deleted.")


class DataEmpty(Exception):
    def __init__(
        self,
        id: UUID | None = None,
    ) -> None:
        super().__init__("No data found.")
        self.id = id

    def __str__(self) -> str:
        msg = super().__str__()
        response = ""

        if self.id is not None:
            response += f"{msg} for id '{self.id}'."

        return response if response else msg
