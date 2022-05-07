from sys import stdin


class MatrixError(BaseException):
    def __init__(self, m1, m2):
        self.matrix1 = m1
        self.matrix2 = m2


class Matrix:
    def __init__(self, lines=[]):
        self.data = [line[:] for line in lines]

    def __str__(self):
        str_matrix = ''
        for i in range(len(self.data)):
            if i == len(self.data) - 1:
                str_matrix += '\t'.join(map(str, self.data[i]))
            else:
                str_matrix += '\t'.join(map(str, self.data[i])) + '\n'

        return str_matrix

    def __add__(self, other):
        if self.size() == other.size():
            result = Matrix()
            length = self.size()[1]
            for selfRow, otherRow in zip(self.data, other.data):
                result.data.append(
                    [selfRow[i] + otherRow[i] for i in range(length)])
            return result
        else:
            raise MatrixError(self, other)

    def __mul__(self, constant):
        result = Matrix()
        result.data = [[constant * row[i]
                        for i in range(len(row))] for row in self.data]
        return result

    __rmul__ = __mul__

    def size(self):
        return len(self.data), len(self.data[0])

    def transpose(self):
        self.data = list(map(list, zip(*self.data)))
        return Matrix(self.data)

    @staticmethod
    def transposed(matrix):
        return Matrix(list(map(list, zip(*matrix.data))))


exec(stdin.read())
