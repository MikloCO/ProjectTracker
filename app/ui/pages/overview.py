from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from app.ui.course_widget import CourseWidget
from app.ui.new_course_dialog import AddCourseDialog


class OverviewPage(QWidget):
    """Page showing all in-progress courses as clickable course cards."""

    def __init__(self, manager, parent=None):
        super().__init__(parent)

        self.manager = manager
        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()

        # # Title with icon
        self.title_layout = QHBoxLayout()
        self.title_label = QLabel()

        self.main_layout.addLayout(self.title_layout)
        self.setLayout(self.main_layout)

        self.refresh_courses()

    def refresh_courses(self):
        """Refresh the course display"""
        # Clear title area
        while self.title_layout.count():
            item = self.title_layout.takeAt(0)
            widget = item.widget()
            if widget and widget is not self.title_label:
                widget.deleteLater()

        # Remove old course row if it exists
        if hasattr(self, "course_row_widget") and self.course_row_widget:
            self.main_layout.removeWidget(self.course_row_widget)
            self.course_row_widget.deleteLater()

        # Create new course row container
        self.course_row_widget = QWidget()
        course_row = QHBoxLayout(self.course_row_widget)
        course_row.setContentsMargins(0, 0, 0, 0)

        in_progress_courses = [
            c for c in self.manager.courses if c.status == "in_progress"
        ]

        if not in_progress_courses:
            self.title_layout.addWidget(
                QLabel(
                    "Use the toolbar to add a new course (New->New course), or choose one from the Browse section."
                )
            )
        else:
            self.title_label.setText("In progress")
            self.title_layout.addWidget(self.title_label)

        for course in in_progress_courses:
            in_progress_course = CourseWidget(course, manager=self.manager)
            course_row.addWidget(in_progress_course)

            in_progress_course.button.clicked.connect(
                lambda _, c=course: self.open_course_detail(c)
            )

        course_row.addStretch()

        # Insert before workbook
        self.main_layout.insertWidget(1, self.course_row_widget)

    def open_add_course_dialog(self):
        dialog = AddCourseDialog(self, manager=self.manager)
        if dialog.exec():
            self.refresh_courses()

    def open_course_detail(self, course):
        main_window = self.window()
        main_window.current_page.set_course(course)
        main_window.stack.setCurrentWidget(main_window.current_page)
