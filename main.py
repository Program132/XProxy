import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QToolBar, QPushButton, QWidget, QHBoxLayout, \
    QSizePolicy, QStackedWidget, QLabel, QLineEdit, QFileDialog, QVBoxLayout
import Discovery.DiscoveryUI as DiscoveryUI

class XProxy(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("XProxy")
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumSize(600, 400)

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

        saveSession_Action: QAction = QAction("Save", self)
        saveSession_Action.triggered.connect(self.fileMenu_saveSession)

        saveAsSession_Action: QAction = QAction("Save as...", self)
        saveAsSession_Action.triggered.connect(self.fileMenu_saveAsSession)

        openSession_Action: QAction = QAction("Open a Session", self)
        openSession_Action.triggered.connect(self.fileMenu_openSession)

        self.filesMenu.addAction(createSession_Action)
        self.filesMenu.addAction(saveSession_Action)
        self.filesMenu.addAction(saveAsSession_Action)
        self.filesMenu.addAction(openSession_Action)

    def fileMenu_createSession(self):
        print("Create new session")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = XProxy()
    window.show()
    sys.exit(app.exec_())