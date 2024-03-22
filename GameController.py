import numpy as np
from DataStructs import Board, FLOWER_WIDTH, BOARD_WIDTH, TOKEN_WIDTH, FLOWER_COUNT, FLOWER_TYPES
from PySide6.QtWidgets import QApplication, QFrame, QGraphicsScene, QGraphicsItem ,QGraphicsView, QPushButton, QLabel, QTextEdit, QHBoxLayout, QVBoxLayout
from PySide6.QtGui import QPen, QColor, QBrush
from PySide6.QtCore import Qt, QRectF, QPointF, Signal
SCALING_FACTOR = 10.0


class TokenGraphicItem(QGraphicsItem):
    def __init__(self, ttype):
        super().__init__()
        self.ttype = ttype
        if ttype == 0:
            # gold
            self.brush = QBrush(QColor(255,206,13))
        else:
            self.brush = QBrush(QColor(230,230,230))
        self.pen = QPen(Qt.GlobalColor.white)


    def boundingRect(self):
        return QRectF(-TOKEN_WIDTH * SCALING_FACTOR * 0.5,-TOKEN_WIDTH * SCALING_FACTOR * 0.5,TOKEN_WIDTH * SCALING_FACTOR, TOKEN_WIDTH * SCALING_FACTOR)


    def paint(self, painter, option, widget = ...):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)
        painter.drawEllipse(-TOKEN_WIDTH * SCALING_FACTOR * 0.5,-TOKEN_WIDTH * SCALING_FACTOR * 0.5,TOKEN_WIDTH * SCALING_FACTOR, TOKEN_WIDTH * SCALING_FACTOR)


class FlowerGraphicItem(QGraphicsItem):
    def __init__(self, flower):
        super().__init__()
        self.type = flower.type
        self.pos = flower.pos
        self.pen = QPen(Qt.GlobalColor.black)

    def boundingRect(self):
        return QRectF(-FLOWER_WIDTH * SCALING_FACTOR * 0.5,-FLOWER_WIDTH * SCALING_FACTOR * 0.5,FLOWER_WIDTH * SCALING_FACTOR, FLOWER_WIDTH * SCALING_FACTOR)


    def paint(self, painter, option, widget = ...):
        painter.setPen(self.pen)
        painter.drawEllipse(-FLOWER_WIDTH * SCALING_FACTOR * 0.5,-FLOWER_WIDTH * SCALING_FACTOR * 0.5,FLOWER_WIDTH * SCALING_FACTOR, FLOWER_WIDTH * SCALING_FACTOR)
        painter.drawText(-FLOWER_WIDTH * SCALING_FACTOR * 0.1,FLOWER_WIDTH * SCALING_FACTOR * 0.1,str(self.type))
        painter.drawText(FLOWER_WIDTH * SCALING_FACTOR * 0.5,FLOWER_WIDTH * SCALING_FACTOR * 0.1,str(self.pos))
class MyScene(QGraphicsScene):
    Signal_Click = Signal(float, float)
    def __init__(self):
        super().__init__()
        self.fitems = []
        self.titems = []
        self.setSceneRect(0,0,BOARD_WIDTH * SCALING_FACTOR, BOARD_WIDTH * SCALING_FACTOR)
        self.addEllipse(0,0,BOARD_WIDTH * SCALING_FACTOR, BOARD_WIDTH * SCALING_FACTOR)
        self.linepen = QPen(QColor(100,100,100))
        self.linepen.setStyle(Qt.PenStyle.DotLine)

    def AddLines(self, data):
        for line in data:
            self.addLine(line[0][0]* SCALING_FACTOR,line[0][1]* SCALING_FACTOR,line[1][0]* SCALING_FACTOR,line[1][1]* SCALING_FACTOR, self.linepen)

    def mousePressEvent(self, event):
        self.Signal_Click.emit(event.scenePos().x() / SCALING_FACTOR, event.scenePos().y() / SCALING_FACTOR)

    def Initialize(self, data):
        self.fitems.clear()
        self.titems.clear()
        self.clear()
        self.addEllipse(0,0,BOARD_WIDTH * SCALING_FACTOR, BOARD_WIDTH * SCALING_FACTOR)
        for flower in data:
            fitem = FlowerGraphicItem(flower)
            fitem.setPos(flower.pos[0] * SCALING_FACTOR, flower.pos[1] * SCALING_FACTOR)
            self.addItem(fitem)
            self.fitems.append(fitem)


    def PutToken(self, ttype, pos):
        titem = TokenGraphicItem(ttype)
        titem.setPos(pos[0] * SCALING_FACTOR, pos[1] * SCALING_FACTOR)
        self.addItem(titem)
        self.titems.append(titem)


class Game(object):
    def __init__(self, scene: MyScene, outputtext):
        super().__init__()
        self.board = Board()
        self.validlines = []
        self.currentturn = 0
        self.scene = scene
        self.outputtext = outputtext
        self.scene.Signal_Click.connect(self.OnClick)

    def OnClick(self, x, y):
        success = self.board.pool.TryAddToken(x, y, self.currentturn)
        if success:
            self.scene.PutToken(self.currentturn, (x, y))

    def Output(self, text):
        if self.outputtext:
            self.outputtext.append("\n%s" % str(text))

    def Restart(self):
        self.Output("Restart!")
        self.validlines.clear()
        self.board.Initiate()
        self.scene.Initialize(self.board.GetPoolData())

    def NextMove(self):
        self.Output("NextMove!")
        self.currentturn = 1 - self.currentturn

    def AIMove(self):
        self.Output("AIMove!")

    def DoMath(self):
        self.Output("Calculating!")
        pooldata = self.board.GetPoolData()
        validlines = []
        # find all lines
        for i in range(FLOWER_TYPES):
            for j in range(FLOWER_COUNT):
                index1 = i * FLOWER_COUNT + j
                for k in range(1, FLOWER_COUNT):
                    index2 = i * FLOWER_COUNT + k
                    p1 = np.asarray(pooldata[index1].pos)
                    p2 = np.asarray(pooldata[index2].pos)
                    n12 = np.linalg.norm(p1 - p2)
                    suc = True
                    for pindex, p in enumerate(pooldata):
                        if pindex == index1 or pindex == index2:
                            continue
                        p3 = np.asarray(p.pos)
                        if np.dot(p2-p1, p3-p1) <= 0:
                            continue
                        if np.dot(p1-p2, p3-p2) <= 0:
                            continue
                        d = np.abs(np.linalg.norm(np.cross(p2-p1, p1-p3)) / n12)
                        if d < FLOWER_WIDTH * 0.5:
                            suc = False
                            break
                    if suc:
                        validlines.append((pooldata[index1].pos, pooldata[index2].pos))

        self.validlines = validlines
        self.Output("Mathdone! %d" % len(validlines))
        self.scene.AddLines(self.validlines)

