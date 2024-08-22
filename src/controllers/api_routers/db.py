from uuid import UUID, uuid4

from fastapi import APIRouter, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.adapters.logger import Logger
from src.core.interactors.api_db_crud import APICRUD
from src.core.models.api_routers.db import (
    CreateRequest,
    CreateResponse,
    DeleteRequest,
    DeleteResponse,
    ReadAllRequest,
    ReadAllResponse,
    ReadRequest,
    ReadResponse,
    UpdateRequest,
    UpdateResponse,
)
from src.core.models.exceptions import DataAlreadyExists, DataEmpty, DataIDNotDeleted, DataIDNotFound


prefix = "/db"
router = APIRouter(tags=["DB"], prefix=prefix)


def parse_init_args_to_router_db(api_crud: APICRUD, logger: Logger) -> None:  # C901: too complex
    exceptions = logger.Exceptions(logger)

    @router.post("/", response_model=CreateResponse)
    async def create(
        request: CreateRequest,
        request_id: str | None = Query(None, description="Custom request ID"),
    ) -> JSONResponse:
        request_id = request_id or str(uuid4())

        try:
            response_data = api_crud.create(request, request_id)
            return JSONResponse(jsonable_encoder(response_data))

        # TODO: figure out how excepts propogate up the call stack from the sql_store level
        except DataAlreadyExists as data_already_exists_exception:
            msg = str(data_already_exists_exception)
            logger.warning(msg)
            return JSONResponse(status_code=404, content={"error_message": msg})

        except Exception as e:
            exceptions.log_api_exception_and_raise_http_exception(
                f"Error creating {request.data.id}", e, request_id, 500
            )

    @router.get("/", response_model=ReadResponse)
    async def read(
        id: UUID = Query(..., description="ID"),
        request_id: str | None = Query(None, description="Custom request ID"),
    ) -> JSONResponse:
        request_id = request_id or str(uuid4())

        try:
            request = ReadRequest(id=id)
            response_data = api_crud.read(request, request_id)
            return JSONResponse(jsonable_encoder(response_data))

        except DataIDNotFound as data_id_not_found_exception:
            msg = str(data_id_not_found_exception)
            logger.warning(msg)
            return JSONResponse(status_code=404, content={"error_message": msg})

        except Exception as e:
            exceptions.log_api_exception_and_raise_http_exception(f"Error creating {id}", e, request_id, 500)

    @router.get("/all", response_model=ReadAllResponse)
    async def read_all(
        id: UUID | None = Query(None, description="Data's ID"),
        request_id: str | None = Query(None, description="Custom request ID"),
    ) -> JSONResponse:
        request_id = request_id or str(uuid4())

        try:
            request = ReadAllRequest(id=id)
            response_data = api_crud.read_all(request, request_id)
            return JSONResponse(jsonable_encoder(response_data))

        except DataEmpty as data_empty_exception:
            msg = str(data_empty_exception)
            logger.warning(msg)
            return JSONResponse(status_code=404, content={"error_message": msg})

        except Exception as e:
            exceptions.log_api_exception_and_raise_http_exception(
                f"Error reading all {id}", e, request_id, 500
            )

    # TODO improve patch logic
    @router.patch("/", response_model=UpdateResponse)
    async def update(
        request: UpdateRequest,
        request_id: str | None = Query(None, description="Custom request ID"),
    ) -> JSONResponse:
        request_id = request_id or str(uuid4())

        try:
            response_data = api_crud.update(request, request_id)
            return JSONResponse(jsonable_encoder(response_data))

        except DataIDNotFound as data_id_not_found_exception:
            msg = str(data_id_not_found_exception)
            logger.warning(msg)
            return JSONResponse(status_code=404, content={"error_message": msg})

        except Exception as e:
            exceptions.log_api_exception_and_raise_http_exception(
                f"Error updating all {request.data.id}", e, request_id, 500
            )

    @router.delete("/", response_model=DeleteResponse)
    async def delete(
        id: UUID | None = Query(None, description="Data's ID"),
        request_id: str | None = Query(None, description="Custom request ID"),
    ) -> JSONResponse:
        request_id = request_id or str(uuid4())

        try:
            request = DeleteRequest(id=id)
            response_data = api_crud.delete(
                request,
                request_id,
            )
            return JSONResponse(jsonable_encoder(response_data))

        except DataIDNotFound as data_id_not_found_exception:
            msg = str(data_id_not_found_exception)
            logger.warning(msg)
            return JSONResponse(status_code=404, content={"error_message": msg})

        except DataIDNotDeleted as data_id_not_deleted_exception:
            msg = str(data_id_not_deleted_exception)
            logger.exception(msg)
            return JSONResponse(status_code=500, content={"error_message": msg})

        except Exception as e:
            exceptions.log_api_exception_and_raise_http_exception(
                f"Error deleting all {id}", e, request_id, 500
            )
