# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PySide6.QtWidgets import QApplication, QFrame, QGraphicsScene, QGraphicsView, QPushButton, QLabel, QTextEdit, QHBoxLayout, QVBoxLayout
import sys
BOARD_WIDTH = 60
TOKEN_WIDTH = 2

class MainWindow(QFrame):
    def __init__(self):
        super().__init__()
        self._setupUI()

    def _setupUI(self):
        self.setWindowTitle("Lacuna")
        layout = QHBoxLayout()
        leftlayout = QVBoxLayout()

        self.setLayout(layout)
        layout.addLayout(leftlayout)

        self.view = QGraphicsView()
        self.view.setFixedSize(600, 600)
        layout.addWidget(self.view)

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.resetBtn = QPushButton("Restart")
        self.calcBtn = QPushButton("DoMath")
        self.infoPanel = QTextEdit()
        self.changemoveBtn = QPushButton("Change Move")

        leftlayout.addWidget(self.infoPanel)
        leftlayout.addWidget(self.resetBtn)
        leftlayout.addWidget(self.calcBtn)
        leftlayout.addWidget(self.changemoveBtn)

def main():
    # Use a breakpoint in the code line below to debug your script.
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()


    app.exec_()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
