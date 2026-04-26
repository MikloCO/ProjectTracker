from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
)


class AddCourseDialog(QDialog):
    """Dialog for creating or editing a course. Pass `course` to enter edit mode."""

    def __init__(self, parent=None, manager=None, course=None):
        super().__init__(parent)

        self.manager = manager
        self.course = course
        self.edit_mode = course is not None

        self.setWindowTitle("Edit Course" if self.edit_mode else "Add Course")
        self.setGeometry(100, 100, 400, 400)

        layout = QFormLayout(self)

        # Inputs
        self.title_input = QLineEdit()
        self.provider_input = QLineEdit()
        self.link_input = QLineEdit()
        self.in_progress = QCheckBox()
        self.project_path = QLineEdit()

        self.chapters_input = QSpinBox()
        self.chapters_input.setMinimum(1)
        self.chapters_input.setValue(1)
        self.chapters_input.setMaximum(9999)

        # Banner
        self.banner_path = QLineEdit()
        self.banner_path.setReadOnly(True)
        self.banner_path.setPlaceholderText("No image selected")

        banner_button = QPushButton("Browse...")
        banner_button.clicked.connect(self.select_banner)

        banner_layout = QHBoxLayout()
        banner_layout.addWidget(self.banner_path)
        banner_layout.addWidget(banner_button)

        # Category dropdown with custom input
        self.category_combo = QComboBox()
        self.category_combo.addItems(["art", "programming", "ai", "new"])
        self.category_combo.currentTextChanged.connect(self.on_category_changed)

        self.category_custom = QLineEdit()
        self.category_custom.setPlaceholderText("Enter custom category")
        self.category_custom.setVisible(False)

        category_layout = QHBoxLayout()
        category_layout.addWidget(self.category_combo)
        category_layout.addWidget(self.category_custom)

        # Add rows
        layout.addRow("Title:", self.title_input)
        layout.addRow("Provider:", self.provider_input)
        layout.addRow("Link:", self.link_input)
        layout.addRow("Number of Chapters:", self.chapters_input)
        layout.addRow("Banner Image:", banner_layout)
        layout.addRow("Category:", category_layout)
        layout.addRow("Project Path (locally):", self.project_path)
        layout.addRow("In Progress:", self.in_progress)
        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.handle_accept)
        button_box.rejected.connect(self.reject)

        layout.addRow(button_box)

        if self.edit_mode:
            self._prefill()

    def _prefill(self):
        c = self.course
        self.title_input.setText(c.title)
        self.provider_input.setText(c.provider)
        self.link_input.setText(c.link or "")
        self.chapters_input.setValue(len(c.chapters))
        self.banner_path.setText(c.banner_path or "")
        self.in_progress.setChecked(c.status == "in_progress")

        self.project_path.setText(c.project_path or "")

        known = ["art", "programming", "ai"]
        if c.category in known:
            self.category_combo.setCurrentText(c.category)
        elif c.category:
            self.category_combo.setCurrentText("new")
            self.category_custom.setText(c.category)
            self.category_custom.setVisible(True)

    def on_category_changed(self, text):
        """Show custom input field when 'new' is selected"""
        self.category_custom.setVisible(text == "new")

    def select_banner(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Course Banner Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)",
        )
        if file_path:
            self.banner_path.setText(file_path)

    def handle_accept(self):
        title = self.title_input.text()
        provider = self.provider_input.text()
        link = self.link_input.text()
        num_chapters = self.chapters_input.value()
        banner = self.banner_path.text()
        status = "in_progress" if self.in_progress.isChecked() else "todo"

        # Get category
        category = self.category_combo.currentText()
        if category == "new":
            category = self.category_custom.text()
            if not category:
                return

        # Validation
        if not title or not provider or not banner or not self.manager:
            return

        if banner == "No image selected":
            return

        project_path = self.project_path.text() or None

        if self.edit_mode:
            self.manager.update_course(
                self.course.id,
                title,
                provider,
                link,
                num_chapters,
                banner,
                category,
                status,
                project_path,
            )
        else:
            self.manager.create_and_save_course(
                title,
                provider,
                link,
                num_chapters,
                banner,
                category,
                status,
                project_path,
            )

        self.accept()
