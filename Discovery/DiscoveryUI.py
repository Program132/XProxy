from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTableWidget, \
    QTableWidgetItem, QHBoxLayout, QSizePolicy
from Discovery import DiscoveryLib as Lib
from Discovery.DiscoveryLib import validate_rate_input


def createDiscoveryPage(application):
    page = QWidget()
    layout = QVBoxLayout()

    url_layout = QHBoxLayout()
    url_label = QLabel("URL:")
    url_input = QLineEdit()
    url_label.setFixedWidth(100)
    url_layout.addWidget(url_label)
    url_layout.addWidget(url_input)

    wordlist_layout = QHBoxLayout()
    wordlist_label = QLabel("Wordlist Path:")
    wordlist_input = QLineEdit()
    wordlist_browse_button = QPushButton("Search")
    wordlist_browse_button.clicked.connect(lambda: browseFile(application, wordlist_input))
    wordlist_label.setFixedWidth(100)
    wordlist_layout.addWidget(wordlist_label)
    wordlist_layout.addWidget(wordlist_input)
    wordlist_layout.addWidget(wordlist_browse_button)

    extensions_layout = QHBoxLayout()
    extensions_label = QLabel("Extensions:")
    extensions_input = QLineEdit()
    extensions_label.setFixedWidth(100)
    extensions_layout.addWidget(extensions_label)
    extensions_layout.addWidget(extensions_input)

    rate_layout = QHBoxLayout()
    rate_label = QLabel("Rate Limit (req/s):")
    rate_input = QLineEdit("10")
    rate_label.setFixedWidth(100)
    rate_layout.addWidget(rate_label)
    rate_layout.addWidget(rate_input)

    buttons_layout = QHBoxLayout()
    run_button = QPushButton("Start Discovery")
    rate = validate_rate_input(rate_input.text())
    run_button.clicked.connect(
        lambda: runDiscovery(
            url_input.text(),
            wordlist_input.text(),
            extensions_input.text(),
            result_table,
            rate
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
    layout.addLayout(buttons_layout)
    layout.addWidget(result_table)

    layout.setStretchFactor(result_table, 1)

    page.setLayout(layout)
    return page


def browseFile(application, input_field):
    file_path, _ = QFileDialog.getOpenFileName(application, "Select a file", "", "All files (*)")
    if file_path:
        input_field.setText(file_path)


import time

import time

def runDiscovery(url, wordlist_path, extensions, result_table, rate_limit=None):
    """
    Lance la découverte avec ou sans limite de requêtes par seconde.
    :param url: URL de base
    :param wordlist_path: Chemin vers le fichier wordlist
    :param extensions: Extensions à tester
    :param result_table: Tableau pour afficher les résultats
    :param rate_limit: Limite de requêtes par seconde (None pour désactiver la limite)
    """
    resetTable(result_table)

    def should_sleep():
        """Vérifie si une pause est nécessaire."""
        return rate_limit and rate_limit > 0

    if len(url) != 0 and len(wordlist_path) != 0:
        directories = Lib.run_folder_fuzzer(url, wordlist_path)
        for path, info in directories.items():
            status = info.get("status_code")
            full_url = info.get("path")
            row_position = result_table.rowCount()
            result_table.insertRow(row_position)
            result_table.setItem(row_position, 0, QTableWidgetItem(full_url))
            result_table.setItem(row_position, 1, QTableWidgetItem(str(status)))
            result_table.setItem(row_position, 2, QTableWidgetItem(path))
            if should_sleep():
                time.sleep(1 / rate_limit)

    if len(url) != 0 and len(wordlist_path) != 0 and len(extensions) != 0:
        files = Lib.run_files_fuzzer(url, wordlist_path, extensions.split(","))
        for path, info in files.items():
            status = info.get("status_code")
            full_url = info.get("path")
            row_position = result_table.rowCount()
            result_table.insertRow(row_position)
            result_table.setItem(row_position, 0, QTableWidgetItem(full_url))
            result_table.setItem(row_position, 1, QTableWidgetItem(str(status)))
            result_table.setItem(row_position, 2, QTableWidgetItem(path))
            if should_sleep():
                time.sleep(1 / rate_limit)



def resetTable(result_table):
    result_table.clearContents()
    result_table.setRowCount(0)
