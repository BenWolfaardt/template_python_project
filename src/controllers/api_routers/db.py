import traceback

from fastapi import APIRouter, HTTPException, Query

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
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


prefix = "/db"
router = APIRouter(tags=["DB"], prefix=prefix)


def parse_init_args_to_router_db(  # noqa C901: too complex
    api_crud: APICRUD, logger: Logging
) -> None:
    @router.post("/")
    async def create(request: CreateRequest) -> JSONResponse:
        try:
            response_data: CreateResponse = api_crud.create(request)
            return JSONResponse(jsonable_encoder(response_data))

        except Exception as e:
            msg = f"Error creating: {str(e)}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg)

    @router.get("/")
    async def read(id: str = Query(..., description="ID")) -> JSONResponse:
        # TODO autogenerate a request_id
        request_id = ""

        try:
            request = ReadRequest(id=id, request_id=request_id)
            response_data: ReadResponse = api_crud.read(request)
            return JSONResponse(jsonable_encoder(response_data))

        except Exception as e:
            msg = f"Error reading: {str(e)}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg)

    @router.get("/all")
    async def read_all() -> JSONResponse:
        # TODO autogenerate a request_id
        request_id = ""

        # TODO have better handling if no data
        try:
            request = ReadAllRequest(request_id=request_id)
            response_data: ReadAllResponse = api_crud.read_all(request)
            return JSONResponse(jsonable_encoder(response_data))

        except Exception as e:
            # msg = f"Error reading all: {str(e)}"
            traceback_str = traceback.format_exc()
            msg = f"Error reading all: {e}\nTraceback: {traceback_str}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg)

    # TODO improve patch logic
    @router.patch("/")
    async def update(request: UpdateRequest) -> JSONResponse:
        try:
            response_data: UpdateResponse = api_crud.update(request)
            return JSONResponse(jsonable_encoder(response_data))

        except Exception as e:
            msg = f"Error updating: {str(e)}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg)

    @router.delete("/")
    async def delete(request: DeleteRequest) -> JSONResponse:
        try:
            response_data: DeleteResponse = api_crud.delete(request)
            # TODO think about this?
            response_dict = response_data.model_dump()
            response_dict["success"] = True
            return JSONResponse(response_dict)

        except Exception as e:
            msg = f"Error deleting: {str(e)}"
            logger.error(msg)
            raise HTTPException(status_code=500, detail=msg)


# TODO add exception handling
# @app.exception_handler(Error)
# async def error_handler(_: Request, e: Error):
#     status_code = 400
#     if e.error_codes:
#         if e.error_codes[0] == ErrorCode.unknown_access_token:
#             status_code = 401
#         if e.error_codes[0] == ErrorCode.illegal_access:
#             status_code = 403
#         if e.error_codes[0] == ErrorCode.user_not_found:
#             status_code = 404
#         if e.error_codes[0] == ErrorCode.system_error:
#             status_code = 500

#     return JSONResponse(
#         status_code=status_code,
#         content={"errors": f"{e.error_codes}"},
#     )
