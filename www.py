import sys
import json
import requests
from bs4 import BeautifulSoup
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QTextBrowser,
    QPushButton,
    QComboBox,
    QFileDialog,
)
from PyQt5.QtGui import QTextCharFormat, QColor


class PostmanWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Postman")
        self.setGeometry(100, 100, 800, 600)

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.main_layout = QVBoxLayout(self.central_widget)
        self.request_layout = QHBoxLayout()
        self.main_layout.addLayout(self.request_layout)

        # Request URL
        self.url_label = QLabel("URL:")
        self.url_input = QLineEdit()
        self.request_layout.addWidget(self.url_label)
        self.request_layout.addWidget(self.url_input)

        # HTTP Method
        self.method_label = QLabel("Method:")
        self.method_combo = QComboBox()
        self.method_combo.addItems(["GET", "POST", "PUT", "DELETE"])
        self.request_layout.addWidget(self.method_label)
        self.request_layout.addWidget(self.method_combo)

        # Request Headers
        self.headers_label = QLabel("Headers:")
        self.headers_input = QTextBrowser()
        self.main_layout.addWidget(self.headers_label)
        self.main_layout.addWidget(self.headers_input)

        # Request body
        self.body_label = QLabel("Request Body:")
        self.body_input = QTextBrowser()
        self.main_layout.addWidget(self.body_label)
        self.main_layout.addWidget(self.body_input)

        # Send button
        self.send_button = QPushButton("Send Request")
        self.send_button.clicked.connect(self.send_request)
        self.main_layout.addWidget(self.send_button)

        # Response
        self.response_label = QLabel("Response:")
        self.response_output = QTextBrowser()
        self.response_output.setReadOnly(True)
        self.main_layout.addWidget(self.response_label)
        self.main_layout.addWidget(self.response_output)

        # Response Mode
        self.response_mode_label = QLabel("Response Mode:")
        self.response_mode_combo = QComboBox()
        self.response_mode_combo.addItems(["Text", "HTML", "JSON"])
        self.response_mode_combo.currentIndexChanged.connect(self.set_response_mode)
        self.main_layout.addWidget(self.response_mode_label)
        self.main_layout.addWidget(self.response_mode_combo)

        # Save buttons
        self.save_json_button = QPushButton("Save JSON")
        self.save_html_button = QPushButton("Save HTML")
        self.save_json_button.clicked.connect(self.save_response_as_json)
        self.save_html_button.clicked.connect(self.save_response_as_html)
        self.main_layout.addWidget(self.save_json_button)
        self.main_layout.addWidget(self.save_html_button)

    def send_request(self):
        url = self.url_input.text()
        method = self.method_combo.currentText()
        headers = self.headers_input.toPlainText()
        request_body = self.body_input.toPlainText()

        try:
            response = requests.request(
                method,
                url,
                headers=self.parse_headers(headers),
                data=request_body,
            )
            response_text = f"Status Code: {response.status_code}\n\n"
            response_text += response.text
        except requests.exceptions.RequestException as e:
            response_text = f"Error: {str(e)}"

        self.response_output.setText(response_text)
    
    def parse_headers(self, headers):
        parsed_headers = {}
        lines = headers.split("\n")
        for line in lines:
            if ":" in line:
                key, value = line.split(":", 1)
                parsed_headers[key.strip()] = value.strip()
        return parsed_headers

    def set_response_mode(self, index):
        mode = self.response_mode_combo.currentText()

        if mode == "HTML":
            response_html = self.response_output.toPlainText()
            self.response_output.clear()
            self.print_colored_html(response_html)
        elif mode == "JSON":
            response_json = self.response_output.toPlainText()
            try:
                parsed_json = json.loads(response_json)
                pretty_json = json.dumps(parsed_json, indent=4)
                self.response_output.setPlainText(pretty_json)
            except json.JSONDecodeError:
                self.response_output.setPlainText(response_json)
        else:
            self.response_output.setPlainText(self.response_output.toPlainText())

    def print_colored_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        self.print_colored_html_recursive(soup)

    def print_colored_html_recursive(self, tag):
        if tag.string:
            self.print_colored_text(f"{tag.name}: {tag.string}")
        for child in tag.children:
            if isinstance(child, str):
                self.print_colored_text(child)
            elif child.name == "br":
                self.response_output.insertPlainText("\n")
            else:
                self.print_colored_html_recursive(child)

    def print_colored_text(self, text):
        text_format = QTextCharFormat()
        text_format.setForeground(QColor("blue"))
        self.response_output.setCurrentCharFormat(text_format)
        self.response_output.insertPlainText(text)

    def save_response_as_json(self):
        response = self.response_output.toPlainText()
        filename, _ = QFileDialog.getSaveFileName(self, "Save JSON", "", "JSON files (*.json)")
        if filename:
            with open(filename, "w") as file:
                file.write(response)

    def save_response_as_html(self):
        response = self.response_output.toPlainText()
        filename, _ = QFileDialog.getSaveFileName(self, "Save HTML", "", "HTML files (*.html)")
        if filename:
            with open(filename, "w") as file:
                file.write(response)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PostmanWindow()
    window.show()
    sys.exit(app.exec_())


