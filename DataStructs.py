import random
import math

SUMTOKEN = 6
FLOWER_TYPES = 7
FLOWER_COUNT = 7
BOARD_WIDTH = 60
TOKEN_WIDTH = 1
FLOWER_WIDTH = 2

class PlayerInfo(object):

    def __init__(self):
        super().__init__()
        self.tokensleft = SUMTOKEN
        self.scoreboard = []
        for i in range(FLOWER_TYPES):
            self.scoreboard.append(0)

    def ToString(self):
        return "Tokens left: %s \n scoring: %s\n" % (self.tokensleft, str(self.scoreboard))

class Token:
    def __init__(self, pos, itype):
        self.pos = pos
        self.type = itype

class Flower:
    def __init__(self, pos, itype):
        self.pos = pos
        self.type = itype

class Pool(object):

    def __init__(self):
        super().__init__()
        self.data = []
        self.tokendata = []

    def TryAddToken(self, x, y, ttype):
        if self.IsConflict(x, y, TOKEN_WIDTH):
            return False
        else:
            self.tokendata.append(Token([x,y], ttype))
            return True

    def GetTokenData(self):
        return self.tokendata

    def GetData(self):
        return self.data

    def IsConflict(self, x, y, width=FLOWER_WIDTH):
        if x == 0 == y:
            return True
        if math.dist((x, y) , (BOARD_WIDTH / 2, BOARD_WIDTH / 2)) >= BOARD_WIDTH / 2:
            return True
        for flower in self.data:
            if math.dist((x,y), flower.pos) < FLOWER_WIDTH * 0.5 + width * 0.5:
                return True
        for token in self.tokendata:
            if math.dist((x,y), token.pos) < TOKEN_WIDTH * 0.5 + width * 0.5:
                return True
        return False

    def Serve(self):
        for i in range(FLOWER_TYPES):
            for j in range(FLOWER_COUNT):
                x = 0
                y = 0
                while self.IsConflict(x, y):
                    x = random.randrange(BOARD_WIDTH)
                    y = random.randrange(BOARD_WIDTH)

                self.data.append(Flower([x, y], i))




class Board(object):
    def __init__(self):
        super().__init__()
        self._Initiate()

    def Initiate(self):
        self._Initiate()

    def _Initiate(self):
        self.playerinfos = [PlayerInfo(), PlayerInfo()]
        self.pool = Pool()
        self.pool.Serve()

    def UpdateScoreByTake(self, flowertype, playerindex):
        info = self.playerinfos[playerindex]
        info.tokensleft -= 1
        info.scoreboard[flowertype] += 2

    def TakeOutFlowers(self, index1, index2, playerindex):
        item1 = self.pool.data[index1]
        item2 = self.pool.data[index2]
        self.pool.data.remove(item1)
        self.pool.data.remove(item2)

        self.UpdateScoreByTake(item1.type, playerindex)

    def GetTokenData(self):
        return self.pool.GetTokenData()

    def GetPoolData(self):
        return self.pool.GetData()

    def GetScoreData(self):
        return "Player1:\n%s \nPlayer2:\n%s\n" % (self.playerinfos[0].ToString(), self.playerinfos[1].ToString())