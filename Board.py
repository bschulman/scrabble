import random

from Location import *


# Board object

class Board(object):
    # Width of this Board, in squares.
    WIDTH = 15

    # Symbol for a double letter score square.
    DOUBLE_LETTER_SCORE = '-'

    # Symbol for a triple letter score square. */
    TRIPLE_LETTER_SCORE = '='

    # Symbol for a double word score square. */
    DOUBLE_WORD_SCORE = '+'

    # Symbol for a triple word score square. */
    TRIPLE_WORD_SCORE = '#'

    # Symbol for a regular square. */
    NO_PREMIUM = ' '

    # Initial layout of bonus squares.
    LAYOUT = ['#  -   #   -  #', ' +   =   =   + ', '  +   - -   +  ', '-  +   -   +  -', '    +     +    ',
              ' =   =   =   = ', '  -   - -   -  ', '#  -   +   -  #', '  -   - -   -  ', ' =   =   =   = ',
              '    +     +    ', '-  +   -   +  -', '  +   - -   +  ', ' +   =   =   + ', '#  -   #   -  #']

    def __init__(self):
        # Occupied Squares on the board (whether occupied by tiles or not).
        # rows, cols = (15, 15)
        self.numberOfPasses = 0
        self.squares = [[''] * 15] * 15

        # Set of legal words.
        self.DICTIONARY = set()

        # Associates tiles with their values.
        self.TILE_VALUES = dict()

        # Hands of the players.
        self.hands = [[]] * 2

        # The bag of remaining tiles.
        self.bag = []

        # Scores of the players.
        self.scores = [0, 0]

        # Current player number (0 or 1).
        self.currentPlayer = 0

        # Load dictionary
        with open('enable1.txt') as n:
            # print("loaded")
            for word in n.readlines():
                self.DICTIONARY.add(word)

        # Initialize tile values
        l = 'eaionrtlsu'
        res = [ord(ele) for sub in l for ele in sub]
        for c in res:
            self.TILE_VALUES[c] = 1
        l = 'dg'
        res = [ord(ele) for sub in l for ele in sub]
        for c in res:
            self.TILE_VALUES[c] = 2
        l = 'bcmp'
        res = [ord(ele) for sub in l for ele in sub]
        for c in res:
            self.TILE_VALUES[c] = 3

        l = 'fhvwy'
        res = [ord(ele) for sub in l for ele in sub]
        for c in res:
            self.TILE_VALUES[c] = 4

        self.TILE_VALUES[ord('k')] = 5

        l = 'jx'
        res = [ord(ele) for sub in l for ele in sub]
        for c in res:
            self.TILE_VALUES[c] = 8

        l = 'qz'
        res = [ord(ele) for sub in l for ele in sub]
        for c in res:
            self.TILE_VALUES[c] = 10

        for c in range(ord('A'), ord('Z'), 1):
            self.TILE_VALUES[c] = 0

        self.TILE_VALUES['-'] = 0

        # Number of consecutive tile exchange turns; 2 ends the game.
        self.squares = self.LAYOUT
        # for r in range(0, 15, 1):
        #     for i in range(0, 15, 1):
        #         self.squares[r][i] = self.LAYOUT[r][i]
        # Create bag
        self.bag = list()
        for tile in list(
                'aaaaaaaaabbccddddeeeeeeeeeeeeffggghhiiiiiiiiijkllllmmnnnnnnooooooooppqrrrrrrssssttttttuuuuvvwwxyyz__'):
            self.bag.append(tile)
        random.shuffle(self.bag)

    #
    # Exchanges 0 or more tiles from hand with the bag. Also toggles the current player and resolves the end of the game
    # if applicable. tilesToExchange is an array of 7 booleans indicating which tiles to exchange.
    #
    def exchange(self, tilesToExchange):
        hand = self.getHand()
        removed = ''
        for i in range(0, len(hand)):
            if tilesToExchange[i]:
                removed += hand[i]
        dumped = self.removeTiles(removed, hand)
        self.deal()
        # Return dumped letters to bag
        for c in list(dumped):
            self.bag.append(c)
        random.shuffle(self.bag)
        # If there weren't enough letters in bag, some dumped letters may return to hand
        self.deal()
        self.currentPlayer = 1 - self.currentPlayer
        self.numberOfPasses += 1
        if self.Over():
            self.scoreUnplayedTiles()

    # Removes the tiles used in word from hand and returns them in a new String.
    @staticmethod
    def removeTiles(word, hand):
        result = ""
        for c in word:
            if ord(c) >= ord('A') & ord(c) <= ord('Z'):
                c = '_'
            hand.remove(c)
            result += c
        return result

    # Returns the current player number (0 or 1).
    def getCurrentPlayer(self):
        return self.currentPlayer

    def deal(self):
        for i in range(0, 6, 1):
            if 7 == len(self.hands[self.getCurrentPlayer()]) or len(self.bag) == 0:
                return  # No tile left to draw!
            self.hands[self.getCurrentPlayer()].append(self.bag.pop(len(self.bag) - 1))
        return

    #
    # Returns current player's hand.
    #
    # Player number (0 or 1).
    #
    def getHand(self):
        return self.hands[self.getCurrentPlayer()]

    #
    # Returns player's score.
    #
    # player number (0 or 1).
    #
    def getScore(self, player):
        return self.scores[player]

    def __str__(self):
        result = ''
        for r in range(0, 15, 1):
            for c in range(0, 15, 1):
                result += self.squares[r][c]
            result += '\n'
        return result

    #
    # Returns true if word can be played from the tiles available in hand.
    #
    @staticmethod
    def canBeDrawnFromHand(word, hand):
        used = [0] * len(hand)
        for c in list(word):
            if c == ' ':
                continue
            found = 0
            for i in range(0, len(hand), 1):
                if not used[i]:
                    tile = hand[i]
                    if c == tile or (c.isupper and tile == '_'):
                        used[i] = 1
                        found = 1
                        break
            if found == 0:
                return 0
        return True

    #
    # Returns the letter or symbol at location.
    #
    def getSquare(self, location):
        return self.squares[location.getRow()][location.getColumn()]

    #
    # Sets the letter or symbol at location.
    #
    def setSquare(self, location, tile):
        self.squares[location.getRow()][location.getColumn()] = tile

    #
    # Places word on board at the specified location and direction. Assumes this is legal.
    #
    def placeWord(self, word, location, direction):
        for c in list(word):
            if c != ' ':
                self.setSquare(c, location)
            location = location.neighbor(direction)

    #
    # Returns true if word, placed at location in direction, would be connected. In other words,
    # word must contain an existing tile, be beside an existing tile, or contain the center.
    #
    def wouldBeConnected(self, word, location, direction):
        cross = direction.opposite()
        for c in list(word):
            if c == ' ':
                return True
            if location.equals(CENTER):
                return True
            after = location.neighbor(cross)
            if after.isOnBoard() and self.isOccupied(after):
                return True
            before = location.antineighbor(cross)
            if before.isOnBoard() and self.isOccupied(before):
                return True
            location = location.neighbor(direction)
        return False

    #
    # Finds the start of a (cross) word including location and moving in direction.
    #

    def findStartOfWord(self, loc, direction):
        while loc.isOnBoard() and self.isOccupied(loc):
            loc = loc.antineighbor(direction)
        return loc.neighbor(direction)

    #
    # Returns true if word, played at location in direction, forms a valid dictionary word of at least two letters.
    #

    def isValidWord(self, word, location, direction):
        if len(word.length) < 2:
            return False
        letters = [0] * len(word)
        for i in range(0, len(word), 1):
            if self.isOccupied(location):
                letters[i] = self.getSquare(location)
            else:
                letters[i] = word[i]
            location = location.neighbor(direction)
        return letters in self.DICTIONARY

        # Returns true if the cross word including (but not necessarily starting with) location forms a valid dictionary
        # word, or no new cross word was formed at this point.

    def isValidWord1(self, location, direction, tile):
        if tile == ' ':
            return True  # Word was already on board
        location = self.findStartOfWord(location, direction)
        word = ""
        tileUsed = False
        while location.isOnBoard():
            if self.isOccupied(location):
                word += self.getSquare(location)
            elif tileUsed:
                break
            else:
                word += tile
                tileUsed = True
            location = location.neighbor(direction)
        if len(word) == 1:
            return True
        return word.lower in self.DICTIONARY

    #
    # Returns true if the square at location contains a tile.
    #

    def isOccupied(self, location):
        return self.getSquare(location)

    # Returns true if word, played at location and direction, would create only legal words.
    def wouldCreateOnlyLegalWords(self, word, location, direction):
        if not self.isValidWord1(word, location, direction):
            return False
        cross = direction.opposite()
        for _ in list(word):
            if not self.isValidWord1(word, location, cross):
                return False
            location = location.neighbor(direction)
        return True

    # Returns the score for the cross word including (but not necessarily starting with) location.
    #
    # tile is the one tile played in this word.
    #

    def scoreWord(self, location, direction, tile):
        temp_score = 0
        multiplier = 1
        location = self.findStartOfWord(location, direction)
        if location.neighbor(direction).isOnBoard() and not self.isOccupied(location.neighbor(direction)):
            return 0
        tileUsed = False
        while location.isOnBoard():
            square = self.getSquare(location)
            if self.isOccupied(location):
                temp_score += self.TILE_VALUES[square]
            elif tileUsed:
                break
            else:
                temp_score += self.TILE_VALUES[tile]
                bonus = self.getSquare(location)
                if bonus == self.DOUBLE_LETTER_SCORE:
                    temp_score += self.TILE_VALUES[tile]
                elif bonus == self.TRIPLE_LETTER_SCORE:
                    temp_score += 2 * self.TILE_VALUES[tile]
                elif bonus == self.DOUBLE_WORD_SCORE:
                    multiplier *= 2
                elif bonus == self.TRIPLE_WORD_SCORE:
                    multiplier *= 3
                tileUsed = True
            location = location.neighbor(direction)
        return temp_score * multiplier

    # Returns the points scored for word, played at location in direction.
    def scoreWord1(self, word, location, direction):
        result = 0
        multiplier = 1
        for c in list(word):
            square = self.getSquare(location)
            if c == ' ':
                result += self.TILE_VALUES[square]
            else:
                result += self.TILE_VALUES[c]
                if square == self.DOUBLE_LETTER_SCORE:
                    result += self.TILE_VALUES[c]
                elif square == self.TRIPLE_LETTER_SCORE:
                    result += 2 * self.TILE_VALUES[c]
                elif square == self.DOUBLE_WORD_SCORE:
                    multiplier *= 2
                elif square == self.TRIPLE_WORD_SCORE:
                    multiplier *= 3
            location = location.neighbor(direction)
        return result * multiplier

        # Returns the score for playing word at location in direction, including any cross words.

    def score(self, word, location, direction):
        # Score word submitted
        result = self.scoreWord(word, location, direction)
        tilesPlayed = 0

        # Score cross words
        for c in list(word):
            if c != ' ':
                result += self.scoreWord(c, location, direction.opposite())
                tilesPlayed += 1
            location = location.neighbor(direction)
        if tilesPlayed == 7:
            result += 50
        return result

    def verifyLegality(self, word, location, direction, hand):
        if len(word) < 2:
            print("Word must be at least two letters long.")
            return True
        if not self.canBeDrawnFromHand(word, hand):
            print("Hand does not contain sufficient tiles to play word.")
            return True
        if not self.canBePlacedOnBoard(word, location, direction):
            print("Board placement incorrect (gaps, overlapping tiles, edge of board).")
            return True
        if not self.wouldBeConnected(word, location, direction):
            print("Board placement incorrect (gaps, overlapping tiles, edge of board).")
            return True
        if not self.wouldCreateOnlyLegalWords(word, location, direction):
            print("Invalid word created.")
            return True
        return False

    #
    # Returns true if word can be placed on board, in the sense of not overlapping existing tiles,
    # leaving no gaps, having no tiles right before or after it, and not extending beyond the edge of the board.
    #

    @staticmethod
    def canBePlacedOnBoard(word, location, direction):
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
    # Returns true if word, played at location in direction, forms a valid dictionary word of at least two letters.
    #

    # def __main__():
    #   board = Board()
    #   # Deal initial hands
    #   board.__deal__(board.hands[0], 7)
    #   board.__deal__(board.hands[1], 7)

    # Returns true if the game is over.
    def Over(self):
        return self.numberOfPasses == 2 or not self.hands[0] or not self.hands[1]

    # Scores any unplayed tiles at the end of the game.
    def scoreUnplayedTiles(self):
        values = [0] * 2
        for i in range(0, len(self.hands), 1):
            for c in self.hands[i]:
                values[i] += self.TILE_VALUES[c]

        for i in range(0, len(self.hands), 1):
            self.scores[i] -= values[i]  # Lose value of own letters
            if not self.hands[i]:
                self.scores[i] += values[1 - i]  # Gain value of opponent's letters

    #
    # Plays word at location in direction from hand. Also refills hand from bag, toggles the current player,
    # and resolves the end of the game if applicable.
    def play(self, word, location, direction, hand):
        self.verifyLegality(word, location, direction, hand)
        self.scores[self.currentPlayer] += self.score(word, location, direction)
        self.placeWord(word, location, direction)
        self.removeTiles(word, hand)
        self.deal()
        currentPlayer = 1 - self.currentPlayer
        numberOfPasses = 0
        if self.Over():
            self.scoreUnplayedTiles()
