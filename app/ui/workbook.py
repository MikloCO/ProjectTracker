# ui/widgets/workbook.py

import uuid
from pathlib import Path
from typing import override

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget

WORKBOOK_FILE = Path.home() / ".course_tracker" / "workbook.html"
IMAGES_DIR = Path.home() / ".course_tracker" / "workbook_images"


class WorkbookTextEdit(QTextEdit):
    """Custom QTextEdit that handles image pasting from clipboard"""

    @override
    def insertFromMimeData(self, source):
        """Override to handle image pasting"""
        if source.hasImage():
            # Get image from clipboard
            pixmap = QPixmap(source.imageData())

            if not pixmap.isNull():
                # Ensure images directory exists
                IMAGES_DIR.mkdir(parents=True, exist_ok=True)

                # Generate unique filename
                image_filename = f"image_{uuid.uuid4().hex}.png"
                image_path = IMAGES_DIR / image_filename

                # Save image
                if pixmap.save(str(image_path)):
                    # Insert image reference into editor
                    cursor = self.textCursor()
                    cursor.insertHtml(f'<img src="{image_path}" width="400">')
                    return

        # Fall back to default behavior
        super().insertFromMimeData(source)


class WorkbookWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.editor = WorkbookTextEdit()

        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        self.setLayout(layout)

        self._ensure_file()
        self.load()

        # Auto-save on change
        self.editor.textChanged.connect(self.save)

    def _ensure_file(self):
        WORKBOOK_FILE.parent.mkdir(parents=True, exist_ok=True)

        if not WORKBOOK_FILE.exists():
            WORKBOOK_FILE.write_text("", encoding="utf-8")

    def load(self):
        content = WORKBOOK_FILE.read_text(encoding="utf-8")
        self.editor.setHtml(content)

    def save(self):
        content = self.editor.toHtml()
        WORKBOOK_FILE.write_text(content, encoding="utf-8")
