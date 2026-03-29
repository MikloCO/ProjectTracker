# core/manager.py

from .models import Chapter, Course
from .storage import save_courses


class CourseManager:
    def __init__(self, courses: list[Course], max_active: int = 3):
        self.courses = courses
        self.max_active = max_active

    def add_course(self, course: Course):
        self.courses.append(course)

    def create_and_save_course(
        self,
        title: str,
        provider: str,
        link: str,
        num_chapters: int,
        banner_path: str | None = None,
        category: str | None = None,
    ):
        """Create a new course with chapters and save to storage"""
        # Create new course with chapters
        new_id = max([c.id for c in self.courses], default=0) + 1
        chapters = [
            Chapter(id=i + 1, title=f"Chapter {i + 1}") for i in range(num_chapters)
        ]

        new_course = Course(
            id=new_id,
            title=title,
            provider=provider,
            link=link if link else None,
            banner_path=banner_path,
            category=category,
            chapters=chapters,
        )

        self.add_course(new_course)
        save_courses(self.courses)

    def activate_course(self, course_id: int):
        active_count = sum(c.active for c in self.courses)

        if active_count >= self.max_active:
            raise ValueError("Pipeline limit reached")

        course = self.get(course_id)
        course.active = True

    def complete_chapter(self, course_id: int, chapter_id: int):
        course = self.get(course_id)

        chapter = next(c for c in course.chapters if c.id == chapter_id)
        chapter.completed = True

    def add_note(self, course_id: int, chapter_id: int, text: str):
        course = self.get(course_id)
        chapter = next(c for c in course.chapters if c.id == chapter_id)

        chapter.notes += f"\n{text}"

    def get(self, course_id: int) -> Course:
        return next(c for c in self.courses if c.id == course_id)
