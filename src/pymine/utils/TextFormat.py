import re, json


class TextFormat(object):
    ESCAPE = "\xc2\xa7"  # ยง

    BLACK = ESCAPE + "0"
    DARK_BLUE = ESCAPE + "1"
    DARK_GREEN = ESCAPE + "2"
    DARK_AQUA = ESCAPE + "3"
    DARK_RED = ESCAPE + "4"
    DARK_PURPLE = ESCAPE + "5"
    GOLD = ESCAPE + "6"
    GRAY = ESCAPE + "7"
    DARK_GRAY = ESCAPE + "8"
    BLUE = ESCAPE + "9"
    GREEN = ESCAPE + "a"
    AQUA = ESCAPE + "b"
    RED = ESCAPE + "c"
    LIGHT_PURPLE = ESCAPE + "d"
    YELLOW = ESCAPE + "e"
    WHITE = ESCAPE + "f"

    OBFUSCATED = ESCAPE + "k"
    BOLD = ESCAPE + "l"
    STRIKETHROUGH = ESCAPE + "m"
    UNDERLINE = ESCAPE + "n"
    ITALIC = ESCAPE + "o"
    RESET = ESCAPE + "r"

    """
    Splits the string by Format tokens
    :param string: String
    :return: array
    """

    def tokenize(self, s):
        return re.split("/(" + self.ESCAPE + "[0123456789abcdefklmnor])/", s, -1)

    """
    Cleans the string from Minecraft codes and ANSI Escape Codes
    :param s: String
    :param rmFormat: bool
    :return: mixed
    """

    def clean(self, s, rmFormat=True):
        if rmFormat:
            return re.sub(self.ESCAPE, "",
                          re.sub(["/" + self.ESCAPE + "[0123456789abcdefklmnor]/", "/\x1b[\\(\\][[0-9\\[\\(]+[Bm]/"],
                                 "", s))
        return re.sub("\x1b", "", re.sub("/\x1b[\\(\\][[0-9\\[\\(]+[Bm]/", "", s))

    def isset(self, variable):
        return variable in locals() or variable in globals()

    is_array = lambda var: isinstance(var, (list, tuple))

    """
    Returns an JSON-formatted string with colors/markup
    :param s: String|array
    :return: String
    """

    def toJSON(self, s):
        if self.is_array(s):
            s = self.tokenize(s)
        newString = []
        pointer = newString[:]
        color = "white"
        bold = False
        italic = False
        underlined = False
        strikethrough = False
        obfuscated = False
        index = 0

        for token in s:
            if self.isset(pointer["text"]):
                if not self.isset(newString["extra"]):
                    newString["extra"] = []
                newString["extra"][index] = []
                pointer = newString["extra"][index][:]
                if color != "white":
                    pointer["color"] = color
                if bold != False:
                    pointer["bold"] = True
                if italic != False:
                    pointer["italic"] = True
                if underlined != False:
                    pointer["underlined"] = True
                if strikethrough != False:
                    pointer["strikethrough"] = True
                if obfuscated != False:
                    pointer["obfuscated"] = True
                ++index

            if token == self.BOLD:
                if bold == False:
                    pointer["bold"] = True
                    bold = True
            elif token == self.OBFUSCATED:
                if obfuscated == False:
                    pointer["obfuscated"] = True
                    obfuscated = True
            elif token == self.ITALIC:
                if italic == False:
                    pointer["italic"] = True
                    italic = True
            elif token == self.UNDERLINE:
                if underlined == False:
                    pointer["underlined"] = True
                    underlined = True
            elif token == self.STRIKETHROUGH:
                if strikethrough == False:
                    pointer["strikethrough"] = True
                    strikethrough = True
            elif token == self.RESET:
                if color != "white":
                    pointer["color"] = "white"
                    color = "white"
                if bold != False:
                    pointer["bold"] = False
                    bold = False
                if obfuscated != False:
                    pointer["obfuscated"] = False
                    obfuscated = False
                if italic != False:
                    pointer["italic"] = False
                    italic = False
                if underlined != False:
                    pointer["underlined"] = False
                    underlined = False
                if strikethrough != False:
                    pointer["strikethrough"] = False
                    strikethrough = False
            elif token == self.BLACK:
                pointer["color"] = "black"
                color = "black"
            elif token == self.DARK_BLUE:
                pointer["color"] = "dark_blue"
                color = "dark_blue"
            elif token == self.DARK_GREEN:
                pointer["color"] = "dark_green"
                color = "dark_green"
            elif token == self.DARK_AQUA:
                pointer["color"] = "dark_aqua"
                color = "dark_aqua"
            elif token == self.DARK_RED:
                pointer["color"] = "dark_red"
                color = "dark_red"
            elif token == self.DARK_PURPLE:
                pointer["color"] = "dark_purple"
                color = "dark_purple"
            elif token == self.GOLD:
                pointer["color"] = "gold"
                color = "gold"
            elif token == self.GRAY:
                pointer["color"] = "gray"
                color = "gray"
            elif token == self.DARK_GRAY:
                pointer["color"] = "dark_gray"
                color = "dark_gray"
            elif token == self.BLUE:
                pointer["color"] = "blue"
                color = "blue"
            elif token == self.GREEN:
                pointer["color"] = "green"
                color = "green"
            elif token == self.AQUA:
                pointer["color"] = "aqua"
                color = "aqua"
            elif token == self.RED:
                pointer["color"] = "red"
                color = "red"
            elif token == self.LIGHT_PURPLE:
                pointer["color"] = "light_purple"
                color = "light_purple"
            elif token == self.YELLOW:
                pointer["color"] = "yellow"
                color = "yellow"
            elif token == self.WHITE:
                pointer["color"] = "white"
                color = "white"
            else:
                pointer["text"] = token
        if self.isset(newString["extra"]):
            for k, d in newString["extra"]:
                if not self.isset(d["extra"]):
                    del newString["extra"][k]
        return json.dumps(newString)

    def str_repeat(self, the_str, multiplier):
        return the_str * multiplier

    """
    Returns an HTML-formatted string with colors/markup
    :param s: String|array
    :return: String
    """

    def toHTML(self, s):
        if not self.is_array(s):
            s = self.tokenize(s)
        newString = ""
        tokens = 0
        for token in s:
            if token == self.BOLD:
                newString += "<span style=font-weight:bold>"
                ++tokens
            elif token == self.ITALIC:
                newString += "<span style=font-style:italic>"
                ++tokens
            elif token == self.UNDERLINE:
                newString += "<span style=text-decoration:underline>"
                ++tokens
            elif token == self.STRIKETHROUGH:
                newString += "<span style=text-decoration:line-through>"
                ++tokens
            elif token == self.RESET:
                newString += self.str_repeat("</span>", tokens)
                tokens = 0

            elif token == self.BLACK:
                newString += "<span style=color:#000>"
                ++tokens
            elif token == self.DARK_BLUE:
                newString += "<span style=color:#00A>"
                ++tokens
            elif token == self.DARK_GREEN:
                newString += "<span style=color:#0A0>"
                ++tokens
            elif token == self.DARK_AQUA:
                newString += "<span style=color:#0AA>"
                ++tokens
            elif token == self.DARK_RED:
                newString += "<span style=color:#A00>"
                ++tokens
            elif token == self.DARK_PURPLE:
                newString += "<span style=color:#A0A>"
                ++tokens
            elif token == self.GOLD:
                newString += "<span style=color:#FA0>"
                ++tokens
            elif token == self.GRAY:
                newString += "<span style=color:#AAA>"
                ++tokens
            elif token == self.DARK_GRAY:
                newString += "<span style=color:#555>"
                ++tokens
            elif token == self.BLUE:
                newString += "<span style=color:#55F>"
                ++tokens
            elif token == self.GREEN:
                newString += "<span style=color:#5F5>"
                ++tokens
            elif token == self.AQUA:
                newString += "<span style=color:#5FF>"
                ++tokens
            elif token == self.RED:
                newString += "<span style=color:#F55>"
                ++tokens
            elif token == self.LIGHT_PURPLE:
                newString += "<span style=color:#F5F>"
                ++tokens
            elif token == self.YELLOW:
                newString += "<span style=color:#FF5>"
                ++tokens
            elif token == self.WHITE:
                newString += "<span style=color:#FFF>"
                ++tokens
            else:
                newString += token

        newString += self.str_repeat("</span>", self.tokens)
        return newString

    """
    Returns an ANSI-formatted string with colors/markup
    :param s: String|array
    :return: String
    """

    def toANSI(self, s):
        if not self.is_array(s):
            s = self.tokenize(s)

        newString = ""
        for token in s:
            if token == self.BOLD:
                newString += "\033[1m"
            elif token == self.OBFUSCATED:
                newString += "\033[0m"
            elif token == self.ITALIC:
                newString += "\033[3m"
            elif token == self.UNDERLINE:
                newString += "\033[4m"
            elif token == self.STRIKETHROUGH:
                newString += "\033[0m"
            elif token == self.RESET:
                newString += self.str_repeat("</span>", self.tokens)
                tokens = 0

            # Colors
            elif token == self.BLACK:
                newString += "\033[30m"
            elif token == self.DARK_BLUE:
                newString += "\033[34m"
            elif token == self.DARK_GREEN:
                newString += "\033[32m"
            elif token == self.DARK_AQUA:
                newString += "\033[36m"
            elif token == self.DARK_RED:
                newString += "\033[31m"
            elif token == self.DARK_PURPLE:
                newString += "\033[35m"
            elif token == self.GOLD:
                newString += "\033[43m"
            elif token == self.GRAY:
                newString += "\033[37m"
            elif token == self.DARK_GRAY:
                newString += "\033[40m"
            elif token == self.BLUE:
                newString += "\033[44m"
            elif token == self.GREEN:
                newString += "\033[42m"
            elif token == self.AQUA:
                newString += "\033[46m"
            elif token == self.RED:
                newString += "\033[41m"
            elif token == self.LIGHT_PURPLE:
                newString += "\033[45m"
            elif token == self.YELLOW:
                newString += "\033[43m"
            elif token == self.WHITE:
                newString += "\033[47m"
            else:
                newString += token
        return newString
