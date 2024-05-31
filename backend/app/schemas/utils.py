from typing import Type, TypeVar

from pydantic import BaseModel

from app.database.core import Base

T = TypeVar("T", bound=BaseModel)

def to_pydantic(db_object: Base, pydantic_model: Type[T]) -> T: # type: ignore
    return pydantic_model(**db_object.__dict__)
