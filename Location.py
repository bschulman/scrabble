class Location(object):

    def __init__(self, row, column):
        self.row = row
        self.column = column

    def getRow(self):
        return self.row

    def getColumn(self):
        return self.column

    # Returns a new Location which is offset from this by direction. For example, a.neighbor(HORIZONTAL) is the
    # location to the right of 'a'.
    def neighbor(self):
        return Location(self.row + self.row, self.column + self.column)

    # Returns a new Location which is offset from this by the opposite of direction. For example, a.neighbor(
    # HORIZONTAL) is the location to the left of 'a'.
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
        if o is None or type(self) != type(o):
            return False
        location = Location(o.row, o.column)
        return self.row == location.row and self.column == location.column

    def hashCode(self):
        return [hash(self.row), hash(self.column)]

    def str(self):
        return 'Location{' + 'row=' + self.row + ', column=' + self.column + '}'


HORIZONTAL = Location(0, 1)

# Direction for vertical words.
VERTICAL = Location(1, 0)

# The center square (which the first move must contain).
CENTER = Location(7, 7)
