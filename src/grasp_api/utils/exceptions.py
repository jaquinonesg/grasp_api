from typing import Any

from fastapi import HTTPException, status


def raise_not_found(data: Any) -> None:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Example with id <{data}> not found!",
    )
