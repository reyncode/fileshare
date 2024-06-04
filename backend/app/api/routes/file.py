from typing import Any

from fastapi import APIRouter, HTTPException

from app.crud.file import files
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
    Create a new file database object with name and path owned by the current user.
    """
    # TODO: instead of 400, rename the path to _1 or something similar for duplicate file names. 

    file = files.read_file_by_path(session=session, path=file_in.path, owner_id=current_user.id)

    if file:
        raise HTTPException(
            status_code=400,
            detail="A file with the same name already exists"
        )

    file = files.create_file(session=session, file_in=file_in, owner_id=current_user.id)

    return to_pydantic(file, FilePublic)

@router.get("/{file_id}", response_model=FilePublic)
def read_file(session: SessionDep, file_id: int) -> Any:
    """
    Get an file by id.
    """
    file = files.read_file(session=session, id=file_id)

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
    count = files.read_file_count_by_user_id(session=session, user_id=current_user.id)
    all_files = files.read_all_files_by_user_id(session=session, user_id=current_user.id, skip=skip, limit=limit)

    result = [to_pydantic(file, FilePublic) for file in all_files]

    return FilesPublic(data=result, count=count)

@router.put("/{file_id}", response_model=FilePublic)
def update_file(
    *, session: SessionDep, current_user: CurrentUser, file_id: int, file_in: FileUpdate
) -> Any:
    """
    Update a file by it's id.
    """
    file = files.read_file(session=session, id=file_id)
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

    update_file = files.update_file(session=session, file_id=file.id, file_in=file_in)

    return to_pydantic(update_file, FilePublic)

@router.delete("/{file_id}", response_model=Message)
def delete_file(
    *, session: SessionDep, current_user: CurrentUser, file_id: int
) -> Any:
    """
    Delete a file by it's id.
    """
    file = files.read_file(session=session, id=file_id)
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

    return files.delete_file(session=session, file_id=file_id)
