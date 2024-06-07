from fastapi import APIRouter, Depends, status as http_status

from grasp_api.api.v1.provision.base.serializers import ExampleRM
from grasp_api.crud.example import ExampleCRUD, get_example_crud
from grasp_api.utils.errors import NotFoundError
from grasp_api.utils.exceptions import raise_not_found

router = APIRouter()


@router.get("/{example_id}", status_code=http_status.HTTP_200_OK)
async def get_example_by_id(
    example_id: str, examples: ExampleCRUD = Depends(get_example_crud)
):
    try:
        return await examples.get(example_id=example_id)
    except NotFoundError:
        raise_not_found(example_id)


@router.post("/example", status_code=http_status.HTTP_201_CREATED)
async def create_example(
    data: ExampleRM, examples: ExampleCRUD = Depends(get_example_crud)
):
    return await examples.create(data=data)


@router.delete("/{example_id}", status_code=http_status.HTTP_200_OK)
async def delete_example_by_id(
    example_id: str, examples: ExampleCRUD = Depends(get_example_crud)
):
    try:
        return {
            "status": await examples.delete(example_id=example_id),
            "message": "The example has been deleted!",
        }
    except NotFoundError:
        raise_not_found(example_id)


@router.patch("/{example_id}", status_code=http_status.HTTP_200_OK)
async def patch_example_by_id(
    example_id: str,
    data: ExampleRM,
    examples: ExampleCRUD = Depends(get_example_crud),
):
    try:
        return await examples.patch(example_id=example_id, data=data)
    except NotFoundError:
        raise_not_found(example_id)
