from enum import Enum
import StdDraw
import handleKeys
from Board import Board as Board
from Gatekeeper import GateKeeper as GateKeeper
from Location import CENTER as CENTER
from Location import HORIZONTAL as HORIZONTAL
from Location import Location as Location
from MyScrabblePlayer import MyScrabblePlayer as MyScrabblePlayer
from PlayWord import PlayWord as PlayWord


# GUI allowing a human to play against a ScrabbleAI.


# Returns true if key is a letter or a space.
def isLetterOrSpace(key):
    return ord('a') <= ord(key) <= ord('z') or (ord('A') <= ord(key) <= ord('Z')) or key == " "


class Game(object):
    COLORS = dict()

    # LETTER_FONT = tkFont.Font(family="MS Sans Serif", size=20)

    # VALUE_FONT =  tkFont.Font(family="MS Sans Serif", size = 10)

    # INTERFACE_FONT = tkFont.Font(family = "MS Serif", size = 18)

    # TYPING_FONT = tkFont.Font(family = "Comic Sans MS", size = 18)

    # This Scrabble is always in exactly one of these modes.
    class Mode(Enum):
        BOARD = 0  # Board is 0: Waiting for user to play a word on the board
        HAND = 1  # Hand is 1: Waiting for user to select tiles (if any) to exchange
        ILLEGAL_MOVE = 2  # I-M is 2: Waiting for user to acknowledge an illegal move
        AI_PLAYING = 3  # AP is 3: Waiting for AI to play
        GAME_OVER = 4  # GO is 4: Game over

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

        # Current GUI mode.
        self.mode = 0

        # Location of the cursor on the board.
        self.boardCursor = CENTER

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
        self.tiles_to_Exchange = []

        # Opponent.
        self.ai = MyScrabblePlayer(self.board)

        # ai = Incrementalist() # Opponent
        self.ai.setGateKeeper(GateKeeper(self.board))

    # Prepare for the user to play a word on the board. */
    def enterBoardMode(self):
        self.mode = 0
        self.wordBeingConstructed = ""

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
            StdDraw.text(19, 6, "Use spaces for tiles already on board,")
            StdDraw.text(19, 5, "an upper-case letter to play a blank.")
            StdDraw.text(19, 4, "Use - and = as to move cursor up and down,")
            StdDraw.text(19, 3, "[ and ] to move cursor left and right,  ")
            StdDraw.text(19, 2, "/ to toggle direction.")
            StdDraw.text(19, 1, 'Use \ to exchange letters or pass.')
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

        # Returns the key that the user pressed. Shift modifies letter keys in the usual way.

    # Prepare for the user to select tiles (if any) to exchange.
    def enterHandMode(self):
        self.mode = 1
        self.handCursor = 0
        self.tilesToDiscard = [False] * 7

    #
    # Handles a key pressed by the user
    #

    def handleKeyPress(self):
        # global wordBeingConstructed, boardCursor
        c = handleKeys.getKeyPressed()
        if self.mode == 0 and c == '/':
            boardCursorDirection = self.boardCursorDirection.opposite()
            # Move board cursor
            local_next = None
            if c == "[":
                local_next = self.boardCursor.antineighbor()
            if c == "]":
                local_next = self.boardCursor.neighbor()
            if c == "=":
                local_next = self.boardCursor.antineighbor()
            if c == "-":
                local_next = self.boardCursor.neighbor()
            if local_next and local_next.isOnBoard():
                self.boardCursor = local_next
            # Type in word to be played
            if isLetterOrSpace(c):
                self.wordBeingConstructed += c
            if c == "\x08" and not self.wordBeingConstructed.isEmpty():
                self.wordBeingConstructed = self.wordBeingConstructed[0:len(self.wordBeingConstructed) - 1:1]
            # Play word
            if c == "\r":
                word_to_play = PlayWord(self.wordBeingConstructed, self.boardCursor, boardCursorDirection, self.board)
                word_to_play.play(self.board, self.board.getCurrentPlayer())
                if self.board.gameIsOver():
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
                        if self.handCursor >= self.board.getHand().size():
                            self.handCursor -= 1

                    # Toggle letter
                    if c == " ":
                        self.tilesToDiscard[self.handCursor] = not self.tilesToDiscard[self.handCursor]
                    # Exchange/pass
                    if c == "Enter":
                        self.board.exchange(self.tiles_to_Exchange)
                        if self.board.gameIsOver():
                            self.mode = 4
                        else:
                            self.mode = 3
                elif self.mode == 2:
                    if c == "Enter":
                        self.enterBoardMode()

    # Runs the game.
    def run(self):
        StdDraw.setCanvasSize(805, 525)
        StdDraw.setXscale(-1.5, 23.5)
        StdDraw.setY_scale(-1.5, 15.5)
        self.boardCursor = CENTER
        self.boardCursorDirection = HORIZONTAL
        self.draw()
        while self.mode != self.Mode.GAME_OVER:
            if self.mode == self.Mode.AI_PLAYING:
                self.draw()
                place = self.ai.chooseMove().play(self.board, 0)
                if place is not None:
                    self.boardCursor = place[0]
                    self.boardCursorDirection = place[1]
                elif self.board.gameIsOver():
                    self.mode = self.Mode.GAME_OVER
                else:
                    self.enterBoardMode()
                self.draw()
            else:
                self.handleKeyPress()
                self.draw()


def _main():
    Game.run(Game())


if __name__ == '__main__':
    _main()
