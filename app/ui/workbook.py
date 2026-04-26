# ui/widgets/workbook.py

from pathlib import Path
from typing import override

import qtawesome as qta
from PySide6.QtGui import QFont, Qt, QTextListFormat
from PySide6.QtWidgets import QTextEdit, QToolBar, QVBoxLayout, QWidget

from app.ui.theme import get_saved_theme

# WORKBOOK_FILE = Path.home() / ".course_tracker" / "workbook.html"


class WorkbookTextEdit(QTextEdit):
    """QTextEdit that strips rich content on paste, accepting plain text only."""

    def __init__(self):
        super().__init__()
        self.setTextInteractionFlags(Qt.TextEditorInteraction)

    @override
    def insertFromMimeData(self, source):
        # Only allow plain text
        if source.hasText():
            self.insertPlainText(source.text())


class WorkbookWidget(QWidget):
    """Rich-text editor for course notes, auto-saved per course to ~/.course_tracker/workbooks/."""

    def __init__(self, course):
        super().__init__()

        self.editor = WorkbookTextEdit()
        self.toolbar = QToolBar("Workbook Toolbar")
        self.layout = QVBoxLayout()
        self.course = course
        self.file_path = self.get_workbook_path()

        self.toolbar.toggleViewAction().setEnabled(False)

        ic = "#333333" if get_saved_theme() == "light" else "#cccccc"

        bold_action = self.toolbar.addAction(qta.icon("fa5s.bold", color=ic), "Bold")
        bold_action.triggered.connect(self.format_bold)
        italic_action = self.toolbar.addAction(
            qta.icon("fa5s.italic", color=ic), "Italic"
        )
        italic_action.triggered.connect(self.format_italic)
        underline_action = self.toolbar.addAction(
            qta.icon("fa5s.underline", color=ic), "Underline"
        )
        underline_action.triggered.connect(self.format_underline)
        self.toolbar.addSeparator()
        bullet_action = self.toolbar.addAction(
            qta.icon("fa5s.list-ul", color=ic), "Bullet List"
        )
        bullet_action.triggered.connect(self.insert_bullet_list)
        numbered_action = self.toolbar.addAction(
            qta.icon("fa5s.list-ol", color=ic), "Numbered List"
        )
        numbered_action.triggered.connect(self.insert_numbered_list)
        self.toolbar.addSeparator()
        undo_action = self.toolbar.addAction(qta.icon("fa5s.undo", color=ic), "Undo")
        undo_action.triggered.connect(self.editor.undo)
        redo_action = self.toolbar.addAction(qta.icon("fa5s.redo", color=ic), "Redo")
        redo_action.triggered.connect(self.editor.redo)
        clear_action = self.toolbar.addAction(
            qta.icon("fa5s.eraser", color=ic), "Clear Formatting"
        )
        clear_action.triggered.connect(self.clear_formatting)

        self.layout.addWidget(self.toolbar)

        self.layout.addWidget(self.editor)
        self.setLayout(self.layout)

        self._ensure_file()
        self.load()

        # Auto-save on change
        self.editor.textChanged.connect(self.save)

    def get_workbook_path(self) -> Path:
        base = Path.home() / ".course_tracker" / "workbooks"
        base.mkdir(parents=True, exist_ok=True)
        return base / f"course_{self.course.id}.html"

    def _ensure_file(self):
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            self.file_path.write_text("", encoding="utf-8")

    def load(self):
        content = self.file_path.read_text(encoding="utf-8")
        self.editor.setHtml(content)

    def save(self):
        content = self.editor.toHtml()
        self.file_path.write_text(content, encoding="utf-8")

    def format_bold(self):
        self.editor.setFontWeight(
            QFont.Bold if self.editor.fontWeight() == QFont.Normal else QFont.Normal
        )

    def format_italic(self):
        self.editor.setFontItalic(not self.editor.fontItalic())

    def format_underline(self):
        self.editor.setFontUnderline(not self.editor.fontUnderline())

    def insert_bullet_list(self):
        cursor = self.editor.textCursor()
        current_list = cursor.currentList()

        # Toggle OFF if already bullet
        if current_list and current_list.format().style() == QTextListFormat.ListDisc:
            current_list.remove(cursor.block())
            block_format = cursor.blockFormat()
            block_format.setIndent(0)
            cursor.setBlockFormat(block_format)
            return

        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.ListDisc)
        cursor.createList(list_format)

    def insert_numbered_list(self):
        cursor = self.editor.textCursor()
        current_list = cursor.currentList()

        # If already in a numbered list, remove it
        if current_list:
            list_format = current_list.format()
            if list_format.style() == QTextListFormat.ListDecimal:
                cursor.removeSelectedText()
                block_format = cursor.blockFormat()
                block_format.setIndent(0)
                cursor.setBlockFormat(block_format)
                self.editor.setTextCursor(cursor)
                return

        # Insert numbered list
        list_format = QTextListFormat()
        list_format.setStyle(QTextListFormat.ListDecimal)
        cursor.insertList(list_format)

    def clear_formatting(self):
        self.editor.setCurrentFont(self.editor.font())
