#########################
# Board.py
# 
# For shapes/pieces
########################

class Board(object):
        
    _board = 0b0000000000000000
    
    def __init__(self):
        self._board = 0b0000000000000000
    
    def setBoard(self, boardVal):
        self._board = boardVal
        
    def getBoard(self):
        return self._board 