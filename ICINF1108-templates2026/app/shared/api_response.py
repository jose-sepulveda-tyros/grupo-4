from typing import Any, Generic, TypeVar

from pydantic import BaseModel


DataT = TypeVar("DataT")


class ApiError(BaseModel):
    type: str
    details: Any | None = None


class ApiResponse(BaseModel, Generic[DataT]):
    success: bool
    statusCode: int
    message: str
    data: DataT | None = None
    error: ApiError | None = None

    @classmethod
    def success_response(
        cls,
        data: DataT,
        message: str,
        status_code: int = 200,
    ) -> "ApiResponse[DataT]":
        return cls(
            success=True,
            statusCode=status_code,
            message=message,
            data=data,
            error=None,
        )

    @classmethod
    def error_response(
        cls,
        message: str,
        status_code: int,
        error_type: str,
        details: Any | None = None,
    ) -> "ApiResponse[None]":
        return cls(
            success=False,
            statusCode=status_code,
            message=message,
            data=None,
            error=ApiError(
                type=error_type,
                details=details,
            ),
        )