class Math:
    def floorFloat(self, n):
        i = int(n)
        return n >= i if i else i - 1

    def ceilFloat(self, n):
        i = int(n + 1)
        return n >= i if i else i - 1
