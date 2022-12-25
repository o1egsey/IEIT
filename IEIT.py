"""
    This module provides functionality for calculate_distance, get neighbors, optimize radius and delta.
"""
import math
from prettytable import PrettyTable
import csv


class IEIT:

    def __init__(self, classes: list):
        self.classes = classes
        self.base_class = classes[0]

    @staticmethod
    def calculate_distance(vector_1, vector_2):
        """Calculate distance between two vectors."""
        distance = 0

        for x, y in zip(vector_1, vector_2):
            if x != y:
                distance += 1

        return distance

    def get_neighbors(self):
        """
            This method find neighbor for all classes.
        """
        for cl in self.classes:
            cl_distances_dict = {}
            cc = self.classes.copy()
            if cc.index(cl) != 0:
                cc.remove(cl)
                cc.insert(0, cl)

            friend_id = 1
            for x in range(len(self.classes)-1):
                cl_distances_dict[cc[friend_id]] = IEIT.calculate_distance(cl.etalon_vector,
                                                                           cc[friend_id].etalon_vector)
                friend_id += 1

            cl.neighbor = min(cl_distances_dict, key=cl_distances_dict.get)
            # print(f"Neighbor of class {cl} is : {min(cl_distances_dict, key=cl_distances_dict.get)}")

            # print(cl_distances_dict)

    def optimize_radius(self):
        with open('output_data/radius_data.csv', 'w') as file:
            csvwriter = csv.writer(file, lineterminator='\n')
            csvwriter.writerow(['Radius', 'Working Area?', 'KFE', 'k1', 'k3', 't_d1', 't_betta'])

            for cl in self.classes:
                radius = 0
                radius_dict = {}
                true_area_radiuses = {}

                # print(cl.neighbor.filename)

                for x in range(51):
                    k1 = 0
                    k3 = 0
                    for i in range(cl.size):
                        if IEIT.calculate_distance(cl.etalon_vector, cl.get_vector(i)) <= radius:
                            k1 += 1
                        if IEIT.calculate_distance(cl.etalon_vector, cl.neighbor.get_vector(i)) <= radius:
                            k3 += 1

                    t_d1 = k1 / cl.size
                    t_betta = k3 / cl.size
                    d1_b = t_d1 - t_betta
                    kfe = d1_b * math.log((1.0 + d1_b + 0.1) / (1.0 - d1_b + 0.1)) / math.log(2.0)

                    if t_d1 >= 0.5 > t_betta:
                        radius_dict[radius] = [True, kfe]
                        csvwriter.writerow([radius, 'True', kfe, k1, k3, t_d1, t_betta])
                    else:
                        radius_dict[radius] = [False, kfe]
                        csvwriter.writerow([radius, 'False', kfe, k1, k3, t_d1, t_betta])

                    radius += 1
                # print(radius_dict)
                for key, value in radius_dict.items():
                    if value[0] is True:
                        true_area_radiuses[key] = value[1]

                perfect_radius = max(true_area_radiuses, key=true_area_radiuses.get, default=0)
                cl.perfect_radius = perfect_radius
                cl.kfe = radius_dict[perfect_radius][1]

    def optimize_delta(self, max_delta=50):
        filename = 'output_data/deltas_data.csv'

        with open(filename, 'w') as f:
            csvwriter = csv.writer(f, lineterminator='\n')
            csvwriter.writerow(['Delta', 'KFE_0', 'Working Area_0', 'KFE_1', 'Working Area_1', 'KFE_2', 'Working Area_2'])
            for delta in range(1, max_delta):
                self.base_class.delta = delta
                self.base_class.get_avg_vector()
                self.base_class.get_limits()

                row = []

                for cl in self.classes:
                    row = [delta]
                    # csvwriter.writerow([f'Class: {cl.filename}'])
                    cl.avg_vector = self.base_class.avg_vector
                    cl.higher_limit = self.base_class.higher_limit
                    cl.lower_limit = self.base_class.lower_limit
                    cl.matrix_to_binary()
                    cl.get_etalon_vector()
                    IEIT.get_neighbors(self)

                    # radius optimization starts
                    radius = 0
                    radius_dict = {}

                    for x in range(51):
                        k1 = 0
                        k3 = 0
                        for i in range(cl.size):
                            if IEIT.calculate_distance(cl.etalon_vector, cl.get_vector(i)) <= radius:
                                k1 += 1
                            if IEIT.calculate_distance(cl.etalon_vector, cl.neighbor.get_vector(i)) <= radius:
                                k3 += 1

                        t_d1 = k1 / cl.size
                        t_betta = k3 / cl.size
                        d1_b = t_d1 - t_betta
                        kfe = d1_b * math.log((1.0 + d1_b + 0.1) / (1.0 - d1_b + 0.1)) / math.log(2.0)

                        if t_d1 >= 0.5 > t_betta:
                            radius_dict[kfe] = True
                        else:
                            radius_dict[kfe] = False
                        radius += 1

                    k_f_e = max(radius_dict.keys())
                    area = radius_dict[k_f_e]

                    row.append(kfe)
                    row.append(area)

                csvwriter.writerow(row)
                row.clear()

                    # csvwriter.writerow([delta, k_f_e, area])






    # def optimize_delta(self, max_delta=50):
    #     """Method for optimization delta. It takes max delta, as param.
    #         Then for every value of delta it is calculating new limits, new binary matrix, etalon, neighbors, perfect
    #         radius and then calculate KFE for this delta.
    #
    #         To-do: needed to implement algorithm for getting perfect delta automatically.
    #     """
    #     # filename = 'deltas.csv'
    #     filename = 'deltas.txt'
    #     fields = ['Delta', 'Working area', 'KFE']
    #     with open(filename, 'w') as f:
    #         # csvwriter = csv.writer(f, lineterminator='\n')
    #         class_index = 0
    #         true_delta_dict = {}
    #         list_of_deltas = []
    #
    #         for cl in self.classes:
    #             # print(f"Class #{class_index}")
    #             f.write(f"Class is {cl.filename} \n")
    #             for delta in range(1, max_delta):
    #                 f.write(f"delta :{delta} \n")
    #                 cl.delta = delta
    #                 cl.get_limits()
    #                 cl.matrix_to_binary()
    #                 cl.get_etalon_vector()
    #                 IEIT.get_neighbors(self)
    #                 f.write(f"Neighbor delta is: {cl.neighbor.delta} \n")
    #                 IEIT.optimize_radius(self)
    #                 # print(f"Radius: {cl.perfect_radius}")
    #
    #                 delta_table = PrettyTable(['Delta', 'Working Area', 'KFE'])
    #
    #                 k1 = 0
    #                 k3 = 0
    #                 for i in range(cl.size):
    #                     f.write(f"Etalon vector  {cl.etalon_vector} \n")
    #                     f.write(f"I vector:  {cl.get_vector(i)}, i={i} \n")
    #                     f.write(f"Distance: {IEIT.calculate_distance(cl.etalon_vector, cl.get_vector(i))} \n")
    #                     f.write(f"Radius: {cl.perfect_radius} \n\n")
    #                     if IEIT.calculate_distance(cl.etalon_vector, cl.get_vector(i)) <= cl.perfect_radius:
    #                         k1 += 1
    #                     f.write(f"Etalon vector  {cl.etalon_vector} \n")
    #                     f.write(f"I neighbor vector:  {cl.neighbor.get_vector(i)}, i={i} \n")
    #                     f.write(f"Distance: {IEIT.calculate_distance(cl.etalon_vector, cl.neighbor.get_vector(i))} \n")
    #                     f.write(f"Radius: {cl.perfect_radius} \n\n")
    #                     if IEIT.calculate_distance(cl.etalon_vector, cl.neighbor.get_vector(i)) <= cl.perfect_radius:
    #                         k3 += 1
    #                 t_d1 = k1 / cl.size
    #                 t_betta = k3 / cl.size
    #                 d1_b = t_d1 - t_betta
    #                 kfe = d1_b * math.log((1.0 + d1_b + 0.1) / (1.0 - d1_b + 0.1)) / math.log(2.0)
    #                 f.write(f"K1: {k1}")
    #                 f.write(f"K3: {k3}")
    #                 f.write(f"KFE: {kfe} \n")
    #
    #                 # if t_d1 >= 0.5 > t_betta:
    #                 #     delta_table.add_row([delta, 'True', kfe])
    #                 #     csvwriter.writerow([delta, 'True', kfe])
    #                 #     true_delta_dict[delta] = kfe
    #                 # else:
    #                 #     delta_table.add_row([delta, 'False', kfe])
    #                 #     csvwriter.writerow([delta, 'False', kfe])
    #
    #                 # print(radius_table)
    #                 # print(delta_table)
    #             class_index += 1
    #             # print(true_delta_dict)
    #             # new_dict = {}
    #             # for k, v in true_delta_dict.items():
    #             #     if 1 <= k <= 8 or 17 <= k <= 22:
    #             #         # new_dict[k] = v
    #             #         list_of_deltas.append([k, v])
    #             #         # if k in list_of_deltas:
    #             #         #     list_of_deltas[k] += v
    #             #         # else:
    #             #         #     list_of_deltas.append([k, v])
    #             # # print(new_dict)
    #             # print(list_of_deltas)
    #             # # new_dict.clear()
    #             # list_of_deltas.clear()
    #             true_delta_dict = {}
    #         # print(list_of_deltas)
