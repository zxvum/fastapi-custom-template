from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.requests import Request

from app.db.exceptions import DatabaseValidationError


async def database_validation_exception_handler(request: Request, exc: DatabaseValidationError) -> JSONResponse:
    error_detail = [{"loc": [exc.field or "__root__"], "msg": exc.message}]
    request_exc = RequestValidationError(errors=error_detail)
    return await request_validation_exception_handler(request, request_exc)


class ObjectDoesNotExist(Exception):
    pass
