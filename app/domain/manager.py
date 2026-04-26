# core/manager.py

from PySide6.QtCore import QObject, Signal

from .models import Chapter, Course
from .storage import save_courses


class CourseManager(QObject):
    """
    Central manager responsible for handling course data, updates, and persistence.

    This class acts as the single source of truth for all course-related operations,
    including creation, modification, and saving to disk.

    Attributes:
        courses (list[Course]): List of all loaded courses.
        max_active (int): Maximum number of courses allowed to be active simultaneously.
        current_course (Course | None): Currently selected course.
    """

    course_updated = Signal(int)  # emitted with course_id when a course changes

    def __init__(self, courses: list[Course], max_active: int = 3):
        """
        Initialize the CourseManager.

        Args:
            courses: Preloaded list of Course objects.
            max_active: Maximum number of active courses allowed.
        """
        super().__init__()
        self.courses = courses
        self.max_active = max_active
        self.current_course = None

    def add_course(self, course: Course):
        """
        Add a new course to the manager.

        Args:
            course: The Course instance to add.
        """
        self.courses.append(course)

    def create_and_save_course(
        self,
        title: str,
        provider: str,
        link: str,
        num_chapters: int,
        banner_path: str | None = None,
        category: str | None = None,
        status: str = "todo",
        project_path: str | None = None,
    ):
        """
        Create a new course with generated chapters and persist it.

        Args:
            title: Name of the course.
            provider: Platform or provider of the course.
            link: Optional URL to the course.
            num_chapters: Number of chapters to generate.
            banner_path: Optional path to a banner image.
            category: Optional category label.
            status: Initial course status (default is "todo").
        """
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
            project_path=project_path,
            chapters=chapters,
            status=status,
        )

        self.add_course(new_course)
        save_courses(self.courses)

    def active_count(self, exclude_id: int | None = None) -> int:
        return sum(
            1 for c in self.courses if c.status == "in_progress" and c.id != exclude_id
        )

    def update_status(self, course_id: int, status: str):
        """
        Update the status of a course and persist the change.

        Args:
            course_id: ID of the course to update.
            status: New status value.
        """
        course = self.get(course_id)
        course.status = status
        save_courses(self.courses)

    def get(self, course_id: int) -> Course:
        """
        Retrieve a course by its ID.

        Args:
            course_id: ID of the course.

        Returns:
            The matching Course instance.

        Raises:
            StopIteration: If no course with the given ID exists.
        """
        return next(c for c in self.courses if c.id == course_id)

    def update_course(
        self,
        course_id: int,
        title: str,
        provider: str,
        link: str,
        num_chapters: int,
        banner_path: str | None,
        category: str | None,
        status: str,
        project_path: str | None = None,
    ):
        """Update an existing course's metadata, adding new chapters if num_chapters increased."""
        course = self.get(course_id)
        course.title = title
        course.provider = provider
        course.link = link if link else None
        course.banner_path = banner_path if banner_path else None
        course.category = category
        course.project_path = project_path
        course.status = status

        current_count = len(course.chapters)
        if num_chapters > current_count:
            for i in range(current_count, num_chapters):
                course.chapters.append(Chapter(id=i + 1, title=f"Chapter {i + 1}"))

        save_courses(self.courses)
        self.course_updated.emit(course_id)

    def set_chapter_completed(self, course_id: int, chapter_id: int, completed: bool):
        """
        Mark a chapter as completed or not and persist the change.

        Args:
            course_id: ID of the course.
            chapter_id: ID of the chapter within the course.
            completed: Whether the chapter is completed.
        """
        course = self.get(course_id)
        chapter = next(c for c in course.chapters if c.id == chapter_id)
        chapter.completed = completed
        save_courses(self.courses)
        self.course_updated.emit(course_id)
