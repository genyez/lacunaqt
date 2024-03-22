
from DataStructs import Board

class Game(object):
    def __init__(self, scene, outputtext):
        super().__init__()
        self.board = Board()
        self.scene = scene
        self.outputtext = outputtext

    def Output(self, text):
        if self.outputtext:
            self.outputtext.append("\n%s" % str(text))

    def Restart(self):
        self.Output("Restart!")

    def NextMove(self):
        self.Output("NextMove!")

    def DoMath(self):
        self.Output("Calculating!")


