from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from app.domain.manager import CourseManager
from app.ui.new_course_dialog import AddCourseDialog
from app.ui.pages.archive import ArchivePage
from app.ui.pages.browse import BrowsePage
from app.ui.pages.current import CurrentPage
from app.ui.pages.overview import OverviewPage


class MainWindow(QMainWindow):
    """Root application window with a stacked page layout and toolbar navigation."""

    def __init__(self, manager: CourseManager):
        super().__init__()
        self.setWindowTitle("Project Tracker")
        self.setMinimumSize(800, 400)

        self.manager = manager
        self.setup_ui()

    def setup_ui(self):
        self.stack = QStackedWidget()

        self.overview_page = OverviewPage(self.manager, parent=self)
        self.browse_page = BrowsePage(self.manager, parent=self)
        self.archived_page = ArchivePage(self.manager, parent=self)
        self.current_page = CurrentPage(self.manager, parent=self)

        self.stack.addWidget(self.overview_page)
        self.stack.addWidget(self.browse_page)
        self.stack.addWidget(self.archived_page)
        self.stack.addWidget(self.current_page)

        toolbar = QToolBar("Navigation")
        self.addToolBar(toolbar)

        layout = QHBoxLayout()

        toolbar.addAction(self.make_action("Overview", 0))
        toolbar.addAction(self.make_action("Browse", 1))
        toolbar.addAction(self.make_action("Archived", 2))

        layout.addWidget(self.stack)

        # File menu
        menu = self.menuBar()

        file_menu = menu.addMenu("&New")
        add_action = QAction("Add new course", self)
        add_action.triggered.connect(self.open_add_course_dialog)
        file_menu.addAction(add_action)

        # Settings menu
        settings_menu = menu.addMenu("&Settings")
        settings_menu.addAction(
            "Edit color theme", lambda: self.on_settings("Edit color theme")
        )
        settings_menu.addAction(
            "Edit courses", lambda: self.on_settings("Edit courses")
        )

        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def make_action(self, name, index):
        action = QAction(name, self)
        action.triggered.connect(lambda: self.stack.setCurrentIndex(index))
        return action

    def make_page(self, text):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel(text))
        page.setLayout(layout)
        return page

    def make_nav_button(self, text, index):
        btn = QPushButton(text)
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(index))
        return btn

    def open_add_course_dialog(self):
        dialog = AddCourseDialog(self, manager=self.manager)
        if dialog.exec():
            self.refresh_all()

    def on_settings(self, action: str):
        if action == "Edit courses":
            courses = self.manager.courses
            if not courses:
                return
            names = [c.title for c in courses]
            name, ok = QInputDialog.getItem(
                self, "Edit Course", "Select a course:", names, editable=False
            )
            if not ok:
                return
            course = next(c for c in courses if c.title == name)
            dialog = AddCourseDialog(self, manager=self.manager, course=course)
            if dialog.exec():
                self.refresh_all()

    def refresh_all(self):
        self.overview_page.refresh_courses()
        self.browse_page.populate_courses()
        self.archived_page.populate_courses()
