# # Scrabble AI player that plays up to 4 tiles per turn other than the first
# # Code by Ben Schulman
#
# # Scrabble board, maintaining bag, players' hands, and other game logic.
#
# # General conventions:
#
# # Each square is either a lower-case letter (a regular tile), an upper-case letter (a played blank), or a symbol.
#
# # Each bag/hand tile is either a lower-case letter (a regular tile) or _ (an unplayed blank).
#
# # Words submitted consist of letters (upper-case for played blanks) and spaces (existing tiles on the board).
# import random
# from collections import namedtuple
#
# import Board
# import StdDraw
# from Location import CENTER as CENTER
# from Location import HORIZONTAL as HORIZONTAL
# from PlayWord import PlayWord, removeTiles
# from Scrabble import Game as Game
#
#
#
#
# #
#
#
#
# # # Intermediary between a ScrabbleAI and a Board, allowing the former to get information it needs without allowing
# # full access.
#
#
# Color = namedtuple('RGB', 'red, green, blue')
# colors = {}  # dict of colors
#
#
# # class RGB(Color):
# #     def hex_format(self):
# #         # Returns color in hex format
# #         return '#{:02X}{:02X}{:02X}'.format(self.red, self.green, self.blue)
#
#
#     #
#     # Handles a key pressed by the user.
#     #
#
#
#
#     # Runs the game. Crashes if the AI opponent plays an illegal move.
#     def run(self):
#         self.board.deal()
#         self.board.currentPlayer = 1
#
#         # StdDraw.enableDoubleBuffering()
#
#         self.draw()
#         # print("here")
#         while self.mode != 4:
#             if self.mode == 3:
#                 self.draw()
#                 place = self.ai.chooseMove().play(self.board, 0)
#                 if place:
#                     self.boardCursor = place
#                     self.boardCursorDirection = place
#                 if Board.gameIsOver(self.board):
#                     self.mode = 4
#                 else:
#                     self.enterBoardMode()
#                     self.draw()
#             else:
#                 self.handleKeyPress()
#                 self.draw()
#
# # print("Hello World")
# Game().run()
# # print("Hello World")
# # if __name__ == "__init__":
# # init()
