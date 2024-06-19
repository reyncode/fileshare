from typing import Any

from fastapi import APIRouter, HTTPException

from app.crud.file import file_crud
from app.api.dependencies import CurrentUser, SessionDep
from app.schemas.file import FileCreate, FileUpdate, FilePublic, FilesPublic
from app.schemas.security import Message
from app.schemas.utils import to_pydantic

router = APIRouter()

@router.post("/", response_model=FilePublic)
def create_file(
    *, session: SessionDep, current_user: CurrentUser, file_in: FileCreate
) -> Any:
    """
    Create a new file database object with name owned by the current user.
    """
    file = file_crud.read_file_by_name(session=session, name=file_in.name, owner_id=current_user.id)

    if file:
        file_in.name = file_crud.generate_unique_name(session=session, name=file_in.name, owner_id=current_user.id)

    file = file_crud.create_file(session=session, file_in=file_in, owner_id=current_user.id)

    return to_pydantic(file, FilePublic)

@router.get("/{file_id}", response_model=FilePublic)
def read_file(session: SessionDep, file_id: int) -> Any:
    """
    Get an file by id.
    """
    file = file_crud.read_file(session=session, id=file_id)

    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return to_pydantic(file, FilePublic)

@router.get("/", response_model=FilesPublic)
def read_files(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 25
) -> Any:
    """
    Get a list of files with the current_user's id.
    """
    count = file_crud.read_file_count_by_owner_id(session=session, user_id=current_user.id)
    all_files = file_crud.read_all_files_by_owner_id(session=session, user_id=current_user.id, skip=skip, limit=limit)

    result = [to_pydantic(file, FilePublic) for file in all_files]

    return FilesPublic(data=result, count=count)

@router.put("/{file_id}", response_model=FilePublic)
def update_file(
    *, session: SessionDep, current_user: CurrentUser, file_id: int, file_in: FileUpdate
) -> Any:
    """
    Update a file by it's id.
    """
    file = file_crud.read_file(session=session, id=file_id)
    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if (file.owner_id != current_user.id):
        raise HTTPException(
            status_code=400,
            detail="User does not have permission to update this file"
        )

    update_file = file_crud.update_file(session=session, file_id=file.id, file_in=file_in)

    return to_pydantic(update_file, FilePublic)

@router.delete("/{file_id}", response_model=Message)
def delete_file(
    *, session: SessionDep, current_user: CurrentUser, file_id: int
) -> Any:
    """
    Delete a file by it's id.
    """
    file = file_crud.read_file(session=session, id=file_id)
    if not file:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    if (file.owner_id != current_user.id):
        raise HTTPException(
            status_code=400,
            detail="User does not have permission to delete this file"
        )

    return file_crud.delete_file(session=session, file_id=file_id)
