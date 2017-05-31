
class Tag:
    value = None

    def getValue(self):
        return self.value

    def getType(self):
        pass

    def setValue(self, value):
        self.value = value

    def write(self, nbt, network=False):
        pass

    def read(self, nbt, network=False):
        pass

    def __toString(self):
        return str(self.value)
        return str(self.value)