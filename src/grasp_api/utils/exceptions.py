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


def raise_binascii(data: Any) -> None:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Error decoding the message: {data}",
    )


def raise_exception_with_200() -> None:
    raise HTTPException(
        status_code=200, detail="Message received but processing failed"
    )
