from fastapi import APIRouter, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

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
from src.core.ports.logging import Logging


prefix = "/db"
router = APIRouter(tags=["DB"], prefix=prefix)


def parse_init_args_to_router_db(api_crud: APICRUD, logger: Logging) -> None:  # C901: too complex
    @router.post("/")
    async def create(request: CreateRequest) -> JSONResponse:
        try:
            response_data: CreateResponse = api_crud.create(request)
            return JSONResponse(jsonable_encoder(response_data))

        except Exception as e:
            msg = f"Error creating: {e!s}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg) from e

    @router.get("/")
    async def read(id: str = Query(..., description="ID"), request_id: str | None = None) -> JSONResponse:
        try:
            request = ReadRequest(id=id, request_id=request_id)
            response_data: ReadResponse = api_crud.read(request)
            return JSONResponse(jsonable_encoder(response_data))

        except Exception as e:
            msg = f"Error reading: {e!s}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg) from e

    @router.get("/all")
    async def read_all(request_id: str | None = None) -> JSONResponse:
        # TODO have better handling if no data
        try:
            request = ReadAllRequest(request_id=request_id)
            response_data: ReadAllResponse = api_crud.read_all(request)
            return JSONResponse(jsonable_encoder(response_data))

        except Exception as e:
            msg = f"Error reading all: {e!s}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg) from e

    # TODO improve patch logic
    @router.patch("/")
    async def update(request: UpdateRequest) -> JSONResponse:
        try:
            request = UpdateRequest(data=request.data, request_id=request.request_id)
            response_data: UpdateResponse = api_crud.update(request)
            return JSONResponse(jsonable_encoder(response_data))

        except Exception as e:
            msg = f"Error updating: {e!s}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg) from e

    # TODO debug why its not deleting
    @router.delete("/")
    async def delete(id: str, request_id: str | None = None) -> JSONResponse:
        try:
            request = DeleteRequest(id=id, request_id=request_id)
            response_data: DeleteResponse = api_crud.delete(request)
            # TODO think about this?
            response_dict = response_data.model_dump()
            response_dict["success"] = True
            return JSONResponse(response_dict)

        except Exception as e:
            msg = f"Error deleting: {e!s}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg) from e
