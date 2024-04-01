from fastapi import FastAPI


class API:
    def __init__(self) -> None:
        self.server: FastAPI = self.make_http_controller()

    def make_http_controller(self) -> FastAPI:
        app = FastAPI(
            title="API",
            description="Template Python OpenAPI specification.",
            contact={
                "name": "Template Python",
                "url": "https://example.com/contact",
                "email": "support@example.com",
            },
            license_info={
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
            },
            version="1.0.0",
        )

        return app
