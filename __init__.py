# Scrabble AI player that plays up to 4 tiles per turn other than the first
# Code by Ben Schulman


# Scrabble board, maintaining bag, players' hands, and other game logic.

# General conventions:

# Each square is either a lower-case letter (a regular tile), an upper-case letter (a played blank), or a symbol.

# Each bag/hand tile is either a lower-case letter (a regular tile) or _ (an unplayed blank).

# Words submitted consist of letters (upper-case for played blanks) and spaces (existing tiles on the board).
import random
from typing import List

import StdDraw
# import tkFont
from collections import namedtuple
from Board import Board as Board
from PlayWord import PlayWord as PlayWord
import Location


class Location(object):

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def getRow(self):
        return self.row

    def getColumn(self):
        return self.column

    # Returns a new Location which is offset from this by direction. For example, a.neighbor(HORIZONTAL) is the
    # location to the right of a.
    def neighbor(self):
        return Location(self.row + self.row, self.column + self.column)

    # Returns a new Location which is offset from this by the opposite of direction. For example, a.neighbor(
    # HORIZONTAL) is the location to the left of a.
    def antineighbor(self):
        return Location(self.row - self.row, self.column - self.column)

    # Returns the opposite of this direction. HORIZONTAL and VERTICAL are opposites.
    def opposite(self):
        if self == HORIZONTAL:
            return VERTICAL
        return HORIZONTAL

    # Returns true if this Location is on the board. */
    def isOnBoard(self):
        return 0 <= self.row < 15 and 0 <= self.column < 15

    def equals(self, o):
        if self == o:
            return True
        if o == None or type(self) != type(o):
            return False
        location = Location(o.row, o.column)
        return self.row == location.row and self.column == location.column

    def hashCode(self):
        return [hash(self.row), hash(self.column)]

    def str(self):
        return 'Location{' + 'row=' + self.row + ', column=' + self.column + '}'


# Direction for horizontal words.
HORIZONTAL = Location(0, 1)

# Direction for vertical words.
VERTICAL = Location(1, 0)

# The center square (which the first move must contain).
CENTER = Location(7, 7)

# Log of all keys typed to compare with StdDraw's:
LASTKEYTYPED = []


# # Board object
# class Board(object):
#     # Width of this Board, in squares.
#     WIDTH = 15
#
#     # Symbol for a double letter score square.
#     DOUBLE_LETTER_SCORE = '-'
#
#     # Symbol for a triple letter score square. */
#     TRIPLE_LETTER_SCORE = '='
#
#     # Symbol for a double word score square. */
#     DOUBLE_WORD_SCORE = '+'
#
#     # Symbol for a triple word score square. */
#     TRIPLE_WORD_SCORE = '#'
#
#     # Symbol for a regular square. */
#     NO_PREMIUM = ' '
#
#     # Initial layout of bonus squares.
#     LAYOUT = ['#  -   #   -  #', ' +   =   =   + ', '  +   - -   +  ', '-  +   -   +  -', '    +     +    ',
#               ' =   =   =   = ', '  -   - -   -  ', '#  -   +   -  #', '  -   - -   -  ', ' =   =   =   = ',
#               '    +     +    ', '-  +   -   +  -', '  +   - -   +  ', ' +   =   =   + ', '#  -   #   -  #']
#
#     def __init__(self):
#         # Occupied Squares on the board (whether occupied by tiles or not).
#         # rows, cols = (15, 15)
#         self.numberOfPasses = 0
#         self.squares = [[''] * 15] * 15
#
#         # Set of legal words.
#         self.DICTIONARY = set()
#
#         # Associates tiles with their values.
#         self.TILE_VALUES = dict()
#
#         # Hands of the players.
#         self.hands = [[]] * 2
#
#         # The bag of remaining tiles.
#         self.bag = []
#
#         # Scores of the players.
#         self.scores = [0, 0]
#
#         # Current player number (0 or 1).
#         self.currentPlayer = 0
#
#         # Load dictionary
#         with open('enable1.txt') as n:
#             # print("loaded")
#             for word in n.readlines():
#                 self.DICTIONARY.add(word)
#
#         # Initialize tile values
#         l = 'eaionrtlsu'
#         res = [ord(ele) for sub in l for ele in sub]
#         for c in res:
#             self.TILE_VALUES[c] = 1
#         l = 'dg'
#         res = [ord(ele) for sub in l for ele in sub]
#         for c in res:
#             self.TILE_VALUES[c] = 2
#         l = 'bcmp'
#         res = [ord(ele) for sub in l for ele in sub]
#         for c in res:
#             self.TILE_VALUES[c] = 3
#
#         l = 'fhvwy'
#         res = [ord(ele) for sub in l for ele in sub]
#         for c in res:
#             self.TILE_VALUES[c] = 4
#
#         self.TILE_VALUES[ord('k')] = 5
#
#         l = 'jx'
#         res = [ord(ele) for sub in l for ele in sub]
#         for c in res:
#             self.TILE_VALUES[c] = 8
#
#         l = 'qz'
#         res = [ord(ele) for sub in l for ele in sub]
#         for c in res:
#             self.TILE_VALUES[c] = 10
#
#         for c in range(ord('A'), ord('Z'), 1):
#             self.TILE_VALUES[c] = 0
#
#         self.TILE_VALUES['-'] = 0
#
#         # Number of consecutive tile exchange turns; 2 ends the game.
#         self.squares = self.LAYOUT
#         # for r in range(0, 15, 1):
#         #     for i in range(0, 15, 1):
#         #         self.squares[r][i] = self.LAYOUT[r][i]
#         # Create bag
#         self.bag = list()
#         for tile in list(
#                 'aaaaaaaaabbccddddeeeeeeeeeeeeffggghhiiiiiiiiijkllllmmnnnnnnooooooooppqrrrrrrssssttttttuuuuvvwwxyyz__'):
#             self.bag.append(tile)
#         random.shuffle(self.bag)
#
#     def deal(self):
#         for i in range(0, 6, 1):
#             if 7 == len(self.hands[getCurrentPlayer(self)]) or len(self.bag) == 0:
#                 return  # No tile left to draw!
#             self.hands[getCurrentPlayer(self)].append(self.bag.pop(len(self.bag) - 1))
#         return
#
#     #
#     # Returns current player's hand.
#     #
#     # Player number (0 or 1).
#     #
#     def getHand(self):
#         return self.hands[getCurrentPlayer(self)]
#
#     #
#     # Returns player's score.
#     #
#     # player number (0 or 1).
#     #
#     def getScore(self, player):
#         return self.scores[player]
#
#     def __str__(self):
#         result = ''
#         for r in range(0, 15, 1):
#             for c in range(0, 15, 1):
#                 result += self.squares[r][c]
#             result += '\n'
#         return result
#
#     #
#     # Returns true if word can be played from the tiles available in hand.
#     #
#     def canBeDrawnFromHand(self, word, hand):
#         used = [0] * len(hand)
#         for c in list(word):
#             if c == ' ':
#                 continue
#             found = 0
#             for i in range(0, len(hand), 1):
#                 if not used[i]:
#                     tile = hand[i]
#                     if c == tile or (c.isupper and tile == '_'):
#                         used[i] = 1
#                         found = 1
#                         break
#             if found == 0:
#                 return 0
#         return True
#
#     #
#     # Returns the letter or symbol at location.
#     #
#     def getSquare(self, location):
#         return self.squares[location.getRow()][location.getColumn()]
#
#     #
#     # Sets the letter or symbol at location.
#     #
#     def setSquare(self, location, tile):
#         self.squares[location.getRow()][location.getColumn()] = tile
#
#     #
#     # Places word on board at the specified location and direction. Assumes this is legal.
#     #
#     def placeWord(self, word, location, direction):
#         for c in list(word):
#             if c != ' ':
#                 self.setSquare(c, location)
#             location = location.neighbor(direction)
#
#     # Returns true if the square at location contains a tile.
#     def isOccupied(self, location):
#         return self.getSquare(location)
#
#     #
#     # Returns true if word can be placed on board, in the sense of not overlapping existing tiles,
#     # leaving no gaps, having no tiles right before or after it, and not extending beyond the edge of the board.
#     #


def __canBePlacedOnBoard__(word, location, direction):
    # Check for tile right before word
    before = location.antineighbor(direction)
    if before.isOnBoard() and before.isOccupied():
        return False
    # Check squares within word
    for c in list(word):
        if not location.isOnBoard():  # Off edge of board
            return False
        if (c == ' ') != location.getSquare().isalpha:
            # Tile played on top of existing tile or gap in word where there is no tile
            return False
        location = location.neighbor(direction)
        # Check for tile right after word
        if location.isOnBoard() and location.isOccupied():
            return False
        # No problems!
    return True

    #
    # Returns true if word, placed at location in direction, would be connected. In other words,
    # word must contain an existing tile, be beside an existing tile, or contain the center.
    #
    def wouldBeConnected(self):
        cross = direction.opposite()
        for c in list(word):
            if c == ' ':
                return True
            if location.equals(location.CENTER):
                return True
            after = location.neighbor(cross)
            if after.isOnBoard() and self.isOccupied(after):
                return True
            before = location.antineighbor(cross)
            if before.isOnBoard() and self.isOccupied(before):
                return True
            location = location.neighbor(direction)
        return False

    # Finds the start of a (cross) word including location and moving in direction.
    #
    def findStartOfWord(self, location, direction):
        while location.isOnBoard() and self.isOccupied(location):
            location = location.antineighbor(direction)
        return location.neighbor(direction)


def isValidWord(board, location, direction, tile):
    if tile == ' ':
        return True  # Word was already on board
    location = board.findStartOfWord(location, direction)
    word = ""
    tileUsed = False
    while location.isOnBoard():
        if board.isOccupied(location):
            word += board.getSquare(location)
        elif tileUsed:
            break
        else:
            word += tile
            tileUsed = True
        location = location.neighbor(direction)
    if len(word) == 1:
        return True
    return word.lower in board.DICTIONARY


#
# Returns true if word, played at location in direction, forms a valid dictionary word of at least two letters.
#

# def __main__():
#   board = Board()
#   # Deal initial hands
#   board.__deal__(board.hands[0], 7)
#   board.__deal__(board.hands[1], 7)


#
# Returns true if the cross word including (but not necessarily starting with) location forms a valid dictionary
# word, or no new cross word was formed at this point. tile is The one tile played in this word.
#

def isValidWord1(board, word, location, direction):
    if len(word.length) < 2:
        return False
    letters = [0] * len(word)
    for i in range(0, len(word), 1):
        if board.isOccupied(location):
            letters[i] = board.getSquare(location)
        else:
            letters[i] = word[i]
        location = location.neighbor(direction)
    return letters in board.DICTIONARY


# Returns true if word, played at location and direction, would create only legal words.
def wouldCreateOnlyLegalWords(board, word, location, direction, tile):
    if not board.isValidWord(board, word, location, direction, tile):
        return False
    cross = direction.opposite()
    for _ in list(word):
        if not board.isValidWord1(board, word, location, cross):
            return False
        location = location.neighbor(direction)
    return True


# Returns the score for the cross word including (but not necessarily starting with) location.
#
# tile is the one tile played in this word.
#
def scoreWord(board, location, direction, tile):
    score = 0
    multiplier = 1
    location = board.findStartOfWord(location, direction)
    if location.neighbor(direction).isOnBoard() and not board.isOccupied(location.neighbor(direction)):
        return 0
    tileUsed = False
    while location.isOnBoard():
        square = board.getSquare(location)
        if board.isOccupied(location):
            score += board.TILE_VALUES[square]
        elif tileUsed:
            break
        else:
            score += board.TILE_VALUES[tile]
            bonus = board.getSquare(location)
            if bonus == board.DOUBLE_LETTER_SCORE:
                score += board.TILE_VALUES[tile]
            elif bonus == board.TRIPLE_LETTER_SCORE:
                score += 2 * board.TILE_VALUES[tile]
            elif bonus == board.DOUBLE_WORD_SCORE:
                multiplier *= 2
            elif bonus == board.TRIPLE_WORD_SCORE:
                multiplier *= 3
            tileUsed = True
        location = location.neighbor(direction)
    return score * multiplier


# Returns the points scored for word, played at location in direction.
def scoreWord1(board, word, location, direction):
    result = 0
    multiplier = 1
    for c in list(word):
        square = board.getSquare(location)
        if c == ' ':
            result += board.TILE_VALUES[square]
        else:
            result += board.TILE_VALUES[c]
            if square == board.DOUBLE_LETTER_SCORE:
                result += board.TILE_VALUES[c]
            elif square == board.TRIPLE_LETTER_SCORE:
                result += 2 * board.TILE_VALUES[c]
            elif square == board.DOUBLE_WORD_SCORE:
                multiplier *= 2
            elif square == board.TRIPLE_WORD_SCORE:
                multiplier *= 3
        location = location.neighbor(direction)
    return result * multiplier


# Returns the score for playing word at location in direction, including any cross words.
def score(board, word, location, direction):
    # Score word submitted
    result = board.scoreWord(board, word, location, direction)
    tilesPlayed = 0

    # Score cross words
    for c in list(word):
        if c != ' ':
            result += board.scoreWord(board, location, direction.opposite(), c)
            tilesPlayed += 1
        location = location.neighbor(direction)
    if tilesPlayed == 7:
        result += 50
    return result


def verifyLegality(board, word, location, direction, hand):
    if len(word) < 2:
        return True
    if not board.canBeDrawnFromHand(word, hand):
        return True
    if not board.canBePlacedOnBoard(word, location, direction):
        return True
    if not board.wouldBeConnected(word, location, direction):
        return True
    if not board.wouldCreateOnlyLegalWords(word, location, direction):
        return True
    return False


# Returns true if the game is over.
def gameIsOver(board):
    return board.numberOfPasses == 2 or not board.hands[0] or not board.hands[1]


# Scores any unplayed tiles at the end of the game.
def scoreUnplayedTiles(board):
    values = [0] * 2
    for i in range(0, len(board.hands), 1):
        for c in board.hands[i]:
            values[i] += board.TILE_VALUES[c]

    for i in range(0, len(board.hand), 1):
        board.scores[i] -= values[i]  # Lose value of own letters
        if not board.hands[i]:
            board.scores[i] += values[1 - i]  # Gain value of opponent's letters


#
# Plays word at location in direction from hand. Also refills hand from bag, toggles the current player, and resolves
# the end of the game if applicable.

def play(board, word, location, direction, hand):
    if verifyLegality(board, word, location, direction, hand):
        return
    board.scores[board.currentPlayer] += board.score(board, word, location, direction)
    board.placeWord(word, location, direction)
    removeTiles(word, hand)
    # print("dealed")
    board.deal(hand, 7 - hand.size())
    if board.currentPlayer == 0:
        board.currentPlayer = 1
    else:
        board.currentPlayer = 0
    board.numberOfPasses = 0
    if board.gameIsOver():
        scoreUnplayedTiles(board)


#
# Exchanges 0 or more tiles from hand with the bag. Also toggles the current player and resolves the end of the game
# if applicable. tilesToExchange is an array of 7 booleans indicating which tiles to exchange.
#
def exchange(board, hand, tilesToExchange):
    removed = ''
    for i in range(0, len(hand)):
        if tilesToExchange[i]:
            removed += hand[i]
    dumped = removeTiles(removed, hand)
    board.deal(board, hand, 7 - len(hand))
    # Return dumped letters to bag
    for c in list(dumped):
        board.bag.append(c)
    random.shuffle(board.bag)
    # If there weren't enough letters in bag, some dumped letters may return to hand
    board.deal(hand, 7 - hand.size())
    board.currentPlayer = 1 - board.currentPlayer
    board.numberOfPasses += 1
    if gameIsOver(board):
        scoreUnplayedTiles(board)


# Removes the tiles used in word from hand and returns them in a new String.
def removeTiles(word, hand):
    result = ''
    for c in list(word):
        if ord(c) >= ord('A') and c <= ord('Z'):
            c = '_'
        hand.remove(c)
        result += ord(c)
    return result


# Returns the current player number (0 or 1).
def getCurrentPlayer(board):
    return board.currentPlayer


# # Intermediary between a ScrabbleAI and a Board, allowing the former to get information it needs without allowing
# full access.

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


#
# Player that can choose moves for Scrabble.
#
# from abc import ABCMeta
# class ScrabbleAI(object):

#   __metaclass__ = ABCMeta
#   #
#   # Sets the GateKeeper for the next move. Note that, in a tournament, this may be from a completely new game; each move should be generated independently.
#   #
#   def setGateKeeper(gateKeeper):

#   #
#   # Returns a good move given the state of the game (accessed through the GateKeeper).
#   #
#     def chooseMove():

# # Playing one or more tiles on the board.

# # A move played by a ScrabbleAI. Used mainly as the return type of ScrabbleAI.chooseMove(). class ScrabbleMove():
# __metaclass__ = ABCMeta # # Plays this move on board for the indicated player. Returns the location and direction
# of the move if relevant, null otherwise. # def play(board, playerNumber)

# class PlayWord(object):
#     #
#     # The word to be played.
#     #
#     #
#     #
#
#     word = ''
#
#     # The location of the first tile in the word (new or already on the board.
#     location = Location(None, None)
#
#     # The direction in which this word is to be played: Location.HORIZONTAL or Location.VERTICAL.
#     direction = Location(None, None)
#
#     def __init__(self, word, location, direction, board):
#         self.board = board
#         self.word = word
#         self.location = location
#         self.direction = direction
#
#     def play(self, board, playerNumber):
#         play(board, self.word, self.location, self.direction, board.getHand(playerNumber))
#         return Location(self.location, self.direction)


# Exchanging 0 or more tiles.
class ExchangeTiles:
    #
    # An array of seven booleans, indicating which tiles in the hand to exchange. Any entries beyond the length of
    # the hand are ignored.
    #

    tilesToExchange = [False] * 7

    def __init__(self):
        self.tilesToExchange = self.tilesToExchange

    def play(self, board):
        playerNumber = board.getCurrentPlayer()
        board.exchange(board.getHand(playerNumber), self.tilesToExchange)
        return None


class MyScrabblePlayer(object):
    ALL_TILES = [True, True, True, True, True, True, True]

    def __init__(self, board):
        self.board = board
        self.gate = GateKeeper(board)

    # considers every permutation of letters in the current hand and plays the best word on the best spot on the
    # board that also hits the center tile this could be improved by only considering the center cross on the board
    # as possible plays rather than every location on the board and returns best possible move
    #
    def findFistMove(self):
        hand = self.gate.getHand()
        bestMove: list[PlayWord] = [PlayWord('', Location(0, 0), VERTICAL, self.board)] * 7
        i: int
        for i in (0, 6, 1):
            bestMove[i] = PlayWord(None, None, None, self.board)
        bestScore: list[int] = [-1] * 7
        # for i in (0, 6, 1):
        #     # initialize the arrays
        #     bestScore[i] = -1
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
                                    if p != q and p != m and p != n and p != i and p != j and p != k and q != m and q != n and q != i and q != j and q != k and m != n and m != i and m != j and m != k and n != i and n != j and n != k and i != j and i != k and j != k:
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
                                        kk: int
                                        for kk in range(0, 5, 1):
                                            word = words[kk]
                                            for row in range(0, self.board.WIDTH - 1, 1):
                                                for col in range(0, Board.WIDTH - 1, 1):
                                                    location = Location(row, col)
                                                    for direction in (HORIZONTAL, VERTICAL):
                                                        if self.gate.verifyLegality():
                                                            continue  # if it wasn't legal; go on to the next one
                                                        local_score = self.gate.score(word, location, direction)
                                                        if local_score > bestScore[kk]:
                                                            bestScore[kk] = local_score
                                                            bestMove[kk] = PlayWord(word, location, direction,
                                                                                    self.board)

        best = 0
        index = 0
        # make this into a separate method -- TODO 
        for i in range(1, 6):  # finds the best playable word using the scores
            if bestScore[i] > best:
                best = bestScore[i]
                index = i
        if bestMove[index] is not None:
            return bestMove[index]
        return ExchangeTiles()  # in the case that we cannot make a word, which should never be the case

        #
        # finds the best possible move through playing up to 4 tiles on the board
        # cannot play between two columns or rows that have a gap between them that plays across both rows/columns
        # returns the best move
        #

    def findAllMoves(self):
        found = False  # check to see if we need to exchange tiles a.k.a. pass
        hand = self.gate.getHand()
        bestMove = [PlayWord(self.board, None, None, None)] * 5
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
                            words = [['']] * 4
                            words[0] = " " + a, a + " ", "  " + a, "   " + a, a + "  ", a + "   "
                            words[
                                1] = "" + a + b, a + b + " ", a + " " + b, " " + a + b, "  " + a + b, "   " + a + b, a + b + "  ", a + b + "   ", a + "  " + b, a + "   " + b
                            words[
                                2] = "" + a + b + c, a + b + c + " ", a + b + " " + c, a + " " + b + c, " " + a + b + c, a + b + c + "  ", a + b + c + "   ", a + b + c + "    ", a + b + c + "     ", "  " + a + b + c, "   " + a + b + c, "    " + a + b + c, "     " + a + b + c
                            words[
                                3] = "" + a + b + c + d, a + b + c + d + " ", a + b + c + " " + d, a + b + " " + c + d, a + " " + b + c + d, " " + a + b + c + d, "  " + a + b + c + d, "   " + a + b + c + d, "     " + a + b + c + d
                            count = len(hand)
                            if count > 4:
                                count = 4
                                # tries every possible word string on every location
                                for kk in range(0, count):
                                    for word in words[kk]:
                                        for row in range(0, self.board.WIDTH - 1):
                                            for col in range(0, self.board.WIDTH - 1):
                                                location = Location(row, col)
                                                for direction in (HORIZONTAL, VERTICAL):
                                                    if self.gate.verifyLegality():
                                                        continue
                                                    found = True
                                                    score = self.gate.score(word, location, direction)
                                                    if score > bestScore[kk]:
                                                        bestScore[kk] = score
                                                        bestMove[kk] = PlayWord(word, location, direction, self.board)
        best = 0
        index = 0
        for i in range(0, 3):  # finds best playable word using the scores
            if bestScore[i] > best:
                best = bestScore[i]
                index = i
        # checks if we have found a word and that our word choice is not null
        if bestMove[index] is not None and found:
            return bestMove[index]
        return ExchangeTiles()

    #
    #
    # returns best first move or best move in general depending on if the center tile is open
    #
    def findBestMove(self):
        if self.gate.getSquare(CENTER) == self.board.DOUBLE_WORD_SCORE:
            return self.findFistMove
        return self.findAllMoves()

    def setGateKeeper(self, gateKeeper):
        self.gate = gateKeeper

    def chooseMove(self):
        return self.findBestMove()


#
# Dumb AI that picks the highest-scoring one-tile move. Plays a two-tile move on the first turn. Exchanges all of its
# letters if it can't find any other move.
#
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
                    localscore = self.gateKeeper.score(word, CENTER, HORIZONTAL)
                    if localscore > bestScore:
                        bestScore = localscore
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
                            localscore = self.gateKeeper.score(word, location, direction)
                            if localscore > bestScore:
                                bestScore = localscore
                                bestMove = PlayWord(word, location, direction, self.board)

        if bestMove:
            return bestMove
        return ExchangeTiles()

    def chooseMove(self):
        if self.gateKeeper.getSquare(CENTER) == self.board.DOUBLE_WORD_SCORE:
            return self.findTwoTileMove()
        return self.findOneTileMove()


# GUI allowing a human to play against a ScrabbleAI. To change the AI, edit the constructor.


# Returns true if key is a letter or a space.
def isLetterOrSpace(key):
    if key is not None:
        return ord('a') <= ord(key) <= ord('z') or (ord('A') <= ord(key) <= ord('Z')) or key == " "


class Game(object):
    COLORS = dict()

    # LETTER_FONT = tkFont.Font(family="MS Sans Serif", size=20)

    # VALUE_FONT =  tkFont.Font(family="MS Sans Serif", size = 10)

    # INTERFACE_FONT = tkFont.Font(family = "MS Serif", size = 18)

    # TYPING_FONT = tkFont.Font(family = "Comic Sans MS", size = 18)

    # Keys that the user might press.
    KEYS = []

    # This Scrabble is always in exactly one of these modes.
    Mode = 0

    # BOARD = auto() # Board is 0: Waiting for user to play a word on the board
    # HAND =auto() # Hand is 1: Waiting for user to select tiles (if any) to exchange
    # ILLEGAL_MOVE = auto() # IM is 2: Waiting for user to acknowledge an illegal move
    # AI_PLAYING = auto() # AP is 3: Waiting for AI to play
    # GAME_OVER = auto() # GO is 4: Game over

    def __init__(self):
        # print("Hello world")
        self.board = Board()
        self.COLORS[ord(self.board.NO_PREMIUM)] = StdDraw.PINK
        # print(self.board.NO_PREMIUM)
        self.COLORS[ord(self.board.DOUBLE_LETTER_SCORE)] = StdDraw.LIGHT_GRAY
        self.COLORS[ord(self.board.TRIPLE_LETTER_SCORE)] = StdDraw.CYAN
        self.COLORS[ord(self.board.DOUBLE_WORD_SCORE)] = StdDraw.DARK_GRAY
        self.COLORS[ord(self.board.TRIPLE_WORD_SCORE)] = StdDraw.VIOLET
        # print(str(self.COLORS['#']))
        for c in range(ord('a'), ord('z')):
            self.COLORS[c] = StdDraw.TILE_COLOR
        for c in range(ord('A'), ord('Z')):
            self.COLORS[c] = StdDraw.TILE_COLOR
        self.COLORS[ord('_')] = StdDraw.TILE_COLOR
        # Relevant keys
        for c in {'a', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'x',
                  'c', 'v', 'b', 'n', 'm', 'z'}:
            self.KEYS.append(c)
        self.KEYS.append("/")
        self.KEYS.append("[")  # use as left
        self.KEYS.append("]")  # use as right
        self.KEYS.append("=")  # use as up
        self.KEYS.append("-")  # use as down
        for c in {'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X',
                  'C', 'V', 'B', 'N', 'M'}:
            self.KEYS.append(c)
        self.KEYS.append(" ")
        self.KEYS.append("\x08")
        self.KEYS.append("\r")
        self.KEYS.append("\\")  # backslash: use instead of alt
        print(self.KEYS[1])
        print(self.KEYS)

        # Current GUI mode.
        self.mode = 0

        # Location of the cursor on the board.
        self.boardCursor = Location(0, 0)

        # Direction (Location.HORIZONTAL or Location.VERTICAL) of cursor on the board.
        self.boardCursorDirection = Location(0, 0)

        #
        # The word currently being constructed.
        #
        self.wordBeingConstructed = ''

        # Location of the cursor in the user's hand, for selecting tiles to discard.
        self.handCursor = 0

        # Tiles marked for discarding.
        self.tilesToDiscard = []

        # Tiles marked for exchanging
        self.tilesToExchange = []

        # Opponent.
        self.ai = MyScrabblePlayer(self.board)

        # ai = Incrementalist() # Opponent
        self.ai.setGateKeeper(GateKeeper(self.board))

    # Draws one square or tile at position x, y
    #
    # outlined is true if this is the current tile in the hand when selecting tiles to exchange.
    # crossedOut is True if this tile has been marked for exchange.
    # faceDown is True if this is a tile in the opponent's hand.
    #
    def drawSquare(self, x, y, square, outlined, crossedOut, faceDown):
        # Draw background
        # print(square)
        StdDraw.setPenColor(self.COLORS[ord(square)])
        StdDraw.filledSquare(x, y, 0.5)
        # Draw letter and value for regular tile
        if not faceDown:
            if ord('a') <= ord(square) <= ord('z'):
                StdDraw.setPenColor(StdDraw.BLACK)
                # StdDraw.setFont(LETTER_FONT)
                StdDraw.text(x, y, ("" + square))
                # StdDraw.setFont(VALUE_FONT)
                StdDraw.text(x + 0.3, y - 0.3, "" + str(self.board.TILE_VALUES[ord(square)]))
            elif ord('A') <= ord(square) <= ord('Z'):
                StdDraw.setPenColor(StdDraw.RED)
                # StdDraw.setFont(LETTER_FONT)
                StdDraw.text(x, y, ("" + square))
                # Draw outline
                if outlined:
                    StdDraw.setPenColor(StdDraw.WHITE)
                elif square.isalpha or square == '_':
                    StdDraw.setPenColor(StdDraw.BLACK)
                else:
                    StdDraw.setPenColor(StdDraw.WHITE)
                StdDraw.square(x, y, 0.5)
                # Draw slash
                if crossedOut:
                    StdDraw.setPenColor(StdDraw.BLACK)
                    StdDraw.line(x - 0.5, y - 0.5, x + 0.5, y + 0.5)
                    StdDraw.line(x - 0.5, y + 0.5, x + 0.5, y - 0.5)

    # Draws the current state of the game, including instructions. */

    # Draws the board cursor.
    def drawBoardCursor(self):
        x = self.boardCursor.getColumn()
        y = 14 - self.boardCursor.getRow()
        if self.boardCursorDirection == HORIZONTAL:
            xs = {x - 0.4, x - 0.4, x + 0.4}
            ys = {y - 0.2, y + 0.2, y}
        else:
            xs = {x - 0.2, x + 0.2, x}
            ys = {y + 0.4, y + 0.4, y - 0.4}
        StdDraw.setPenColor(StdDraw.WHITE)
        StdDraw.filledPolygon(xs, ys)
        StdDraw.setPenColor(StdDraw.TABLE_COLOR)
        StdDraw.polygon(xs, ys)

    def draw(self):
        StdDraw.clear()
        # Draw board
        for r in range(self.board.WIDTH - 1, -1, -1):
            for c in range(self.board.WIDTH - 1, -1, -1):
                # r and c are converted to x and y in this call
                self.drawSquare(c, 14 - r, self.board.getSquare(Location(r, c)), False, False, False)
        # Draw hands
        hand = self.board.getHand()
        for i in range(0, len(hand) - 1):
            self.drawSquare(16 + i, 14, hand[i], False, False, True)
        for i in range(0, len(hand) - 1):
            self.drawSquare(16 + i, 11, hand[i], self.mode == 1 and self.handCursor == i,
                            self.mode == 1 and self.tilesToDiscard[i], False)
        # print("here")
        # print(self.mode)
        StdDraw.setPenColor(StdDraw.BLACK)
        # StdDraw.setFont(self.INTERFACE_FONT)
        StdDraw.text(19, 13, "Opponent: " + str(self.board.getScore(0)))
        StdDraw.text(19, 10, "You: " + str(self.board.getScore(1)))
        StdDraw.show(100)
        # print("here")
        if self.mode == 0:
            # Draw cursor
            # print("here")
            self.drawBoardCursor()
            # Draw word being constructed
            StdDraw.setPenColor(StdDraw.BLACK)
            # StdDraw.setFont(self.TYPING_FONT)
            StdDraw.text(19, 8, "[" + self.wordBeingConstructed + "]")
            # Draw instructions
            # StdDraw.setFont(self.INTERFACE_FONT)
            StdDraw.text(19, 7, "Type a word and hit enter to play.")
            StdDraw.text(19, 6, "Use spaces for tiles aready on board,")
            StdDraw.text(19, 5, "an upper-case letter to play a blank.")
            StdDraw.text(19, 4, "Use - and = as to move cursor up and down,")
            StdDraw.text(19, 3, "[ and ] to move cursor left and right,  ")
            StdDraw.text(19, 2, "/ to toggle direction.")
            StdDraw.text(19, 1, "Use \ to exchange letters or pass.")
        elif self.mode == 1:
            StdDraw.setPenColor(StdDraw.BLACK)
            # StdDraw.setFont(self.INTERFACE_FONT)
            StdDraw.text(19, 6, "Use -/= and [/] as U/D and L/R to move in hand.")
            StdDraw.text(19, 5, "Space to mark/unmark tile.")
            StdDraw.text(19, 4, "Enter to exchange marked tiles.")
            StdDraw.text(19, 3, "Use \ to return to board.")
        elif self.mode == 2:
            # Draw word being constructed
            StdDraw.setPenColor(StdDraw.BLACK)
            # StdDraw.setFont(self.TYPING_FONT)
            StdDraw.text(19, 8, "[" + self.wordBeingConstructed + "]")
            # Draw instructions
            # StdDraw.setFont(self.INTERFACE_FONT)
            StdDraw.text(19, 6, "Illegal move.")
            StdDraw.text(19, 5, "Press enter to continue.")
        elif self.mode == 4:
            StdDraw.setPenColor(StdDraw.BLACK)
            # StdDraw.setFont(self.INTERFACE_FONT)
            StdDraw.text(19, 6, "Game over.")
        elif self.mode == 3:
            StdDraw.setPenColor(StdDraw.BLACK)
            # StdDraw.setFont(self.INTERFACE_FONT)
            StdDraw.text(19, 6, "Opponent thinking...")
        StdDraw.show()
        print("made it past show")

    # Prepare for the user to play a word on the board. */
    def enterBoardMode(self):
        self.mode = 0
        self.wordBeingConstructed = ""

    # Returns the key that the user pressed. Shift modifies letter keys in the usual way.
    def getKeyPressed(self):
        # print("here")
        # print(len(StdDraw.keysTyped))
        # print(StdDraw.keysTyped[0])
        # print(len(KEYSTYPED))
        temp_key = None
        while not temp_key:
            temp_key = StdDraw.checkForEvents()
        if temp_key is not LASTKEYTYPED and temp_key is not None:
            print(temp_key)
            for i in range(0, 59):
                # print(key)
                if temp_key[0] == self.KEYS[i]:
                    print("found")
                    result = self.KEYS[i]
                    if ord('A') <= ord(self.KEYS[i]) <= ord('Z') and not self.KEYS[i] == '':
                        result = self.KEYS[i]
                    print(result)
                    return result

    #
    # Handles a key pressed by the user.
    #

    # Prepare for the user to select tiles (if any) to exchange.
    def enterHandMode(self):
        self.mode = 1
        self.handCursor = 0
        self.tilesToDiscard = [False] * 7

    def handleKeyPress(self):
        # global wordBeingConstructed, boardCursor
        c = self.getKeyPressed()
        print(c)
        print(self.mode)
        if self.mode == 0:
            boardCursorDirection = self.boardCursorDirection.opposite()
            # Move board cursor
            local_next = None
            if c == "[":
                local_next = self.boardCursor.antineighbor()
            elif c == "]":
                local_next = self.boardCursor.neighbor()
            elif c == "=":
                local_next = self.boardCursor.antineighbor()
            elif c == "-":
                local_next = self.boardCursor.neighbor()
            if local_next and local_next.isOnBoard():
                boardCursor = local_next
            # Type in word to be played
            if isLetterOrSpace(c):
                self.wordBeingConstructed += c
            if c == "\x08" and not self.wordBeingConstructed.isEmpty():
                self.wordBeingConstructed = self.wordBeingConstructed[0, len(self.wordBeingConstructed) - 1]
                print(self.wordBeingConstructed)
            # Play word
            if c == "\r":
                word_to_play = PlayWord(self.wordBeingConstructed, self.boardCursor, boardCursorDirection, self.board)
                word_to_play.play(self.board)
                if gameIsOver(self.board):
                    self.mode = 4
                else:
                    self.mode = 3
            # Switch to hand mode
            if c == "\\":
                self.enterHandMode()
            elif self.mode == 1:
                # Switch to board mode
                if c == "\\":
                    self.enterBoardMode()
                # Move hand cursor
                if c == "-":
                    self.handCursor -= 1
                    if self.handCursor < 0:
                        self.handCursor += 1
                    elif c == "=":
                        self.handCursor += 1
                        if self.handCursor >= self.board.getHand(1).size():
                            self.handCursor -= 1

                    # Toggle letter
                    if c == " ":
                        self.tilesToDiscard[self.handCursor] = not self.tilesToDiscard[self.handCursor]
                    # Exchange/pass
                    if c == "Enter":
                        exchange(self.board.getHand(), self.tilesToDiscard, self.tilestoExchange)
                        if gameIsOver(self.board):
                            self.mode = 4
                        else:
                            self.mode = 3
                elif self.mode == 2:
                    if c == "Enter":
                        self.enterBoardMode()

    # Runs the game. Crashes if the AI opponent plays an illegal move.
    def run(self):
        self.board.deal()
        self.board.currentPlayer = 1
        StdDraw.setCanvasSize(805, 525)
        StdDraw.setXscale(-1.5, 23.5)
        StdDraw.setYscale(-1.5, 15.5)
        # StdDraw.enableDoubleBuffering()
        self.boardCursor = CENTER
        self.boardCursorDirection = HORIZONTAL
        self.draw()
        # print("here")
        while self.mode != 4:
            if self.mode == 3:
                self.draw()
                place = self.ai.chooseMove().play(self.board)
                if place:
                    self.boardCursor = place
                    self.boardCursorDirection = place
                if gameIsOver(self.board):
                    self.mode = 4
                else:
                    self.enterBoardMode()
                    self.draw()
            else:
                self.draw()
                self.handleKeyPress()


def _main():
    game = Game()
    game.run()


if __name__ == '__main__':
    _main()
