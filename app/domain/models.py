# core/models.py

from typing import Literal

from pydantic import BaseModel, Field, field_validator


class Chapter(BaseModel):
    """A single chapter within a course, tracking completion and optional notes."""

    id: int
    title: str
    completed: bool = False
    notes: str = ""


CourseStatus = Literal["todo", "in_progress", "completed"]


class Course(BaseModel):
    """A course with its metadata, chapters, gallery images, and current status."""

    id: int
    title: str
    provider: str
    link: str | None = None
    banner_path: str | None = None
    category: str | None = None

    project_path: str | None = None
    chapters: list[Chapter] = Field(default_factory=list)
    image_paths: list[str] = Field(default_factory=list)
    status: CourseStatus = "todo"

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Title cannot be empty")
        return value
