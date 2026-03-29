import sys

import qtawesome as qta
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.domain.manager import CourseManager
from app.domain.storage import load_courses
from app.ui.course_widget import CourseWidget
from app.ui.new_course_dialog import AddCourseDialog
from app.ui.workbook import WorkbookWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Project Tracker")
        self.setMinimumSize(800, 400)

        # Load courses from JSON storage
        courses = load_courses()
        self.manager = CourseManager(courses)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.main_layout = QVBoxLayout(central_widget)

        # Title with icon
        title_layout = QHBoxLayout()
        title_label = QLabel("In progress")
        title_layout.addWidget(title_label)

        # Add single plus button to add new course
        add_button = QPushButton()
        add_button.setIcon(qta.icon("fa5s.plus", color="black", scale_factor=1.5))
        add_button.setMaximumWidth(60)
        add_button.clicked.connect(self.open_add_course_dialog)
        title_layout.addWidget(add_button)

        title_layout.addStretch()
        self.main_layout.addLayout(title_layout)

        self.refresh_courses()

        self.workbook = WorkbookWidget()
        self.main_layout.addWidget(self.workbook)
        self.setCentralWidget(central_widget)

    def refresh_courses(self):
        """Refresh the course display"""
        # Remove old course row if it exists
        if hasattr(self, "course_row_widget") and self.course_row_widget:
            self.main_layout.removeWidget(self.course_row_widget)
            self.course_row_widget.deleteLater()

        # Reload courses from storage
        courses = load_courses()
        self.manager.courses = courses

        # Create new course row container
        self.course_row_widget = QWidget()
        course_row = QHBoxLayout(self.course_row_widget)
        course_row.setContentsMargins(0, 0, 0, 0)

        # Add loaded courses
        for course in self.manager.courses:
            course_row.addWidget(CourseWidget(course, manager=self.manager))

        course_row.addStretch()

        # Insert before workbook
        self.main_layout.insertWidget(1, self.course_row_widget)

    def open_add_course_dialog(self):
        dialog = AddCourseDialog(self, manager=self.manager)
        if dialog.exec():
            self.refresh_courses()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
