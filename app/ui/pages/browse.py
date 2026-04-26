from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.ui.course_widget import CourseWidget


class BrowsePage(QWidget):
    def __init__(self, manager, parent=None):
        super().__init__(parent)
        self.manager = manager
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Title
        title_layout = QHBoxLayout()
        title_label = QLabel("Browse Courses")
        title_layout.addWidget(title_label)
        main_layout.addLayout(title_layout)

        # Scroll Area
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

        # Only NOT active courses (browse)
        courses = [c for c in self.manager.courses if c.status == "todo"]

        if not courses:
            self.container_layout.addWidget(
                QLabel(
                    "Courses that are not started yet will show up here. Add a few courses from new-> add course."
                )
            )

        # Group by category
        categories = {}
        for course in courses:
            key = course.category or "Uncategorized"
            categories.setdefault(key, []).append(course)

        # Build UI per category
        for category in sorted(categories.keys()):
            course_list = sorted(
                categories[category], key=lambda c: c.title
            )  # Category title
            label = QLabel(category)
            self.container_layout.addWidget(label)

            # Grid for courses
            grid = QGridLayout()
            grid.setSpacing(10)

            for i, course in enumerate(course_list):
                row = i // 3
                col = i % 3

                course_widget = CourseWidget(course, manager=self.manager)
                grid.addWidget(course_widget, row, col)
                course_widget.button.clicked.connect(
                    lambda _, c=course: self.open_course_detail(c)
                )

            self.container_layout.addLayout(grid)

    def open_course_detail(self, course):
        main_window = self.window()
        main_window.current_page.set_course(course)
        main_window.stack.setCurrentWidget(main_window.current_page)
