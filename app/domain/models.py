# core/models.py

from pydantic import BaseModel, Field, field_validator


class Chapter(BaseModel):
    id: int
    title: str
    completed: bool = False
    notes: str = ""


class Course(BaseModel):
    id: int
    title: str
    provider: str
    link: str | None = None
    banner_path: str | None = None
    category: str | None = None

    chapters: list[Chapter] = Field(default_factory=list)

    active: bool = False

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value
