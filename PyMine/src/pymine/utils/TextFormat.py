from src.pymine.maths import const
import re, json

class TextFormat(object):
	const.ESCAPE = "\xc2\xa7" #ยง

	const.BLACK = const.ESCAPE + "0"
	const.DARK_BLUE = const.ESCAPE + "1"
	const.DARK_GREEN = const.ESCAPE + "2"
	const.DARK_AQUA = const.ESCAPE + "3"
	const.DARK_RED = const.ESCAPE + "4"
	const.DARK_PURPLE = const.ESCAPE + "5"
	const.GOLD = const.ESCAPE + "6"
	const.GRAY = const.ESCAPE + "7"
	const.DARK_GRAY = const.ESCAPE + "8"
	const.BLUE = const.ESCAPE + "9"
	const.GREEN = const.ESCAPE + "a"
	const.AQUA = const.ESCAPE + "b"
	const.RED = const.ESCAPE + "c"
	const.LIGHT_PURPLE = const.ESCAPE + "d"
	const.YELLOW = const.ESCAPE + "e"
	const.WHITE = const.ESCAPE + "f"

	const.OBFUSCATED = const.ESCAPE + "k"
	const.BOLD = const.ESCAPE + "l"
	const.STRIKETHROUGH = const.ESCAPE + "m"
	const.UNDERLINE = const.ESCAPE + "n"
	const.ITALIC = const.ESCAPE + "o"
	const.RESET = const.ESCAPE + "r"


	"""
	Splits the string by Format tokens
	:param string: String
	:return: array
	"""
	def tokenize(s):
		return re.split("/(" + const.ESCAPE + "[0123456789abcdefklmnor])/", s, -1)


	"""
	Cleans the string from Minecraft codes and ANSI Escape Codes
	:param s: String
	:param rmFormat: bool
	:return: mixed
	"""
	def clean(s, rmFormat = True):
		if rmFormat:
			return re.sub(const.ESCAPE,"",re.sub(["/" + const.ESCAPE + "[0123456789abcdefklmnor]/", "/\x1b[\\(\\][[0-9\\[\\(]+[Bm]/"],"",s))
		return re.sub("\x1b","",re.sub("/\x1b[\\(\\][[0-9\\[\\(]+[Bm]/", "", s))


	def isset(variable):
		return variable in locals() or variable in globals()

	is_array = lambda var: isinstance(var, (list,tuple))

	"""
	Returns an JSON-formatted string with colors/markup
	:param s: String|array
	:return: String
	"""
	def toJSON(self, s):
		if is_array(s):
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
			if isset(pointer["text"]):
				if not isset(newString["extra"]):
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

			if token == const.BOLD:
				if bold == False:
					pointer["bold"] = True
					bold = True
			elif token == const.OBFUSCATED:
				if obfuscated == False:
					pointer["obfuscated"] = True
					obfuscated = True
			elif token == const.ITALIC:
				if italic == False:
					pointer["italic"] = True
					italic = True
			elif token == const.UNDERLINE:
				if underlined == False:
					pointer["underlined"] = True
					underlined = True
			elif token == const.STRIKETHROUGH:
				if strikethrough == False:
					pointer["strikethrough"] = True
					strikethrough = True
			elif token == const.RESET:
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
			elif token == const.BLACK:
				pointer["color"] = "black"
				color = "black"
			elif token == const.DARK_BLUE:
				pointer["color"] = "dark_blue"
				color = "dark_blue"
			elif token == const.DARK_GREEN:
				pointer["color"] = "dark_green"
				color = "dark_green"
			elif token == const.DARK_AQUA:
				pointer["color"] = "dark_aqua"
				color = "dark_aqua"
			elif token == const.DARK_RED:
				pointer["color"] = "dark_red"
				color = "dark_red"
			elif token == const.DARK_PURPLE:
				pointer["color"] = "dark_purple"
				color = "dark_purple"
			elif token == const.GOLD:
				pointer["color"] = "gold"
				color = "gold"
			elif token == const.GRAY:
				pointer["color"] = "gray"
				color = "gray"
			elif token == const.DARK_GRAY:
				pointer["color"] = "dark_gray"
				color = "dark_gray"
			elif token == const.BLUE:
				pointer["color"] = "blue"
				color = "blue"
			elif token == const.GREEN:
				pointer["color"] = "green"
				color = "green"
			elif token == const.AQUA:
				pointer["color"] = "aqua"
				color = "aqua"
			elif token == const.RED:
				pointer["color"] = "red"
				color = "red"
			elif token == const.LIGHT_PURPLE:
				pointer["color"] = "light_purple"
				color = "light_purple"
			elif token == const.YELLOW:
				pointer["color"] = "yellow"
				color = "yellow"
			elif token == const.WHITE:
				pointer["color"] = "white"
				color = "white"
			else:
				pointer["text"] = token
		if isset(newString["extra"]):
			for k,d in newString["extra"] :
				if not isset(d["extra"]):
					del newString["extra"][k]
		return json.dumps(newString)

	def str_repeat(the_str, multiplier):
		return the_str * multiplier

	"""
	Returns an HTML-formatted string with colors/markup
	:param s: String|array
	:return: String
	"""
	def toHTML(self, s):
		if not is_array(s):
			s = self.tokenize(s)
		newString = ""
		tokens = 0
		for token in s:
			if token == const.BOLD:
				newString += "<span style=font-weight:bold>"
				++tokens
			elif token == const.ITALIC:
				newString += "<span style=font-style:italic>"
				++tokens
			elif token == const.UNDERLINE:
				newString += "<span style=text-decoration:underline>"
				++tokens
			elif token == const.STRIKETHROUGH:
				newString += "<span style=text-decoration:line-through>"
				++tokens
			elif token == const.RESET:
				newString += str_repeat("</span>", tokens)
				tokens = 0

			elif token == const.BLACK:
				newString += "<span style=color:#000>"
				++tokens
			elif token == const.DARK_BLUE:
				newString += "<span style=color:#00A>"
				++tokens
			elif token == const.DARK_GREEN:
				newString += "<span style=color:#0A0>"
				++tokens
			elif token == const.DARK_AQUA:
				newString += "<span style=color:#0AA>"
				++tokens
			elif token == const.DARK_RED:
				newString += "<span style=color:#A00>"
				++tokens
			elif token == const.DARK_PURPLE:
				newString += "<span style=color:#A0A>"
				++tokens
			elif token == const.GOLD:
				newString += "<span style=color:#FA0>"
				++tokens
			elif token == const.GRAY:
				newString += "<span style=color:#AAA>"
				++tokens
			elif token == const.DARK_GRAY:
				newString += "<span style=color:#555>"
				++tokens
			elif token == const.BLUE:
				newString += "<span style=color:#55F>"
				++tokens
			elif token == const.GREEN:
				newString += "<span style=color:#5F5>"
				++tokens
			elif token == const.AQUA:
				newString += "<span style=color:#5FF>"
				++tokens
			elif token == const.RED:
				newString += "<span style=color:#F55>"
				++tokens
			elif token == const.LIGHT_PURPLE:
				newString += "<span style=color:#F5F>"
				++tokens
			elif token == const.YELLOW:
				newString += "<span style=color:#FF5>"
				++tokens
			elif token == const.WHITE:
				newString += "<span style=color:#FFF>"
				++tokens
			else:
				newString += token

		newString += str_repeat("</span>", tokens)
		return newString

	"""
	Returns an ANSI-formatted string with colors/markup
	:param s: String|array
	:return: String
	"""
	def toANSI(self, s):
		if not is_array(s):
			s = self.tokenize(s)

		newString = ""
		for token in s:
			if token == const.BOLD:
				newString += "\033[1m"
			elif token == const.OBFUSCATED:
				newString += "\033[0m"
			elif token == const.ITALIC:
				newString += "\033[3m"				
			elif token == const.UNDERLINE:
				newString += "\033[4m"			
			elif token == const.STRIKETHROUGH:
				newString += "\033[0m"					
			elif token == const.RESET:
				newString += str_repeat("</span>", tokens)
				tokens = 0					

			#Colors
			elif token == const.BLACK:
				newString += "\033[30m"			
			elif token == const.DARK_BLUE:
				newString += "\033[34m"				
			elif token == const.DARK_GREEN:
				newString += "\033[32m"				
			elif token == const.DARK_AQUA:
				newString += "\033[36m"				
			elif token == const.DARK_RED:
				newString += "\033[31m"					
			elif token == const.DARK_PURPLE:
				newString += "\033[35m"					
			elif token == const.GOLD:
				newString += "\033[43m"				
			elif token == const.GRAY:
				newString += "\033[37m"				
			elif token == const.DARK_GRAY:
				newString += "\033[40m"				
			elif token == const.BLUE:
				newString += "\033[44m"				
			elif token == const.GREEN:
				newString += "\033[42m"				
			elif token == const.AQUA:
				newString += "\033[46m"				
			elif token == const.RED:
				newString += "\033[41m"				
			elif token == const.LIGHT_PURPLE:
				newString += "\033[45m"				
			elif token == const.YELLOW:
				newString += "\033[43m"				
			elif token == const.WHITE:
				newString += "\033[47m"				
			else:
				newString += token
		return newString