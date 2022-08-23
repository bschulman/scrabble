import ExchangeTiles
import Location
import PlayWord
from Gatekeeper import GateKeeper


class MyScrabblePlayer(object):
    ALL_TILES = [True, True, True, True, True, True, True]

    def __init__(self, board):
        self.board = board
        self.gate = GateKeeper(board)

    # considers every permutation of letters in the current hand and plays the best word on the best spot on the
    # board that also hits the center tile this could be improved by only considering the center cross on the board
    # as possible plays rather than every location on the board and returns the best possible move
    #
    def findFirstMove(self):
        hand = self.gate.getHand()
        bestMove = list((None, None, None, None, None, None, None))
        for i in (0, 6, 1):
            bestMove[i] = PlayWord.PlayWord('', Location.Location(0, 0), Location.VERTICAL, self.board)
        bestScore = [] * 7
        for i in (0, 6, 1):
            # initialize the arrays
            bestScore[i] = -1
            # needs a 7 nested for loop to consider every possible permutation of letters
        for p in range(0, len(hand), 1):
            for q in range(0, len(hand), 1):
                for m in range(0, len(hand), 1):
                    for n in range(0, len(hand), 1):
                        for i in range(0, len(hand), 1):
                            for j in range(0, len(hand), 1):
                                for k in range(0, len(hand), 1):
                                    # checks to make sure we don't try and use the same tiles from our hand at the
                                    # same time
                                    if p != q and p != m and p != n and p != i and p != j and p != k and q != m \
                                            and q != n and q != i and q != j and q != k and m != n and m != i \
                                            and m != j and m != k and n != i and n != j and n != k and i != j \
                                            and i != k and j != k:
                                        a = hand[p]
                                        if a == '_':
                                            a = 'E'  # This could be improved slightly by trying all possibilities
                                            # for the blank
                                        b = hand[q]
                                        if b == '_':
                                            b = 'E'  # This could be improved slightly by trying all possibilities
                                            # for the blank
                                        c = hand[m]
                                        if c == '_':
                                            c = 'E'  # This could be improved slightly by trying all possibilities
                                            # for the blank
                                        d = hand[n]
                                        if d == '_':
                                            d = 'E'
                                        f = hand[i]
                                        if f == '_':
                                            f = 'E'
                                        g = hand[j]
                                        if g == '_':
                                            g = 'E'
                                        h = hand[k]
                                        if h == '_':
                                            h = 'E'
                                        # creates possible word strings
                                        words = [''] * 6
                                        words[0] = "" + a + b
                                        words[1] = "" + a + b + c
                                        words[2] = "" + a + b + c + d
                                        words[3] = "" + a + b + c + d + f
                                        words[4] = "" + a + b + c + d + f + g
                                        words[5] = "" + a + b + c + d + f + g + h
                                        for kk in range(0, 5, 1):
                                            word = words[kk]
                                            for row in range(0, self.board.WIDTH - 1, 1):
                                                for col in range(0, self.board.WIDTH - 1, 1):
                                                    location = Location.Location(row, col)
                                                    for direction in (Location.HORIZONTAL, Location.VERTICAL):
                                                        if self.gate.verifyLegality():
                                                            continue  # if it wasn't legal; go on to the next one
                                                        localscore = self.gate.score(word, location, direction)
                                                        if localscore > bestScore[kk]:
                                                            bestScore[kk] = localscore
                                                            bestMove[kk] = PlayWord.PlayWord(word, location, direction,
                                                                                             self.board)

        best = 0
        index = 0
        for i in range(0, 6):  # finds the best playable word using the scores
            if bestScore[i] > best:
                best = bestScore[i]
                index = i
        if bestMove[index] is not None:
            return bestMove[index]
        return ExchangeTiles.ExchangeTiles()  # in the case that we cannot make a word, which should never be the case

        #
        # finds the best possible move through playing up to 4 tiles on the board
        # cannot play between two columns or rows that have a gap between them that plays across both rows/columns
        # returns the best move
        #

    def findAllMoves(self):
        found = False  # check to see if we need to exchange tiles a.k.a. pass
        hand = self.gate.getHand()
        bestMove = [PlayWord.PlayWord(None, None, None, self.board),
                    PlayWord.PlayWord(None, None, None, self.board),
                    PlayWord.PlayWord(None, None, None, self.board),
                    PlayWord.PlayWord(None, None, None, self.board),
                    PlayWord.PlayWord(None, None, None, self.board)
                    ]
        bestScore = [0] * 5
        for i in range(0, 4):  # initialize the arrays
            bestScore[i] = -1
            bestMove[i] = None

        # creates 4 nested for loops to consider different permutations of playing up to 4 tiles
        for p in range(0, len(hand) - 1):
            for i in range(0, len(hand) - 1):
                for j in range(0, len(hand) - 1):
                    for k in range(0, len(hand) - 1):
                        if p != i and p != j and p != k and i != j and i != k and j != k:
                            # treats every blank tile as the letter e
                            a = hand[p]
                            if a == '_':
                                a = 'E'  # This could be improved slightly by trying all possibilities for the blank
                            b = hand[i]
                            if b == '_':
                                b = 'E'  # This could be improved slightly by trying all possibilities for the blank
                            c = hand[j]
                            if c == '_':
                                c = 'E'  # This could be improved slightly by trying all possibilities for the blank
                            d = hand[k]
                            if d == '_':
                                d = 'E'
                            # creates word strings
                            words = [[''], [''], [''], ['']]
                            words[0] = " " + a, a + " ", "  " + a, "   " + a, a + "  ", a + "   "
                            words[
                                1] = "" + a + b, a + b + " ", a + " " + b, " " + a + b, "  " + a + b, "   " + a + b, \
                                     a + b + "  ", a + b + "   ", a + "  " + b, a + "   " + b
                            words[
                                2] = "" + a + b + c, a + b + c + " ", a + b + " " + c, a + " " + b + c, \
                                     " " + a + b + c, a + b + c + "  ", a + b + c + "   ", a + b + c + "    ", \
                                     a + b + c + "     ", "  " + a + b + c, "   " + a + b + c, "    " + a + b + c, \
                                     "     " + a + b + c
                            words[
                                3] = "" + a + b + c + d, a + b + c + d + " ", a + b + c + " " + d, \
                                     a + b + " " + c + d, a + " " + b + c + d, " " + a + b + c + d, \
                                     "  " + a + b + c + d, "   " + a + b + c + d, "     " + a + b + c + d
                            count = len(hand)
                            if count > 4:
                                count = 4
                                # tries every possible word string on every location
                                for kk in range(0, count):
                                    for word in words[kk]:
                                        for row in range(0, self.board.WIDTH - 1):
                                            for col in range(0, self.board.WIDTH - 1):
                                                location = Location.Location(row, col)
                                                for direction in (Location.HORIZONTAL, Location.VERTICAL):
                                                    if self.gate.verifyLegality():
                                                        continue
                                                    found = True
                                                    score = self.gate.score(word, location, direction)
                                                    if score > bestScore[kk]:
                                                        bestScore[kk] = score
                                                        bestMove[kk] = PlayWord.PlayWord(word, location, direction,
                                                                                         self.board)
        best = 0
        index = 0
        for i in range(0, 3):  # finds the best playable word using the scores
            if bestScore[i] > best:
                best = bestScore[i]
                index = i
        # checks if we have found a word and that our word choice is not null
        if bestMove[index] is not None and found:
            return bestMove[index]
        return ExchangeTiles.ExchangeTiles()

    #
    #
    # returns the best first move or best move in general depending on if the center tile is open
    #
    def findBestMove(self):
        if self.gate.getSquare(Location.CENTER) == self.board.DOUBLE_WORD_SCORE:
            return self.findFirstMove()
        return self.findAllMoves()

    def setGateKeeper(self, gateKeeper):
        self.gate = gateKeeper

    def chooseMove(self):
        return self.findBestMove()
