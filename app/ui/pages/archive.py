from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.ui.course_widget import CourseWidget


class ArchivePage(QWidget):
    def __init__(self, manager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        title_layout = QHBoxLayout()
        title_label = QLabel("Archived Courses")
        title_layout.addWidget(title_label)
        main_layout.addLayout(title_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.container_layout = QVBoxLayout(container)

        scroll.setWidget(container)
        main_layout.addWidget(scroll)

        self.populate_courses()

    def populate_courses(self):
        def clear_layout(layout):
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
                elif item.layout():
                    clear_layout(item.layout())

        clear_layout(self.container_layout)

        # Filter archived courses
        courses = [c for c in self.manager.courses if c.status == "completed"]

        if not courses:
            label = QLabel("No archived courses yet.")
            label.setWordWrap(True)
            self.container_layout.addWidget(label)
            return

        # Group by category
        categories = {}
        for course in courses:
            key = course.category or "Uncategorized"
            categories.setdefault(key, []).append(course)

        # Build UI
        for category in sorted(categories.keys()):
            course_list = sorted(categories[category], key=lambda c: c.title)

            label = QLabel(category)
            self.container_layout.addWidget(label)

            grid = QGridLayout()
            grid.setSpacing(10)

            for i, course in enumerate(course_list):
                row = i // 3
                col = i % 3

                widget = CourseWidget(course)
                grid.addWidget(widget, row, col)
                widget.button.clicked.connect(
                    lambda _, c=course: self.open_course_detail(c)
                )

            self.container_layout.addLayout(grid)

    def open_course_detail(self, course):
        main_window = self.window()
        main_window.current_page.set_course(course)
        main_window.stack.setCurrentWidget(main_window.current_page)
