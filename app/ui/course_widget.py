import qtawesome as qta
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap, Qt
from PySide6.QtWidgets import QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget

from app.domain.manager import CourseManager
from app.domain.models import Course
from app.ui.new_course_dialog import AddCourseDialog


class CourseWidget(QWidget):
    """Card widget displaying a course banner, title, and progress bar."""

    def __init__(self, course=None, manager=None):
        super().__init__()
        self.course: Course = course
        self.manager: CourseManager = manager

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.setLayout(self.layout)
        self.card = QVBoxLayout()
        self.card.setContentsMargins(0, 0, 0, 0)
        self.card.setSpacing(0)
        self.card.setAlignment(Qt.AlignHCenter)

        self.button = QPushButton()
        self.button.setFixedSize(200, 150)

        self.title_label = QLabel()
        self.title_label.setFixedHeight(40)
        self.title_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        if self.manager:
            self.manager.course_updated.connect(self.on_course_updated)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedWidth(200)
        self.progress_bar.setTextVisible(False)

        self.card.addWidget(self.title_label)
        self.card.addWidget(self.button)
        self.card.addWidget(self.progress_bar)

        if course:
            self.setup_course()
        else:
            self.setup_empty()

        self.layout.addLayout(self.card)
        self.setFixedHeight(220)
        self.on_course_updated(self.course.id)

    def on_course_updated(self, course_id):
        if not self.course:
            return

        if self.course.id == course_id:
            self.update_progressbar()

    def setup_course(self):
        if self.course.banner_path:
            pixmap = QPixmap(self.course.banner_path)
            self.title_label.setText(self.course.title)

            # Check if pixmap loaded successfully
            if not pixmap.isNull():
                w, h = self.button.width(), self.button.height()
                scaled = pixmap.scaled(
                    w, h, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
                )
                x = (scaled.width() - w) // 2
                y = (scaled.height() - h) // 2
                self.button.setIcon(QIcon(scaled.copy(x, y, w, h)))
                self.button.setIconSize(QSize(w, h))
            else:
                # If image failed to load, show a placeholder
                self.button.setIcon(qta.icon("fa6s.image"))
                self.button.setText("Image not found")

        # Set title label styling if it exists
        if self.title_label:
            self.title_label.setWordWrap(True)

        self.update_progressbar()

        # Clean style for course buttons
        self.button.setStyleSheet("""
            QPushButton {
                padding: 0px;
                margin: 0px;
                border: none;
            }
        """)

    def update_progressbar(self):
        # Calculate and display progress
        if self.course.chapters:
            completed = sum(1 for ch in self.course.chapters if ch.completed)
            total = len(self.course.chapters)
            progress_percent = int((completed / total) * 100)
            self.progress_bar.setValue(progress_percent)
        else:
            self.progress_bar.setValue(0)

    def setup_empty(self):
        self.title_label.setText("Empty slot")
        self.button.setIcon(qta.icon("fa6s.plus"))
        self.button.clicked.connect(self.open_add_course_dialog)
        self.button.setStatusTip("Add a new course")
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.button.setStyleSheet("""
                                  QPushButton {
                                      background-color: #f0f0f0;
                                      border: 2px dashed #ccc;
                                  }
                                  """)

        # Set fixed width for the widget
        self.setFixedWidth(200)

    def open_add_course_dialog(self):
        dialog = AddCourseDialog(self, manager=self.manager)
        dialog.exec()

    def update_progress(self):
        if self.course.chapters:
            completed = sum(1 for ch in self.course.chapters if ch.completed)
            total = len(self.course.chapters)
            progress_percent = int((completed / total) * 100)
            self.progress_bar.setValue(progress_percent)
        else:
            self.progress_bar.setValue(0)
