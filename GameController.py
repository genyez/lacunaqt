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
        self.lines = []
        self.setSceneRect(0,0,BOARD_WIDTH * SCALING_FACTOR, BOARD_WIDTH * SCALING_FACTOR)
        self.addEllipse(0,0,BOARD_WIDTH * SCALING_FACTOR, BOARD_WIDTH * SCALING_FACTOR)
        self.linepen = QPen(QColor(100,100,100))
        self.linepen.setStyle(Qt.PenStyle.DotLine)

    def ClearLines(self):
        for line in self.lines:
            self.removeItem(line)
        self.lines.clear()

    def AddLines(self, data):
        for line in data:
            line = self.addLine(line[0][0]* SCALING_FACTOR,line[0][1]* SCALING_FACTOR,line[1][0]* SCALING_FACTOR,line[1][1]* SCALING_FACTOR, self.linepen)
            self.lines.append(line)
    def mousePressEvent(self, event):
        self.Signal_Click.emit(event.scenePos().x() / SCALING_FACTOR, event.scenePos().y() / SCALING_FACTOR)

    def RefreshFlowers(self, data):
        for item in self.fitems:
            self.removeItem(item)
        self.fitems.clear()
        for flower in data:
            fitem = FlowerGraphicItem(flower)
            fitem.setPos(flower.pos[0] * SCALING_FACTOR, flower.pos[1] * SCALING_FACTOR)
            self.addItem(fitem)
            self.fitems.append(fitem)

    def Initialize(self, data):
        self.titems.clear()
        self.clear()
        self.addEllipse(0,0,BOARD_WIDTH * SCALING_FACTOR, BOARD_WIDTH * SCALING_FACTOR)
        self.RefreshFlowers(data)



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

    def point2linedis(self, p1, p2, p3):
        if np.dot(p2 - p1, p3 - p1) <= 0:
            return False
        if np.dot(p1 - p2, p3 - p2) <= 0:
            return False
        return np.abs(np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p1 - p2))

    def pointdis(self, p1, p2):
        p1 = np.asarray(p1)
        p2 = np.asarray(p2)
        return np.linalg.norm(p2 - p1)

    def OnClick(self, x, y):
        # get nearest pos in valid lines to put token
        mindis = 9999
        minline = None
        p3 = np.asarray((x, y))
        for line in self.validlines:
            dis = self.point2linedis(np.asarray(line[0]), np.asarray(line[1]), p3)
            if dis is not False:
                if dis < mindis:
                    minline = line
                    mindis = dis
        p1 = np.asarray(minline[0])
        p2 = np.asarray(minline[1])
        n = (p2-p1) / np.linalg.norm(p2-p1,2)
        targetpos = p1 + n*np.dot(p3-p1,n)

        success = self.board.pool.TryAddToken(targetpos[0], targetpos[1], self.currentturn)
        if success:
            self.board.TakeOutFlowers(minline[2], minline[3], self.currentturn)
            self.scene.RefreshFlowers(self.board.GetPoolData())
            self.scene.PutToken(self.currentturn, (targetpos[0], targetpos[1]))

            self.Output(self.board.GetScoreData())

            finished = self.FinishUp()

            self.DoMath()
            if not finished:
                self.NextMove()

    def Output(self, text):
        if self.outputtext:
            self.outputtext.append("\n%s" % str(text))

    def Restart(self):
        self.Output("Restart!")
        self.validlines.clear()
        self.board.Initiate()
        self.scene.Initialize(self.board.GetPoolData())

    def NextMove(self):
        self.currentturn = 1 - self.currentturn
        self.Output("Now is Player%d's turn" % (self.currentturn+1))

    def AIMove(self):
        self.Output("AIMove!")

    def FinishUp(self):
        # not finished yet
        if self.board.playerinfos[0].tokensleft > 0 or self.board.playerinfos[1].tokensleft > 0:
            # self.Output("We are not finished yet!")
            return False
        pooldata = self.board.GetPoolData()
        tokendata = self.board.GetTokenData()
        for flower in pooldata:
            mindis = 9999
            belongsto = -1
            for token in tokendata:
                dis = self.pointdis(token.pos, flower.pos)
                if dis < mindis:
                    mindis = dis
                    belongsto = token.type
            self.board.playerinfos[belongsto].Scoring(flower.type)

        self.Output(self.board.GetScoreData())
        if self.board.playerinfos[0].IsWon():
            wonid = 1
        else:
            wonid = 2
        self.Output("Player %d Wins!" % wonid)
        return True

    def DoMath(self):
        self.scene.invalidate()
        self.scene.ClearLines()

        # self.Output("Calculating!")
        pooldata = self.board.GetPoolData()
        tokendata = self.board.GetTokenData()
        validlines = []
        # find all lines
        for i in range(len(pooldata)):
            for j in range(i + 1, len(pooldata)):
                index1 = i
                index2 = j
                if pooldata[index1].type != pooldata[index2].type:
                    break
                p1 = np.asarray(pooldata[index1].pos)
                p2 = np.asarray(pooldata[index2].pos)
                n12 = np.linalg.norm(p1 - p2)
                suc = True
                def _lacunain(datas, r):
                    nonlocal suc
                    for pindex, p in enumerate(datas):
                        if pindex == index1 or pindex == index2:
                            continue
                        p3 = np.asarray(p.pos)
                        if np.dot(p2 - p1, p3 - p1) <= 0:
                            continue
                        if np.dot(p1 - p2, p3 - p2) <= 0:
                            continue
                        d = np.abs(np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / n12)
                        if d < r:
                            suc = False
                            break
                # tokens lacuna
                _lacunain(tokendata, TOKEN_WIDTH*0.5)
                # flowers lacuna
                _lacunain(pooldata, FLOWER_WIDTH * 0.5)
                if suc:
                    validlines.append((pooldata[index1].pos, pooldata[index2].pos, index1, index2))

        self.validlines = validlines
        # self.Output("Mathdone! %d" % len(validlines))
        self.scene.AddLines(self.validlines)

