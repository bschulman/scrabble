class GateKeeper(object):

    #
    # board is the associated Board.
    # player is the ScrabbleAI's player number (0 or 1).
    #
    def __init__(self, board):
        self.board = board

    # The ScrabbleAI's player number (0)
    player = 0

    #
    # Returns the square at location.
    #
    #
    #
    def getSquare(self, location):
        return self.board.getSquare(location)

    def verifyLegality(self):
        return self.verifyLegality()

    # Returns the score for playing word at location in direction. Assumes this is a legal play.
    def score(self, word, location, direction):
        return self.board.score(self.board, word, location, direction)

    # Returns a copy of the ScrabbleAI's hand.
    def getHand(self):
        return self.board.getHand()

    def str(self):
        return self.board.str()
