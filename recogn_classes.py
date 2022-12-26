"""
    This module contains information about recognizable class: size, matrix, vectors, limits etc.
"""

from PIL import Image
import numpy
import os


class RecognClass:

    def __init__(self, filename):
        self.filename = filename
        self.delta = 18
        self.size = 50
        self.matrix = []
        self.binary_matrix = []
        self.avg_vector = []
        self.higher_limit = []
        self.lower_limit = []
        self.etalon_vector = []
        self.perfect_radius = 0
        self.neighbor = 0
        self.kfe = 0
        # self.neighbor_id = 0

    def image_to_matrix(self):
        """Convert image to matrix with values of pixel RGBs"""
        image = Image.open(self.filename).convert("L")
        alist = list(image.getdata())
        length = len(alist)
        self.matrix = [alist[i * length // self.size: (i + 1) * length // self.size] for i in range(self.size)]
        return self.matrix

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

    def write_to_file(self):
        """This method gets class name from filename, make .txt file and write there all necessary class data"""
        head, tail = os.path.split(self.filename)
        filename = tail.split('.')[0] + '_data.txt'

        with open('output_data/' + filename, 'w') as f:
            f.write(f"{self.filename} \n\n")
            f.writelines(f"Base Matrix: \n {numpy.matrix(self.matrix)} \n\n")
            f.write(f"AVG Vector: \n {self.avg_vector} \n\n")
            f.write(f"Higher Limit: \n {self.higher_limit} \n\n")
            f.write(f"Lower Limit: \n {self.lower_limit} \n\n")
            f.write(f"Binary Matrix: \n {numpy.matrix(self.binary_matrix)} \n\n")
            f.write(f"Etalon Vector : \n {self.etalon_vector} \n\n")
            f.write(f"Neighbor file : \n {self.neighbor.filename} \n\n")
            f.write(f"Perfect radius : \n {self.perfect_radius} \n\n")
            f.write(f"KFE : \n {self.kfe} \n\n")
