#
# Player that can choose moves for Scrabble.
#
from abc import ABCMeta


class ScrabbleAI(object):
    __metaclass__ = ABCMeta

    # Sets the GateKeeper for the next move. Note that, in a tournament, this may be from a
    # completely new game; each move should be generated independently.
    def setGateKeeper(self, gateKeeper):
        raise NotImplementedError()

    # Returns a good move given the state of the game (accessed through the GateKeeper).
    def chooseMove(self):
        raise NotImplementedError()
