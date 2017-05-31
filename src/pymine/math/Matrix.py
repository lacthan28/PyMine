from ...spl.stubs.core_c import ArrayAccess
from copy import *


class Matrix:
    matrix = []
    rows = 0
    columns = 0

    def isset(variable):
        return variable in locals() or variable in globals()

    def offsetExists(self, offset):
        return self.isset(self.matrix[int(offset)])

    def offsetGet(self, offset):
        return self.matrix[int(offset)]

    def offsetSet(self, offset, value):
        self.matrix[int(offset)] = value

    def offsetUnset(self, offset):
        del self.matrix[int(offset)]

    def __init__(self, rows, columns, set=[]):
        self.rows = max(1, int(rows))
        self.columns = max(1, int(columns))
        self.set(set)

    def set(self, m):
        r = 0
        while r < self.rows:
            self.matrix[r] = []
            c = 0
            while c < self.columns:
                self.matrix[r][c] = self.isset(m[r][c]) if m[r][c] else 0
                ++c
            ++r

    def getRows(self):
        return self.rows

    def getColumns(self):
        return self.columns

    def setElement(self, row, column, value):
        if row > self.rows or row < 0 or column > self.columns or column < 0:
            return False
        self.matrix[int(row)][int(column)] = value
        return True

    def getElement(self, row, column):
        if row > self.rows or row < 0 or column > self.columns or column < 0:
            return False
        return self.matrix[int(row)][int(column)]

    def isSquare(self):
        return self.rows == self.columns

    def add(self, matrix):
        if (self.rows is not matrix.getRows()) or (self.columns is not matrix.getColumns()):
            return False

        result = Matrix(self.rows, self.columns)
        r = 0
        while r < self.rows:
            c = 0
            while c < self.columns:
                result.setElement(r, c, self.matrix[r][c] + matrix.getElement(r, c))
                ++c
            ++r
        return result

    def substract(self, matrix):
        if (self.rows is not matrix.getRows()) or (self.columns is not matrix.getColumns()):
            return False
        result = copy(self)
        r = 0
        while r < self.rows:
            c = 0
            while c < self.columns:
                result.setElement(r, c, self.matrix[r][c] - matrix.getElement(r, c))
                ++c
            ++r
        return result

    def divideScalar(self, number):
        result = copy(self)
        r = 0
        while r < self.rows:
            c = 0
            while c < self.columns:
                result.setElement(r, c, self.matrix[r][c] / number)
                ++c
            ++r
        return result

    def transpose(self):
        result = Matrix(self.columns, self.rows)
        r = 0
        while r < self.rows:
            c = 0
            while c < self.columns:
                result.setElement(c, r, self.matrix[r][c])
                ++c
            ++r
        return result

    def product(self, matrix):
        if self.columns is not matrix.getRows():
            return False

        c = matrix.getColumns()
        result = Matrix(self.rows, c)
        i = 0
        while i < self.rows:
            j = 0
            while j < c:
                s = 0
                k = 0
                while k < self.columns:
                    s += self.matrix[i][k] * matrix.getElement(k, j)
                    ++k
                result.setElement(i, j, s)
                ++j
            ++i
        return result

    def determinant(self):
        if self.isSquare() != True:
            return False

        if self.rows is 1:
            return 0
        elif self.rows is 2:
            return self.matrix[0][0] * self.matrix[1][1] - self.matrix[0][1] * self.matrix[1][0]
        elif self.rows is 3:
            return self.matrix[0][0] * self.matrix[1][1] * self.matrix[2][2] + self.matrix[0][1] * self.matrix[1][2] * \
                                                                               self.matrix[2][0] + self.matrix[0][2] * \
                                                                                                   self.matrix[1][0] * \
                                                                                                   self.matrix[2][1] - \
                   self.matrix[2][0] * self.matrix[1][1] * self.matrix[0][2] - self.matrix[2][1] * self.matrix[1][2] * \
                                                                               self.matrix[0][0] - self.matrix[2][2] * \
                                                                                                   self.matrix[1][0] * \
                                                                                                   self.matrix[0][1]

        return False

    def __toString(self):
        s = ""
        r = 0
        while r < self.rows:
            s += ','.join(self.matrix[r]) + ";"
            ++r

        return "Matrix(" + self.rows + "x" + self.columns + ";" + s[0:-1] + ")"
