from PySide6.QtWidgets import (
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
    def __init__(self, parent=None, manager=None):
        super().__init__(parent)

        self.manager = manager

        self.setWindowTitle("Add Course")
        self.setGeometry(100, 100, 400, 400)

        layout = QFormLayout(self)

        # Inputs
        self.title_input = QLineEdit()
        self.provider_input = QLineEdit()
        self.link_input = QLineEdit()

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

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.handle_accept)
        button_box.rejected.connect(self.reject)

        layout.addRow(button_box)

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

        self.manager.create_and_save_course(
            title, provider, link, num_chapters, banner, category
        )

        self.accept()
