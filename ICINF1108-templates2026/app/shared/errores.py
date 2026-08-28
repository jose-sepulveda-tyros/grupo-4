from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.shared.api_response import ApiResponse


MENSAJES_HTTP = {
    400: "Solicitud incorrecta",
    404: "Recurso no encontrado",
    405: "Método no permitido",
    409: "Conflicto con el estado actual del recurso",
    422: "Los datos enviados no son válidos",
    500: "Ocurrió un error interno del servidor",
}


def obtener_tipo_error(status_code: int) -> str:
    try:
        return HTTPStatus(status_code).name.lower()
    except ValueError:
        return "http_error"


def crear_respuesta_error(
    status_code: int,
    message: str,
    error_type: str,
    details: object | None = None,
) -> JSONResponse:
    respuesta = ApiResponse[None].error_response(
        message=message,
        status_code=status_code,
        error_type=error_type,
        details=details,
    )

    return JSONResponse(
        status_code=status_code,
        content=respuesta.model_dump(mode="json"),
    )


async def manejar_error_http(
    _request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    detail = exc.detail

    if isinstance(detail, str):
        message = detail
        details = None
    else:
        message = MENSAJES_HTTP.get(
            exc.status_code,
            "Error en la solicitud",
        )
        details = jsonable_encoder(detail)

    return crear_respuesta_error(
        status_code=exc.status_code,
        message=message,
        error_type=obtener_tipo_error(exc.status_code),
        details=details,
    )


async def manejar_error_validacion(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return crear_respuesta_error(
        status_code=422,
        message=MENSAJES_HTTP[422],
        error_type="validation_error",
        details=jsonable_encoder(exc.errors()),
    )


async def manejar_error_inesperado(
    _request: Request,
    _exc: Exception,
) -> JSONResponse:
    return crear_respuesta_error(
        status_code=500,
        message=MENSAJES_HTTP[500],
        error_type="internal_server_error",
    )


def registrar_manejadores(app: FastAPI) -> None:
    app.add_exception_handler(
        StarletteHTTPException,
        manejar_error_http,
    )
    app.add_exception_handler(
        RequestValidationError,
        manejar_error_validacion,
    )
    app.add_exception_handler(
        Exception,
        manejar_error_inesperado,
    )