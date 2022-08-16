"""
handleKeys.py

The HandleKeys module defines functions that allow the handling of key presses
for the scrabble game.
"""

# Log of all keys typed to compare with StdDraw's:
LAST_KEY_TYPED = []

# Keys that the user might press.
KEYS = []

# Relevant keys
for c in {'a', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'x',
          'c', 'v', 'b', 'n', 'm', 'z'}:
    KEYS.append(ord(c))
KEYS.append("/")
KEYS.append("[")  # use as left
KEYS.append("]")  # use as right
KEYS.append("=")  # use as up
KEYS.append("-")  # use as down
for c in {'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X',
          'C', 'V', 'B', 'N', 'M'}:
    KEYS.append(ord(c))
KEYS.append(" ")
KEYS.append("\x08")
KEYS.append("\r")
KEYS.append("\\")  # backslash: use instead of alt


# print(self.KEYS[1])
# print(self.KEYS)


def getKeyPressed():
    # print("here")
    # print(len(StdDraw.keysTyped))
    # print(StdDraw.keysTyped[0])
    # print(len(KEYSTYPED))
    temp_key = None
    while not temp_key:
        temp_key = input()
    if temp_key is not LAST_KEY_TYPED and temp_key is not None:
        print(temp_key)
        for i in range(0, 59):
            # print(key)
            if temp_key[0] == KEYS[i]:
                print("found")
                result = KEYS[i]
                if ord('A') <= ord(KEYS[i]) <= ord('Z') and not KEYS[i] == '':
                    result = KEYS[i]
                print(result)
                return result
