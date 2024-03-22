# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PySide6.QtWidgets import QApplication, QFrame, QGraphicsScene, QGraphicsView, QPushButton, QLabel, QTextEdit, QHBoxLayout, QVBoxLayout
import sys
from GameController import Game, MyScene, BOARD_WIDTH
from PySide6.QtCore import Qt, QRectF
import random

class MainWindow(QFrame):
    def __init__(self):
        super().__init__()
        self._setupUI()
        random.seed(0)

        self.game = Game(self.scene, self.infoPanel)

        self.calcBtn.clicked.connect(self.game.DoMath)
        self.resetBtn.clicked.connect(self.game.Restart)
        self.nextmoveBtn.clicked.connect(self.game.NextMove)
        self.aimoveBtn.clicked.connect(self.game.AIMove)

        self.clearBtn.clicked.connect(self.ClearInfo)

    def ClearInfo(self):
        self.infoPanel.clear()

    def _setupUI(self):
        self.setWindowTitle("Lacuna")
        layout = QHBoxLayout()
        leftlayout = QVBoxLayout()

        self.setLayout(layout)
        layout.addLayout(leftlayout)

        self.view = QGraphicsView()
        self.view.setFixedSize(600, 600)
        layout.addWidget(self.view)

        self.scene = MyScene()
        self.view.setScene(self.scene)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.resetBtn = QPushButton("Restart")
        self.calcBtn = QPushButton("DoMath")
        self.infoPanel = QTextEdit()
        self.nextmoveBtn = QPushButton("Next Move")
        self.aimoveBtn = QPushButton("AI Move")
        self.clearBtn = QPushButton("Clear")

        leftlayout.addWidget(self.infoPanel)
        leftlayout.addWidget(self.resetBtn)
        leftlayout.addWidget(self.calcBtn)
        leftlayout.addWidget(self.aimoveBtn)
        leftlayout.addWidget(self.nextmoveBtn)
        leftlayout.addWidget(self.clearBtn)

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
