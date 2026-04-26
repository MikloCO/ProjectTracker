import shutil
import uuid
from pathlib import Path

import structlog
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices, QPixmap, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.ui.workbook import WorkbookWidget


class CurrentPage(QWidget):
    """Detail view for the selected course: chapters checklist, image gallery, and workbook."""

    def __init__(self, manager, parent=None):
        super().__init__(parent)
        self.manager = manager

        self.course = None

        self.setup_ui()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()

        self.splitter = QSplitter(Qt.Horizontal)

        # LEFT → Chapters
        self.left_widget = QWidget()
        self.left = QVBoxLayout(self.left_widget)

        # MIDDLE → Gallery
        self.middle_widget = QWidget()
        self.middle = QVBoxLayout(self.middle_widget)

        # RIGHT → Workbook
        self.right_widget = QWidget()
        self.right = QVBoxLayout(self.right_widget)

        # Add to splitter
        self.splitter.addWidget(self.left_widget)
        self.splitter.addWidget(self.middle_widget)
        self.splitter.addWidget(self.right_widget)

        # Stretch
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)
        self.splitter.setStretchFactor(2, 2)

        self.splitter.setHandleWidth(6)

        self.main_layout.addWidget(self.splitter)

        # Bottom row — local project path link
        self.path_row = QWidget()
        path_layout = QHBoxLayout(self.path_row)
        path_layout.setContentsMargins(4, 2, 4, 2)
        path_layout.addWidget(QLabel("Local Project:"))
        self.path_link = QPushButton()
        self.path_link.setFlat(True)
        self.path_link.setStyleSheet("text-align: left; color: palette(link);")
        self.path_link.clicked.connect(self.open_project_path)
        path_layout.addWidget(self.path_link, stretch=1)
        self.path_row.hide()
        self.main_layout.addWidget(self.path_row)

        self.setLayout(self.main_layout)

    def on_chapter_toggled(self, chapter, state):
        completed = bool(state)
        self.manager.set_chapter_completed(self.course.id, chapter.id, completed)

    def get_progress(self, course):
        total = len(course.chapters)
        if total == 0:
            return 0
        completed = sum(c.completed for c in course.chapters)
        return int((completed / total) * 100)

    def set_course(self, course):
        self.course = course
        self.refresh_ui()

    def refresh_ui(self):
        def clear(layout):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        clear(self.left)
        clear(self.middle)
        clear(self.right)

        if not self.course:
            return

        # -------- LEFT → Status --------
        self.left.addWidget(QLabel("Status"))
        status_combo = QComboBox()
        status_combo.addItems(["todo", "in_progress", "completed"])
        status_combo.setCurrentText(self.course.status)
        status_combo.currentTextChanged.connect(self.text_changed)
        self.left.addWidget(status_combo)

        # -------- LEFT → Chapters (scrollable) --------
        self.left.addWidget(QLabel("Chapters"))

        chapter_container = QWidget()
        chapter_layout = QVBoxLayout(chapter_container)
        chapter_layout.setContentsMargins(0, 0, 0, 0)
        chapter_layout.setSpacing(2)

        for chapter in self.course.chapters:
            checkbox = QCheckBox(chapter.title)
            checkbox.setChecked(chapter.completed)
            checkbox.stateChanged.connect(
                lambda state, c=chapter: self.on_chapter_toggled(c, state)
            )
            chapter_layout.addWidget(checkbox)

        chapter_layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(chapter_container)
        self.left.addWidget(scroll)

        # -------- MIDDLE → Gallery --------
        self.middle.addWidget(QLabel("Gallery"))
        self.middle.addWidget(GalleryWidget(self.course))

        # -------- RIGHT → Workbook --------
        self.right.addWidget(WorkbookWidget(self.course))

        # -------- BOTTOM → Local project path --------
        if self.course.project_path:
            self.path_link.setText(self.course.project_path)
            self.path_row.show()
        else:
            self.path_row.hide()

    def open_project_path(self):
        if self.course and self.course.project_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(self.course.project_path))

    def text_changed(self, status):
        if (
            status == "in_progress"
            and self.manager.active_count(exclude_id=self.course.id)
            >= self.manager.max_active
        ):
            QMessageBox.warning(
                self,
                "Too many active courses",
                f"You already have {self.manager.max_active} courses in progress.\nFinish or remove one before starting another.",
            )
            combo = self.sender()
            combo.blockSignals(True)
            combo.setCurrentText(self.course.status)
            combo.blockSignals(False)
            return
        self.course.status = status
        self.manager.update_status(self.course.id, status)
        self.window().refresh_all()


class ImageTile(QLabel):
    """Label that displays a single gallery image scaled to a fixed width."""

    def __init__(self, image_path=None, parent=None):
        super().__init__(parent)

        self.image_path = image_path
        self.setAlignment(Qt.AlignCenter)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.update_pixmap()

    def update_pixmap(self):
        if not self.image_path:
            return

        pixmap = QPixmap(self.image_path)
        scaled = pixmap.scaledToWidth(400, Qt.SmoothTransformation)

        self.setPixmap(scaled)
        self.setFixedHeight(scaled.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_pixmap()


class AddImageTile(QPushButton):
    """Button shown in the gallery that lets the user add new images."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setText("+")
        self.setFixedSize(200, 200)

        self.setStyleSheet("font-size: 24px;")


class GalleryWidget(QWidget):
    """Scrollable gallery of course images with an add-image button."""

    def __init__(self, course):
        super().__init__()

        self.course = course
        self.images = course.image_paths

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.scroll.setWidget(self.container)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll)

        self.refresh()

    def refresh(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        add_tile = AddImageTile()
        add_tile.clicked.connect(self.add_images)
        self.layout.addWidget(add_tile)

        # images
        for p in self.images:
            tile = ImageTile(image_path=p, parent=self.container)
            self.layout.addWidget(tile)

        self.layout.addStretch()

    def add_images(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not files:
            return

        for file_path in files:
            saved_path = self.save_image(file_path)
            self.images.append(saved_path)
        self.course.image_paths = self.images
        self.refresh()

    def get_images_dir(self, course_id: int) -> Path:
        base = Path.home() / ".course_tracker" / "images"
        path = base / f"course_{course_id}"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save_image(self, source_path: str) -> str:
        images_dir = self.get_images_dir(self.course.id)

        ext = Path(source_path).suffix
        new_name = f"{uuid.uuid4()}{ext}"
        new_path = images_dir / new_name

        try:
            shutil.copy(source_path, new_path)
        except Exception as e:
            structlog.get_logger().error("Failed to save courses", error=str(e))

        return str(new_path)
