from PySide6.QtWidgets import QApplication

from app.domain import logging_config, storage
from app.domain.manager import CourseManager
from app.ui.main_window import MainWindow
from app.ui.theme import get_saved_theme, load_theme


def main():
    logging_config.setup_logging()
    app = QApplication([])
    app.setStyle("Fusion")
    app.setStyleSheet(load_theme(get_saved_theme()))
    courses = storage.load_courses()
    manager = CourseManager(courses)

    window = MainWindow(manager)
    window.show()

    app.exec()

    storage.save_courses(manager.courses)


if __name__ == "__main__":
    main()
