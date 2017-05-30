class ArrayAccess(object):
    def __getitem__(self, key):
        return self.container

    def __setitem__(self, key, value):
        self.container = value

    def __delitem__(self, key, value):
        del self.container
