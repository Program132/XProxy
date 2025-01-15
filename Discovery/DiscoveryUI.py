# DiscoveryUI.py: UI + UX for Discovery tool

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTableWidget, \
    QTableWidgetItem, QHBoxLayout, QSizePolicy, QCheckBox
from Discovery import DiscoveryLib as Lib
from Discovery.DiscoveryLib import parse_headers
import os

def createDiscoveryPage(application):
    page = QWidget()
    layout = QVBoxLayout()

    url_layout = QHBoxLayout()
    url_label = QLabel("URL:")
    url_input = QLineEdit()
    url_input.setPlaceholderText("Exemple: https://example.com")
    url_input.setObjectName("url_input")
    url_label.setFixedWidth(100)
    url_layout.addWidget(url_label)
    url_layout.addWidget(url_input)

    wordlist_layout = QHBoxLayout()
    wordlist_label = QLabel("Wordlist Path:")
    wordlist_input = QLineEdit()
    wordlist_input.setPlaceholderText("Exemple: /usr/share/wordlist/wordlist.txt")
    wordlist_input.setObjectName("wordlist_input")
    wordlist_browse_button = QPushButton("Search")
    wordlist_browse_button.clicked.connect(lambda: browseFile(application, wordlist_input))
    wordlist_label.setFixedWidth(100)
    wordlist_layout.addWidget(wordlist_label)
    wordlist_layout.addWidget(wordlist_input)
    wordlist_layout.addWidget(wordlist_browse_button)

    extensions_layout = QHBoxLayout()
    extensions_label = QLabel("Extensions:")
    extensions_label.setFixedWidth(100)
    extensions_input = QLineEdit()
    extensions_input.setPlaceholderText("Exemple: php,html,js")
    extensions_input.setObjectName("extensions_input")
    extensions_layout.addWidget(extensions_label)
    extensions_layout.addWidget(extensions_input)

    rate_layout = QHBoxLayout()
    rate_label = QLabel("Rate Limit (req/s):")
    rate_input = QLineEdit("10")
    rate_input.setObjectName("rate_input")
    rate_checkbox = QCheckBox("Enable Rate Limit")
    rate_checkbox.setObjectName("rate_checkbox")
    rate_checkbox.setChecked(False)
    rate_input.setEnabled(rate_checkbox.isChecked())
    rate_checkbox.stateChanged.connect(lambda state: rate_input.setEnabled(state == Qt.Checked))

    rate_label.setFixedWidth(100)
    rate_layout.addWidget(rate_checkbox)
    rate_layout.addWidget(rate_label)
    rate_layout.addWidget(rate_input)

    headers_layout = QHBoxLayout()
    headers_label = QLabel("Headers:")
    headers_input = QLineEdit()
    headers_input.setObjectName("headers_input")
    headers_input.setPlaceholderText("Exemple: User-Agent: Mozilla; X-Tester-X: program; Accept: */*")
    headers_label.setFixedWidth(100)
    headers_layout.addWidget(headers_label)
    headers_layout.addWidget(headers_input)

    threads_layout = QHBoxLayout()
    threads_label = QLabel("Number of Threads:")
    threads_label.setFixedWidth(100)
    threads_input = QLineEdit("4")
    threads_input.setObjectName("threads_input")
    threads_layout.addWidget(threads_label)
    threads_layout.addWidget(threads_input)

    buttons_layout = QHBoxLayout()
    run_button = QPushButton("Start Discovery")
    run_button.clicked.connect(
        lambda: runDiscovery(
            url_input.text(),
            wordlist_input.text(),
            extensions_input.text(),
            result_table,
            float(rate_input.text()) if rate_checkbox.isChecked() and rate_input.text().strip() else None,
            headers_input.text(),
            threads_input.text()
        )
    )

    reset_button = QPushButton("Reset")
    reset_button.clicked.connect(lambda: resetTable(result_table))

    run_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    reset_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    buttons_layout.addWidget(run_button)
    buttons_layout.addWidget(reset_button)
    buttons_layout.setAlignment(Qt.AlignLeft)

    result_table = QTableWidget()
    result_table.setObjectName("result_table")
    result_table.setColumnCount(3)
    result_table.setHorizontalHeaderLabels(["Path", "Status Code", "File Name"])
    result_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    result_table.horizontalHeader().setStretchLastSection(True)
    result_table.horizontalHeader().setSectionResizeMode(0, 1)
    result_table.horizontalHeader().setSectionResizeMode(1, 1)
    result_table.horizontalHeader().setSectionResizeMode(2, 1)

    layout.addLayout(url_layout)
    layout.addLayout(wordlist_layout)
    layout.addLayout(extensions_layout)
    layout.addLayout(rate_layout)
    layout.addLayout(headers_layout)
    layout.addLayout(threads_layout)
    layout.addLayout(buttons_layout)
    layout.addWidget(result_table)

    layout.setStretchFactor(result_table, 1)

    page.setLayout(layout)
    return page


def browseFile(application, input_field):
    file_path, _ = QFileDialog.getOpenFileName(application, "Select a file", "", "All files (*)")
    if file_path:
        input_field.setText(file_path)

def runDiscovery(url, wordlist_path, extensions, result_table, rate_limit=None, headers=None, threads_input=None):
    resetTable(result_table)

    rate_limit = float(rate_limit) if rate_limit is not None else None
    headers_dict = parse_headers(headers) if headers else {}
    num_threads = int(threads_input.strip()) if threads_input.strip().isdigit() else 1

    if not os.path.isfile(wordlist_path):
        raise FileNotFoundError(f"File not found: {wordlist_path}")

    if len(url) != 0 and len(wordlist_path) != 0:
        directories = Lib.run_folder_fuzzer(base_url=url, wordlist_path=wordlist_path, headers=headers_dict, rate_limit=rate_limit, num_threads=num_threads)
        for path, info in directories.items():
            status = info.get("status_code")
            full_url = info.get("path")
            row_position = result_table.rowCount()
            result_table.insertRow(row_position)
            result_table.setItem(row_position, 0, QTableWidgetItem(full_url))
            result_table.setItem(row_position, 1, QTableWidgetItem(str(status)))
            result_table.setItem(row_position, 2, QTableWidgetItem(path))

    if len(url) != 0 and len(wordlist_path) != 0 and len(extensions) != 0 and extensions.strip():
        files = Lib.run_files_fuzzer(base_url=url, wordlist_path=wordlist_path, extensions=extensions.split(","), headers=headers_dict, rate_limit=rate_limit, num_threads=num_threads)
        for path, info in files.items():
            status = info.get("status_code")
            full_url = info.get("path")
            row_position = result_table.rowCount()
            result_table.insertRow(row_position)
            result_table.setItem(row_position, 0, QTableWidgetItem(full_url))
            result_table.setItem(row_position, 1, QTableWidgetItem(str(status)))
            result_table.setItem(row_position, 2, QTableWidgetItem(path))



def resetTable(result_table):
    result_table.clearContents()
    result_table.setRowCount(0)
