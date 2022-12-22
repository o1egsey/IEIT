"""
    This module contains information about recognizable class: size, matrix, vectors, limits etc.
"""

from PIL import Image
import numpy


class RecognClass:

    def __init__(self, filename):
        self.filename = filename
        self.delta = 20
        self.size = 15
        self.matrix = []
        self.binary_matrix = []
        self.avg_vector = []
        self.higher_limit = []
        self.lower_limit = []
        self.etalon_vector = []
        self.perfect_radius = 0
        # self.neighbor_id = 0
        self.neighbor = 0

    def image_to_matrix(self):
        """Convert image to matrix with values of pixel RGBs"""
        image = Image.open(self.filename).convert("L")
        alist = list(image.getdata())
        length = len(alist)
        self.matrix = [alist[i * length // self.size: (i + 1) * length // self.size] for i in range(self.size)]
        return [alist[i * length // self.size: (i + 1) * length // self.size] for i in range(self.size)]

    def get_avg_vector(self):
        """Calculate average vector from matrix"""
        self.avg_vector = list(numpy.mean(self.matrix, axis=0))
        return list(numpy.mean(self.matrix, axis=0))

    def get_limits(self):
        """Calculate higher and lower limits"""
        high_limit = []
        low_limit = []
        index = 0
        for pixel in self.avg_vector:
            high_limit.append(self.avg_vector[index] + self.delta)
            low_limit.append(self.avg_vector[index] - self.delta)
            index += 1

        self.higher_limit = high_limit
        self.lower_limit = low_limit
        return high_limit, low_limit

    def matrix_to_binary(self):
        """Convert regular matrix to binary"""
        binary_matrix = []

        for i in self.matrix:
            row = []
            for j in i:
                if self.lower_limit[0] <= j <= self.higher_limit[0]:
                    row.append(1)
                else:
                    row.append(0)
            binary_matrix.append(row)

        self.binary_matrix = binary_matrix
        return binary_matrix

    def get_etalon_vector(self):
        """Returns etalon vector for binary matrix"""
        counter_0 = [0] * self.size
        counter_1 = [0] * self.size
        etalon = []

        for row in self.binary_matrix:
            index = 0
            for num in row:
                if num == 0:
                    counter_0[index] += 1
                else:
                    counter_1[index] += 1
                index += 1
        for i, j in zip(counter_0, counter_1):
            if i > j:
                etalon.append(0)
            else:
                etalon.append(1)

        self.etalon_vector = etalon
        return etalon

    def get_vector(self, row_id):
        """This function returns one row from binary matrix"""
        return self.binary_matrix[row_id]
