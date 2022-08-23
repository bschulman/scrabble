import Board
import Location


# Plays word at location in direction from hand. Also refills hand from bag, toggles the current player, and resolves
# the end of the game if applicable.

# Removes the tiles used in word from hand and returns them in a new String.
def removeTiles(word, hand):
    result = ''
    for c in list(word):
        if ord(c) >= ord('A') and c <= ord('Z'):
            c = '_'
        hand.remove(c)
        result += ord(c)
    return result


def play(board, word, location, direction, hand):
    if board.verifyLegality(word, location, direction, hand):
        return
    board.scores[board.currentPlayer] += board.score(board, word, location, direction)
    board.placeWord(word, location, direction)
    removeTiles(word, hand)
    # print("dealt")
    board.deal(hand, 7 - hand.size())
    if board.currentPlayer == 0:
        board.currentPlayer = 1
    else:
        board.currentPlayer = 0
    board.numberOfPasses = 0
    if board.gameIsOver():
        Board.scoreUnplayedTiles(board)


class PlayWord(object):
    #
    # The word to be played.
    #
    #
    #
    word = ''

    # The location of the first tile in the word (new or already on the board).
    location = Location.Location(None, None)

    # The direction in which this word is to be played: Location.HORIZONTAL or Location.VERTICAL.
    direction = Location.Location(None, None)

    def __init__(self, word, location, direction, board):
        self.board = board
        self.word = word
        self.location = location
        self.direction = direction

    def play(self, board):
        play(board, self.word, self.location, self.direction, board.getHand())
        return Location.Location(self.location, self.direction)
