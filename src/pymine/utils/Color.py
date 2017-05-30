
class Color:
    COLOR_DYE_BLACK = 0 #dye colors
    COLOR_DYE_RED = 1
    COLOR_DYE_GREEN = 2
    COLOR_DYE_BROWN = 3
    COLOR_DYE_BLUE = 4
    COLOR_DYE_PURPLE = 5
    COLOR_DYE_CYAN = 6
    COLOR_DYE_LIGHT_GRAY = 7
    COLOR_DYE_GRAY = 8
    COLOR_DYE_PINK = 9
    COLOR_DYE_LIME = 10
    COLOR_DYE_YELLOW = 11
    COLOR_DYE_LIGHT_BLUE = 12
    COLOR_DYE_MAGENTA = 13
    COLOR_DYE_ORANGE = 14
    COLOR_DYE_WHITE = 15

    dyeColors = None

    a, r, g, b = None

    def __init__(self, r, g, b, a=0xff):
        self.r = r & 0xff
        self.g = g & 0xff
        self.b = b & 0xff
        self.a = a & 0xff

        if self.dyeColors is None:
            self.dyeColors = new
