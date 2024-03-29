"""
stddraw.py

The stddraw module defines functions that allow the user to create a
drawing.  A drawing appears on the canvas.  The canvas appears
in the window.  As a convenience, the module also imports the
commonly used Color objects defined in the color module.
"""

import os
import sys
import time

import pygame
import pygame.font
import pygame.gfxdraw

if sys.hexversion < 0x03000000:
    import tkinter
    import tkinter.filedialog
else:
    import tkinter.messagebox as messagebox
    import tkinter.filedialog as tk_file_dialog

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'


# keystyped = []
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------

class Color:
    """
    A Color object models an RGB color.
    """

    # -------------------------------------------------------------------

    def __init__(self, r=0, g=0, b=0):
        """
        Construct self such that it has the given red (r),
        green (g), and blue (b) components.
        """
        # print("Jello World")
        self._r = r  # Red component
        self._g = g  # Green component
        self._b = b  # Blue component

    # -------------------------------------------------------------------

    def getRed(self):
        """
        Return the red component of self.
        """
        return self._r

    # -------------------------------------------------------------------

    def getGreen(self):
        """
        Return the green component of self.
        """
        return self._g

    # -------------------------------------------------------------------

    def getBlue(self):
        """
        Return the blue component of self.
        """
        return self._b

    # -------------------------------------------------------------------

    def __str__(self):
        """
        Return the string equivalent of self, that is, a
        string of the form '(r, g, b)'.
        """
        # return '#%02x%02x%02x' % (self._r, self._g, self._b)
        return '(' + str(self._r) + ', ' + str(self._g) + ', ' + \
               str(self._b) + ')'


# -----------------------------------------------------------------------

# Some predefined Color objects:

WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)

RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)

CYAN = Color(0, 255, 255)
MAGENTA = Color(255, 0, 255)
YELLOW = Color(255, 255, 0)
TABLE_COLOR = Color(24, 64, 35)
TILE_COLOR = Color(251, 224, 174)

DARK_RED = Color(128, 0, 0)
DARK_GREEN = Color(0, 128, 0)
DARK_BLUE = Color(0, 0, 128)

GRAY = Color(128, 128, 128)
DARK_GRAY = Color(64, 64, 64)
LIGHT_GRAY = Color(192, 192, 192)

ORANGE = Color(255, 200, 0)
VIOLET = Color(238, 130, 238)
PINK = Color(255, 175, 175)

# Shade of blue used in Introduction to Programming in Java.
# It is Pantone 300U. The RGB values are approximately (9, 90, 166).
BOOK_BLUE = Color(9, 90, 166)
BOOK_LIGHT_BLUE = Color(103, 198, 243)

# Shade of red used in Algorithms 4th edition
BOOK_RED = Color(150, 35, 31)

# -----------------------------------------------------------------------
'''
def color():
    """
    For testing:
    """
    import stdio
    c1 = Color(128, 128, 128)
    stdio.writeln(c1)
    stdio.writeln(c1.getRed())
    stdio.writeln(c1.getGreen())
    stdio.writeln(c1.getBlue())

if __name__ == '__main__':
    _main()
'''
# -----------------------------------------------------------------------

# Default Sizes and Values

_BORDER = 0.0
# _BORDER = 0.05
_DEFAULT_X_MIN = 0.0
_DEFAULT_X_MAX = 1.0
_DEFAULT_Y_MIN = 0.0
_DEFAULT_Y_MAX = 1.0
_DEFAULT_CANVAS_SIZE = 512
_DEFAULT_PEN_RADIUS = .005  # Maybe change this to 0.0 in the future.
_DEFAULT_PEN_COLOR = BLACK

_DEFAULT_FONT_FAMILY = 'Helvetica'
_DEFAULT_FONT_SIZE = 12

_x_min = 0
_y_min = 0
_x_max = 0
_y_max = 0

_fontFamily = _DEFAULT_FONT_FAMILY
_fontSize = _DEFAULT_FONT_SIZE

_canvasWidth = float(_DEFAULT_CANVAS_SIZE)
_canvasHeight = float(_DEFAULT_CANVAS_SIZE)
_penRadius = 0
_penColor = _DEFAULT_PEN_COLOR
keysTyped = ['']

# Has the window been created?
_windowCreated = False

# Keep track of mouse status

# Has the mouse been left-clicked since the last time we checked?
_mousePressed = False


def _pygameColor(c):
    """
    Convert c, an object of type color.Color, to an equivalent object
    of type pygame.Color.  Return the result.
    """
    # r = c.getRed()
    # g =
    # b =
    return pygame.Color(c.getRed(), c.getGreen(), c.getBlue())


# -----------------------------------------------------------------------

# Private functions to scale and factor X and Y values.

def _scaleX(x):
    return _canvasWidth * (x - _x_min) / (_x_max - _x_min)


def _scaleY(y):
    return _canvasHeight * (_y_max - y) / (_y_max - _y_min)


def _factorX(w):
    return w * _canvasWidth / abs(_x_max - _x_min)


def _factorY(h):
    return h * _canvasHeight / abs(_y_max - _y_min)


def _userX(x):
    return _x_min + x * (_x_max - _x_min) / _canvasWidth


def _userY(y):
    return _y_max - y * (_y_max - _y_min) / _canvasHeight


def setCanvasSize(w=_DEFAULT_CANVAS_SIZE, h=_DEFAULT_CANVAS_SIZE):
    """
    Set the size of the canvas to w pixels wide and h pixels high.
    Calling this function is optional. If you call it, you must do
    so before calling any drawing function.
    """

    global _surface
    global _canvasWidth
    global _canvasHeight
    global _windowCreated
    # noinspection PyGlobalUndefined
    global _background

    if _windowCreated:
        raise Exception('The std draw window already was created')

    if (w < 1) or (h < 1):
        raise Exception('width and height must be positive')

    _canvasWidth = w
    _canvasHeight = h
    _background = pygame.display.set_mode([w, h])
    pygame.display.set_caption('std draw window (r-click to save)')
    _surface = pygame.Surface((w, h))
    _surface.fill(_pygameColor(WHITE))
    _windowCreated = True


def setXscale(minimum=_DEFAULT_X_MIN, maximum=_DEFAULT_X_MAX):
    """
    Set the x-scale of the canvas such that the minimum x value
    is min and the maximum x value is max.
    """
    global _x_min
    global _x_max
    minimum = float(minimum)
    maximum = float(maximum)
    if minimum >= maximum:
        raise Exception('min must be less than max')
    size = maximum - minimum
    _x_min = minimum - _BORDER * size
    _x_max = maximum + _BORDER * size


def setY_scale(minimum=_DEFAULT_Y_MIN, maximum=_DEFAULT_Y_MAX):
    """
    Set the y-scale of the canvas such that the minimum y value
    is min and the maximum y value is max.
    """
    global _y_min
    global _y_max
    minimum = float(minimum)
    maximum = float(maximum)
    if minimum >= maximum:
        raise Exception('min must be less than max')
    size = maximum - minimum
    _y_min = minimum - _BORDER * size
    _y_max = maximum + _BORDER * size


def setPenRadius(r=_DEFAULT_PEN_RADIUS):
    """
    Set the pen radius to r, thus affecting the subsequent drawing
    of points and lines. If r is 0.0, then points will be drawn with
    the minimum possible radius and lines with the minimum possible
    width.
    """
    global _penRadius
    r = float(r)
    if r < 0.0:
        raise Exception('Argument to setPenRadius() must be non-neg')
    _penRadius = r * float(_DEFAULT_CANVAS_SIZE)


def setPenColor(c):
    """
    Set the pen color to c, where c is an object of class color.Color.
    c defaults to std draw.BLACK.
    """
    global _penColor
    _penColor = c


def setFontFamily(f=_DEFAULT_FONT_FAMILY):
    """
    Set the font family to f (e.g. 'Helvetica' or 'Courier').
    """
    global _fontFamily
    _fontFamily = f


def setFontSize(s=_DEFAULT_FONT_SIZE):
    """
    Set the font size to s (e.g. 12 or 16).
    """
    global _fontSize
    _fontSize = s


# -----------------------------------------------------------------------

def _makeSureWindowCreated():
    global _windowCreated
    if not _windowCreated:
        setCanvasSize()
        _windowCreated = True


# -----------------------------------------------------------------------

# Functions to draw shapes, text, and images on the background canvas.

def _pixel(x, y):
    """
    Draw on the background canvas a pixel at (x, y).
    """
    _makeSureWindowCreated()
    xs = _scaleX(x)
    xy = _scaleY(y)
    pygame.gfxdraw.pixel(
        _surface,
        int(round(xs)),
        int(round(xy)),
        _pygameColor(_penColor))


def point(x, y):
    """
    Draw on the background canvas a point at (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    # If the radius is too small, then simply draw a pixel.
    if _penRadius <= 1.0:
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(
            _surface,
            _pygameColor(_penColor),
            pygame.Rect(xs - _penRadius, ys - _penRadius, _penRadius * 2.0, _penRadius * 2.0), 0)


def filledCircle(x, y, r):
    """
    Draw on the background canvas a filled circle of radius r
    centered on (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factorX(2.0 * r)
    hs = _factorY(2.0 * r)
    # If the radius is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(_surface, _pygameColor(_penColor), pygame.Rect(xs - ws / 2.0, ys - hs / 2.0, ws, hs), 0)


def _thickLine(x0, y0, x1, y1, r):
    """
    Draw on the background canvas a line from (x0, y0) to (x1, y1).
    Draw the line with a pen whose radius is r.
    """
    xs0 = _scaleX(x0)
    ys0 = _scaleY(y0)
    xs1 = _scaleX(x1)
    ys1 = _scaleY(y1)
    if abs(xs0 - xs1) < 1.0 and abs(ys0 - ys1) < 1.0:
        filledCircle(x0, y0, r)
        return
    xMid = (xs0 + xs1) / 2
    yMid = (ys0 + ys1) / 2
    _thickLine(x0, y0, xMid, yMid, r)
    _thickLine(xMid, yMid, x1, y1, r)


def line(x0, y0, x1, y1):
    """
    Draw on the background canvas a line from (x0, y0) to (x1, y1).
    """

    THICK_LINE_CUTOFF = 3  # pixels

    _makeSureWindowCreated()

    x0 = float(x0)
    y0 = float(y0)
    x1 = float(x1)
    y1 = float(y1)

    lineWidth = _penRadius * 2.0
    if lineWidth == 0.0:
        lineWidth = 1.0
    if lineWidth < THICK_LINE_CUTOFF:
        x0s = _scaleX(x0)
        y0s = _scaleY(y0)
        x1s = _scaleX(x1)
        y1s = _scaleY(y1)
        pygame.draw.line(
            _surface,
            _pygameColor(_penColor),
            (x0s, y0s),
            (x1s, y1s),
            int(round(lineWidth)))
    else:
        _thickLine(x0, y0, x1, y1, _penRadius / _DEFAULT_CANVAS_SIZE)


def circle(x, y, r):
    """
    Draw on the background canvas a circle of radius r centered on
    (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    r = float(r)
    ws = _factorX(2.0 * r)
    hs = _factorY(2.0 * r)
    # If the radius is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.ellipse(_surface, _pygameColor(_penColor), pygame.Rect(xs - ws / 2.0, ys - hs / 2.0, ws, hs),
                            int(round(_penRadius)))


def rectangle(x, y, w, h):
    """
    Draw on the background canvas a rectangle of width w and height h
    whose lower left point is (x, y).
    """
    global _surface
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    ws = _factorX(w)
    hs = _factorY(h)
    # If the rectangle is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.rect(_surface, _pygameColor(_penColor), pygame.Rect(xs, ys - hs, ws, hs), int(round(_penRadius)))


def filledRectangle(x, y, w, h):
    """
    Draw on the background canvas a filled rectangle of width w and
    height h whose lower left point is (x, y).
    """
    global _surface
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    w = float(w)
    h = float(h)
    ws = _factorX(w)
    hs = _factorY(h)
    # If the rectangle is too small, then simply draw a pixel.
    if (ws <= 1.0) and (hs <= 1.0):
        _pixel(x, y)
    else:
        xs = _scaleX(x)
        ys = _scaleY(y)
        pygame.draw.rect(_surface, _pygameColor(_penColor), pygame.Rect(xs, ys - hs, ws, hs), 0)


def square(x, y, r):
    """
    Draw on the background canvas a square whose sides are of length
    2r, centered on (x, y).
    """
    _makeSureWindowCreated()
    rectangle(x - r, y - r, 2.0 * r, 2.0 * r)


def filledSquare(x, y, r):
    """
    Draw on the background canvas a filled square whose sides are of
    length 2r, centered on (x, y).
    """
    _makeSureWindowCreated()
    filledRectangle(x - r, y - r, 2.0 * r, 2.0 * r)


def polygon(x, y):
    """
    Draw on the background canvas a polygon with coordinates
    (x[i], y[i]).
    """
    global _surface
    _makeSureWindowCreated()
    # Scale X and Y values.
    xScaled = []
    for xi in x:
        xScaled.append(_scaleX(float(xi)))
    yScaled = []
    for yi in y:
        yScaled.append(_scaleY(float(yi)))
    points = []
    for i in range(len(x)):
        points.append((xScaled[i], yScaled[i]))
    points.append((xScaled[0], yScaled[0]))
    pygame.draw.polygon(
        _surface,
        _pygameColor(_penColor),
        points,
        int(round(_penRadius)))


def filledPolygon(x, y):
    """
    Draw on the background canvas a filled polygon with coordinates
    (x[i], y[i]).
    """
    global _surface
    _makeSureWindowCreated()
    # Scale X and Y values.
    xScaled = []
    for xi in x:
        xScaled.append(_scaleX(float(xi)))
    yScaled = []
    for yi in y:
        yScaled.append(_scaleY(float(yi)))
    points = []
    for i in range(len(x)):
        points.append((xScaled[i], yScaled[i]))
    points.append((xScaled[0], yScaled[0]))
    pygame.draw.polygon(_surface, _pygameColor(_penColor), points, 0)


def text(x, y, s):
    """
    Draw string s on the background canvas centered at (x, y).
    """
    _makeSureWindowCreated()
    x = float(x)
    y = float(y)
    xs = _scaleX(x)
    ys = _scaleY(y)
    font = pygame.font.SysFont(_fontFamily, _fontSize)
    temp_text = font.render(s, True, _pygameColor(_penColor))
    text_position = temp_text.get_rect(center=(xs, ys))
    _surface.blit(temp_text, text_position)


global _surface


def picture(pic, x=None, y=None):
    """
    Draw pic on the background canvas centered at (x, y).  pic is an
    object of class picture.Picture. x and y default to the midpoint
    of the background canvas.
    """

    _makeSureWindowCreated()
    # By default, draw pic at the middle of the surface.
    if x is None:
        x = (_x_max + _x_min) / 2.0
    if y is None:
        y = (_y_max + _y_min) / 2.0
    x = float(x)
    y = float(y)
    xs = _scaleX(x)
    ys = _scaleY(y)
    ws = pic.width()
    hs = pic.height()
    picSurface = pic._surface  # violates encapsulation
    _surface.blit(picSurface, [xs - ws / 2.0, ys - hs / 2.0, ws, hs])


def clear(c=WHITE):
    """
    Clear the background canvas to color c, where c is an
    object of class color.Color. c defaults to stddraw.WHITE.
    """
    _makeSureWindowCreated()
    _surface.fill(_pygameColor(c))


def save(f):
    """
    Save the window canvas to file f.
    """
    _makeSureWindowCreated()

    # if sys.hexversion >= 0x03000000:
    #    # Hack because Pygame without full image support
    #    # can handle only .bmp files.
    #    bmpFileName = f + '.bmp'
    #    pygame.image.save(_surface, bmpFileName)
    #    os.system('convert ' + bmpFileName + ' ' + f)
    #    os.system('rm ' + bmpFileName)
    # else:
    #    pygame.image.save(_surface, f)

    pygame.image.save(_surface, f)


# -----------------------------------------------------------------------

def _show():
    """
    Copy the background canvas to the window canvas.
    """
    _background.blit(_surface, (0, 0))
    pygame.display.flip()
    # _checkForEvents()


# def _showAndWaitForever():
#     """
#     Copy the background canvas to the window canvas. Then wait
#     forever, that is, until the user closes the stddraw window.
#     """
#     _makeSureWindowCreated()
#     _show()
#     QUANTUM = .1
#     # print("here")
#     checkForEvents()
#     while True:
#         time.sleep(QUANTUM)


def show(msec=float('inf')):
    """
    Copy the background canvas to the window canvas, and
    then wait for msec milliseconds. msec defaults to infinity.
    """
    # if msec == float('inf'):
    #     _showAndWaitForever()

    _makeSureWindowCreated()
    # print("showing")
    _show()
    # print("made it past _show()")
    # checkForEvents()

    # Sleep for the required time, but check for events every
    # QUANTUM seconds.
    QUANTUM = 1
    sec = msec / 1000.0
    if sec < QUANTUM:
        time.sleep(sec)
    # secondsWaited = 0.0
    # while secondsWaited < sec:


#        time.sleep(QUANTUM)
# secondsWaited += QUANTUM
# if hasNextKeyTyped():
#     return


# -----------------------------------------------------------------------

def _saveToFile():
    """
    Display a dialog box that asks the user for a file name.  Save the
    drawing to the specified file.  Display a confirmation dialog box
    if successful, and an error dialog box otherwise.  The dialog boxes
    are displayed using Tkinter, which (on some computers) is
    incompatible with Pygame. So the dialog boxes must be displayed
    from child processes.
    """
    import subprocess
    _makeSureWindowCreated()

    stddrawPath = os.path.realpath(__file__)

    childProcess = subprocess.Popen(
        [sys.executable, stddrawPath, 'getFileName'],
        stdout=subprocess.PIPE)
    so, se = childProcess.communicate()
    fileName = so.strip()

    if sys.hexversion >= 0x03000000:
        fileName = fileName.decode('utf-8')

    if fileName == '':
        return

    if not fileName.endswith(('.jpg', '.png')):
        subprocess.Popen(
            [sys.executable, stddrawPath, 'reportFileSaveError',
             'File name must end with ".jpg" or ".png".'])
        return

    try:
        save(fileName)
        subprocess.Popen(
            [sys.executable, stddrawPath, 'confirmFileSave'])
    except pygame.error as e:
        subprocess.Popen(
            [sys.executable, stddrawPath, 'reportFileSaveError', str(e)])


# -----------------------------------------------------------------------

# Functions for retrieving keys

def hasNextKeyTyped():
    """
    Return True if the queue of keys the user typed is not empty.
    Otherwise, return False.
    """

    return keysTyped is not []


def nextKeyTyped():
    """
    Remove the first key from the queue of keys that the user typed,
    and return that key.
    """

    return keysTyped.pop()


# -----------------------------------------------------------------------
# Begin added by Alan J. Broder
# -----------------------------------------------------------------------

# Functions for dealing with mouse clicks

def mousePressed():
    """
    Return True if the mouse has been left-clicked since the
    last time mousePressed was called, and False otherwise.
    """
    global _mousePressed
    if _mousePressed:
        _mousePressed = False
        return True
    return False


def mouseX():
    """
    Return the x coordinate in user space of the location at
    which the mouse was most recently left-clicked. If a left-click
    hasn't happened yet, raise an exception, since mouseX() shouldn't
    be called until mousePressed() returns True.
    """

    if _mousePos:
        return _userX(_mousePos[0])
    raise Exception(
        "Can't determine mouse position if a click hasn't happened")


def mouseY():
    """
    Return the y coordinate in user space of the location at
    which the mouse was most recently left-clicked. If a left-click
    hasn't happened yet, raise an exception, since mouseY() shouldn't
    be called until mousePressed() returns True.
    """
    global _mousePos
    if _mousePos:
        return _userY(_mousePos[1])
    raise Exception(
        "Can't determine mouse position if a click hasn't happened")


# -----------------------------------------------------------------------
# End added by Alan J. Broder
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------

# Initialize the x scale, the y scale, and the pen radius.

setXscale()
setY_scale()
setPenRadius()
pygame.font.init()


# -----------------------------------------------------------------------

# Functions for displaying Tkinter dialog boxes in child processes.

def _getFileName():
    """
    Display a dialog box that asks the user for a file name.
    """
    root = tkinter.Tk()
    root.withdraw()
    reply = tk_file_dialog.asksaveasfilename(initialdir='.')
    sys.stdout.write(reply)
    sys.stdout.flush()
    sys.exit()


def _confirmFileSave():
    """
    Display a dialog box that confirms a file save operation.
    """
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showinfo(title='File Save Confirmation',
                        message='The drawing was saved to the file.')
    sys.exit()


def _reportFileSaveError(msg):
    """
    Display a dialog box that reports a msg.  msg is a string which
    describes an error in a file save operation.
    """
    root = tkinter.Tk()
    root.withdraw()
    messagebox.showerror(title='File Save Error', message=msg)
    sys.exit()


# -----------------------------------------------------------------------

def _regressionTest():
    """
    Perform regression testing.
    """

    clear()

    setPenRadius(.5)
    setPenColor(ORANGE)
    point(0.5, 0.5)
    show(0.0)

    setPenRadius(.25)
    setPenColor(BLUE)
    point(0.5, 0.5)
    show(0.0)

    setPenRadius(.02)
    setPenColor(RED)
    point(0.25, 0.25)
    show(0.0)

    setPenRadius(.01)
    setPenColor(GREEN)
    point(0.25, 0.25)
    show(0.0)

    setPenRadius(0)
    setPenColor(BLACK)
    point(0.25, 0.25)
    show(0.0)

    setPenRadius(.1)
    setPenColor(RED)
    point(0.75, 0.75)
    show(0.0)

    setPenRadius(0)
    setPenColor(CYAN)
    for i in range(0, 100):
        point(i / 512.0, .5)
        point(.5, i / 512.0)
    show(0.0)

    setPenRadius(0)
    setPenColor(MAGENTA)
    line(.1, .1, .3, .3)
    line(.1, .2, .3, .2)
    line(.2, .1, .2, .3)
    show(0.0)

    setPenRadius(.05)
    setPenColor(MAGENTA)
    line(.7, .5, .8, .9)
    show(0.0)

    setPenRadius(.01)
    setPenColor(YELLOW)
    circle(.75, .25, .2)
    show(0.0)

    setPenRadius(.01)
    setPenColor(YELLOW)
    filledCircle(.75, .25, .1)
    show(0.0)

    setPenRadius(.01)
    setPenColor(PINK)
    rectangle(.25, .75, .1, .2)
    show(0.0)

    setPenRadius(.01)
    setPenColor(PINK)
    filledRectangle(.25, .75, .05, .1)
    show(0.0)

    setPenRadius(.01)
    setPenColor(DARK_RED)
    square(.5, .5, .1)
    show(0.0)

    setPenRadius(.01)
    setPenColor(DARK_RED)
    filledSquare(.5, .5, .05)
    show(0.0)

    setPenRadius(.01)
    setPenColor(DARK_BLUE)
    polygon([.4, .5, .6], [.7, .8, .7])
    show(0.0)

    setPenRadius(.01)
    setPenColor(DARK_GREEN)
    setFontSize(24)
    text(.2, .4, 'hello, world')
    show(0.0)

    # import picture as p
    # pic = p.Picture('saveIcon.png')
    # picture(pic, .5, .85)
    # show(0.0)

    # Test handling of mouse and keyboard events.
    setPenColor(BLACK)
    import stdio
    stdio.writeln('Left click with the mouse or type a key')
    while True:
        if mousePressed():
            filledCircle(mouseX(), mouseY(), .02)
        if hasNextKeyTyped():
            stdio.write(nextKeyTyped())
        show(0.0)


# -----------------------------------------------------------------------

def _main():
    """
    Dispatch to a function that does regression testing, or to a
    dialog-box-handling function.
    """
    import sys
    if len(sys.argv) == 1:
        _regressionTest()
    elif sys.argv[1] == 'getFileName':
        _getFileName()
    elif sys.argv[1] == 'confirmFileSave':
        _confirmFileSave()
    elif sys.argv[1] == 'reportFileSaveError':
        _reportFileSaveError(sys.argv[2])


if __name__ == '__main__':
    _main()

# Adapted from Robert Sedgewick, Kevin Wayne, and Robert Dondero.
