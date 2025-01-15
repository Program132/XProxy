import json
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QPushButton, QWidget, QHBoxLayout, \
    QSizePolicy, QStackedWidget, QLabel, QVBoxLayout, QInputDialog, QFileDialog, QLineEdit, QMessageBox, QTableWidget, \
    QCheckBox
import Discovery.DiscoveryUI as DiscoveryUI


class XProxy(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("XProxy")
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(800, 600)

        self.filesMenu = None
        self.creationFilesMenu()

        self.toolBar = None
        self.creationToolBar()

        self.mainContainer = None
        self.creationMainContainer()

    def creationFilesMenu(self):
        self.filesMenu = self.menuBar().addMenu("File")

        createSession_Action: QAction = QAction("New Session", self)
        createSession_Action.triggered.connect(self.fileMenu_createSession)

        openSession_Action: QAction = QAction("Open a Session", self)
        openSession_Action.triggered.connect(self.fileMenu_openSession)

        saveSession_Action: QAction = QAction("Save", self)
        saveSession_Action.triggered.connect(self.fileMenu_saveSession)

        saveAsSession_Action: QAction = QAction("Save as...", self)
        saveAsSession_Action.triggered.connect(self.fileMenu_saveAsSession)

        self.filesMenu.addAction(createSession_Action)
        self.filesMenu.addAction(openSession_Action)
        self.filesMenu.addAction(saveSession_Action)
        self.filesMenu.addAction(saveAsSession_Action)

    def fileMenu_createSession(self):
        print("Create new session")

        session_name, ok = QInputDialog.getText(self, "New Session", "Enter the name of the session:")
        if ok and session_name.strip():
            self.current_session_name = session_name.strip()

            file_path, _ = QFileDialog.getSaveFileName(self, "Save Session", "", "JSON Files (*.json)")
            if file_path:
                self.current_session_file = file_path
                self.current_session_data = {}

                self.saveSession()

                QMessageBox.information(self, "Session Created",
                                        f"Session '{self.current_session_name}' created and saved to {self.current_session_file}!")
            else:
                QMessageBox.warning(self, "Invalid File", "No file selected. Session creation cancelled.")
        else:
            QMessageBox.warning(self, "Invalid Name", "Session name cannot be empty.")

    def fileMenu_saveSession(self):
        print("Save current session")

    def fileMenu_saveAsSession(self):
        print("Save as a new file the current session")

    def fileMenu_openSession(self):
        print("Open a saved session")


    def creationToolBar(self):
        toolbar = QToolBar("Tools", self)
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(0)

        buttons = ["Intercepter", "Repeater", "Fuzzer", "Discovery"]

        for index, btn_text in enumerate(buttons):
            button = QPushButton(btn_text)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            toolbar_layout.addWidget(button)
            button.clicked.connect(lambda _, idx=index: self.changeContainerPage(idx))

        toolbar.addWidget(toolbar_widget)

    def creationMainContainer(self):
        self.mainContainer = QStackedWidget()
        self.setCentralWidget(self.mainContainer)

        self.mainContainer.addWidget(self.createIntercepterPage())  # Index 0
        self.mainContainer.addWidget(self.createRepeaterPage())  # Index 1
        self.mainContainer.addWidget(self.createFuzzerPage())  # Index 2
        self.mainContainer.addWidget(DiscoveryUI.createDiscoveryPage(self))  # Index 3

    def changeContainerPage(self, index):
        self.mainContainer.setCurrentIndex(index)

    def createIntercepterPage(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Interface pour l'Intercepter"))
        page.setLayout(layout)
        return page

    def createRepeaterPage(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Interface pour le Repeater"))
        page.setLayout(layout)
        return page

    def createFuzzerPage(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Interface pour le Fuzzer"))
        page.setLayout(layout)
        return page

    def collect_discovery_data(self):
        discovery_page = self.mainContainer.widget(3)
        url_input = discovery_page.findChild(QLineEdit, "url_input")
        wordlist_input = discovery_page.findChild(QLineEdit, "wordlist_input")
        extensions_input = discovery_page.findChild(QLineEdit, "extensions_input")
        rate_checkbox = discovery_page.findChild(QCheckBox, "rate_checkbox")
        rate_input = discovery_page.findChild(QLineEdit, "rate_input")
        headers_input = discovery_page.findChild(QLineEdit, "headers_input")
        threads_input = discovery_page.findChild(QLineEdit, "threads_input")

        result_table = discovery_page.findChild(QTableWidget, "result_table")
        results = []
        for row in range(result_table.rowCount()):
            path = result_table.item(row, 0).text()
            status_code = result_table.item(row, 1).text()
            file_name = result_table.item(row, 2).text()
            results.append({"path": path, "status_code": status_code, "file_name": file_name})

        return {
            "url": url_input.text(),
            "wordlist_path": wordlist_input.text(),
            "extensions": extensions_input.text(),
            "headers": headers_input.text(),
            "threads": threads_input.text(),
            "rate_limit": float(rate_input.text()) if rate_checkbox.isChecked() else None,
            "results": results
        }

    def saveSession(self):
        discovery_data = self.collect_discovery_data()

        session_data = {
            "session_name": self.current_session_name,
            "discovery": discovery_data
        }

        try:
            with open(self.current_session_file, 'w') as json_file:
                json.dump(session_data, json_file, indent=4)
            QMessageBox.information(self, "Session Saved",
                                    f"Session saved successfully to {self.current_session_file}!")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Error saving session: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XProxy()
    window.show()
    sys.exit(app.exec_())