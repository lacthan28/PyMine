class TextContainer:
    text = None

    def __init__(self, text):
        self.text = text

    def setText(self, text):
        self.text = text

    def getText(self):
        return self.text

    def __toString(self):
        return self.getText()