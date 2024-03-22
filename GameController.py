
from DataStructs import Board, FLOWER_WIDTH, BOARD_WIDTH
from PySide6.QtWidgets import QApplication, QFrame, QGraphicsScene, QGraphicsItem ,QGraphicsView, QPushButton, QLabel, QTextEdit, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPen, QColor
from PySide6.QtCore import Qt, QRectF, QPointF
SCALING_FACTOR = 10.0

class FlowerGraphicItem(QGraphicsItem):
    def __init__(self, flower):
        super().__init__()
        self.type = flower.type
        self.pen = QPen(Qt.GlobalColor.black)

    def boundingRect(self):
        return QRectF(0,0,FLOWER_WIDTH * SCALING_FACTOR, FLOWER_WIDTH * SCALING_FACTOR)


    def paint(self, painter, option, widget = ...):
        painter.setPen(self.pen)
        painter.drawEllipse(-FLOWER_WIDTH * SCALING_FACTOR * 0.5,-FLOWER_WIDTH * SCALING_FACTOR * 0.5,FLOWER_WIDTH * SCALING_FACTOR, FLOWER_WIDTH * SCALING_FACTOR)
        painter.drawText(-FLOWER_WIDTH * SCALING_FACTOR * 0.1,FLOWER_WIDTH * SCALING_FACTOR * 0.1,str(self.type))

class MyScene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.fitems = []
        self.setSceneRect(0,0,BOARD_WIDTH * SCALING_FACTOR, BOARD_WIDTH * SCALING_FACTOR)
        self.addEllipse(0,0,BOARD_WIDTH * SCALING_FACTOR, BOARD_WIDTH * SCALING_FACTOR)

    def Initialize(self, data):
        self.fitems.clear()
        self.clear()
        self.addEllipse(0,0,BOARD_WIDTH * SCALING_FACTOR, BOARD_WIDTH * SCALING_FACTOR)
        for flower in data:
            fitem = FlowerGraphicItem(flower)
            fitem.setPos(flower.pos[0] * SCALING_FACTOR, flower.pos[1] * SCALING_FACTOR)
            self.addItem(fitem)
            self.fitems.append(fitem)


class Game(object):
    def __init__(self, scene: MyScene, outputtext):
        super().__init__()
        self.board = Board()
        self.scene = scene
        self.outputtext = outputtext

    def Output(self, text):
        if self.outputtext:
            self.outputtext.append("\n%s" % str(text))

    def Restart(self):
        self.Output("Restart!")
        self.board.Initiate()
        self.scene.Initialize(self.board.GetPoolData())

    def NextMove(self):
        self.Output("NextMove!")

    def DoMath(self):
        self.Output("Calculating!")


