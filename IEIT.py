"""
    This module provides functionality for calculate_distance, get neighbors, optimize radius and delta.
"""
import math
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

    def optimize_radius(self):
        with open('output_data/radius_data.csv', 'w') as file:
            csvwriter = csv.writer(file, lineterminator='\n')
            csvwriter.writerow(['Radius', 'Working Area?', 'KFE'])

            for cl in self.classes:
                radius = 0
                radius_dict = {}
                true_area_radiuses = {}

                for x in range(1, 50):
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
                        csvwriter.writerow([radius, 'True', kfe])
                    else:
                        radius_dict[radius] = [False, kfe]
                        csvwriter.writerow([radius, 'False', kfe])

                    radius += 1

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
            delta_dict = {}
            for delta in range(1, max_delta):
                self.base_class.delta = delta
                self.base_class.get_avg_vector()
                self.base_class.get_limits()

                row = [delta]
                classes_kfe_list = []

                for cl in self.classes:

                    cl.avg_vector = self.base_class.avg_vector
                    cl.higher_limit = self.base_class.higher_limit
                    cl.lower_limit = self.base_class.lower_limit
                    cl.matrix_to_binary()
                    cl.get_etalon_vector()
                    IEIT.get_neighbors(self)

                    radius = 0
                    radius_dict = {}

                    for x in range(1, 50):
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
                    row.append(k_f_e)
                    row.append(area)
                    classes_kfe_list.append(k_f_e)
                    classes_kfe_list.append(area)

                csvwriter.writerow(row)
                delta_dict[delta] = classes_kfe_list

            delta_avgkfe_dict = {}
            for key, value in delta_dict.items():
                if value[1] is True and value[3] is True and value[5] is True:
                    delta_avgkfe_dict[key] = (value[0] + value[2] + value[4]) / 3

            perfect_delta = max(delta_avgkfe_dict, key=delta_avgkfe_dict.get)
            print(perfect_delta)

