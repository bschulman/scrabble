# Exchanging 0 or more tiles.
class ExchangeTiles:
    #
    # An array of seven booleans, indicating which tiles in the hand to exchange. Any entries beyond the length of
    # the hand are ignored.
    #

    tilesToExchange = [False] * 7

    def __init__(self):
        self.tilesToExchange = self.tilesToExchange

    def play(self, board, playerNumber):
        board.exchange(board.getHand(playerNumber), self.tilesToExchange)
        return None
