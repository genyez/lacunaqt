import random
import math
import copy

SUMTOKEN = 6
FLOWER_TYPES = 7
FLOWER_COUNT = 7
BOARD_WIDTH = 60
TOKEN_WIDTH = 1
FLOWER_WIDTH = 2
SCORE_TO_WIN = 4
SCORETYPES_TO_WIN = 4

class PlayerInfo(object):

    def __init__(self):
        super().__init__()
        self.tokensleft = SUMTOKEN
        self.scoreboard = []
        for i in range(FLOWER_TYPES):
            self.scoreboard.append(0)

    def Clone(self):
        info = PlayerInfo()
        info.tokensleft = self.tokensleft
        info.scoreboard = copy.deepcopy(self.scoreboard)
        return info

    def Scoring(self, flowertype, count=1):
        self.scoreboard[flowertype] += count

    def IsWon(self):
        scoring_type_count = 0
        for score in self.scoreboard:
            if score >= SCORE_TO_WIN:
                scoring_type_count += 1
        if scoring_type_count >= SCORETYPES_TO_WIN:
            return True
        else:
            return False

    def ToString(self):
        return "Tokens left: %s \n scoring: %s\n" % (self.tokensleft, str(self.scoreboard))

class Token:
    def __init__(self, pos, itype):
        self.pos = pos
        self.type = itype

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

class Flower:
    def __init__(self, pos, itype):
        self.pos = pos
        self.type = itype

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

class Pool(object):

    def __init__(self):
        super().__init__()
        self.data = []
        self.tokendata = []

    def Clone(self):
        pool = Pool()
        pool.data = copy.deepcopy(self.data)
        pool.tokendata = copy.deepcopy(self.data)
        return pool

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

    def Clone(self):
        b = Board()
        b.playerinfos = [self.playerinfos[0].Clone(), self.playerinfos[1].Clone()]
        b.pool = self.pool.Clone()
        return b

    def Initiate(self):
        self._Initiate(True)

    def _Initiate(self, serve=False):
        self.playerinfos = [PlayerInfo(), PlayerInfo()]
        self.pool = Pool()
        if serve:
            self.pool.Serve()

    def UpdateScoreByTake(self, flowertype, playerindex):
        info = self.playerinfos[playerindex]
        info.tokensleft -= 1
        info.Scoring(flowertype, 2)

    def CurrentRole(self):
        if self.playerinfos[0].tokensleft < self.playerinfos[1].tokensleft:
            return 1
        else:
            return 0

    def TakeMove(self, pos, line):
        role = self.CurrentRole()
        success = self.pool.TryAddToken(pos[0], pos[1], role)
        if success:
            self.TakeOutFlowers(line[2], line[3], role)
        return success

    def SuccessCheck(self):
        if self.playerinfos[0].tokensleft == self.playerinfos[1].tokensleft == 0:
            if self.playerinfos[0].IsWon():
                return 0
            else:
                return 1
        else:
            return False

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