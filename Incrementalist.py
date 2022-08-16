from Gatekeeper import GateKeeper as GateKeeper
from Location import Location as Location
from Location import CENTER as CENTER
from Location import HORIZONTAL as HORIZONTAL
from Location import VERTICAL as VERTICAL
from PlayWord import PlayWord as PlayWord
from ExchangeTiles import ExchangeTiles as ExchangeTiles


class Incrementalist(object):
    # When exchanging, always exchange everything.
    ALL_TILES = {True, True, True, True, True, True, True}

    # The GateKeeper through which this Incrementalist accesses the Board.

    def __init__(self, board):
        self.board = board
        self.gateKeeper = GateKeeper(self.board)

    # This is necessary for the first turn, as one-letter words are not allowed. */
    def findTwoTileMove(self):
        hand = self.gateKeeper.getHand()
        bestWord = ''
        bestScore = -1
        for i in range(0, len(hand) - 1):
            for j in range(0, len(hand) - 1):
                if i != j:
                    a = hand[i]
                    if a == '_':
                        a = 'E'  # This could be improved slightly by trying all possibilities for the blank
                    b = hand[j]
                    if b == '_':
                        b = 'E'  # This could be improved slightly by trying all possibilities for the blank
                    word = "" + a + b
                    if not self.gateKeeper.verifyLegality():
                        continue  # It wasn't legal; go on to the next one
                    local_score = self.gateKeeper.score(word, CENTER, HORIZONTAL)
                    if local_score > bestScore:
                        bestScore = local_score
                        bestWord = word
        if bestScore > -1:
            return PlayWord(bestWord, CENTER, HORIZONTAL, self.board)
        return ExchangeTiles()

    #
    # Technically this tries to make a two-letter word by playing one tile; it won't find words that simply add a
    # tile to the end of an existing word.
    #
    def findOneTileMove(self):
        hand = self.gateKeeper.getHand()
        bestMove = None
        bestScore = -1
        for i in range(0, len(hand) - 1):
            c = hand[i]
            if c == '_':
                c = 'E'  # This could be improved slightly by trying all possibilities for the blank
            for word in {c + " ", " " + c}:
                for row in range(0, self.board.WIDTH):
                    for col in range(0, self.board.WIDTH - 1):
                        location = Location(row, col)
                        for direction in {HORIZONTAL, VERTICAL}:
                            if not self.gateKeeper.verifyLegality():
                                continue
                            local_score = self.gateKeeper.score(word, location, direction)
                            if local_score > bestScore:
                                bestScore = local_score
                                bestMove = PlayWord(word, location, direction, self.board)

        if bestMove:
            return bestMove
        return ExchangeTiles()

    def chooseMove(self):
        if self.gateKeeper.getSquare(CENTER) == self.board.DOUBLE_WORD_SCORE:
            return self.findTwoTileMove()
        return self.findOneTileMove()
