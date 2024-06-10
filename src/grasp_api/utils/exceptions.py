from typing import Any

from fastapi import HTTPException, status


def raise_not_found(data: Any) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Example with id <{data}> not found!",
    )


def raise_conflict(data: Any) -> None:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Integrity error. {data} primary key might be duplicated",
    )


def raise_bad_request_get(data: Any) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Error in query parameters: {data}",
    )


def raise_unprocessable_content(data: Any) -> None:
    raise HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail=f"Error in query parameters: {data}",
    )


def raise_bad_request_post(data: Any) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Error decoding the message: {data}",
    )


def raise_exception_with_ack() -> None:
    raise HTTPException(
        status_code=200, detail="Message received but processing failed"
    )
