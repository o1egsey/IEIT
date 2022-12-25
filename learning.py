from recogn_classes import RecognClass
from IEIT import IEIT
import numpy
import sys
numpy.set_printoptions(threshold=sys.maxsize)


forest = RecognClass('images/for.png')
land = RecognClass('images/road.png')
grass = RecognClass('images/grass2.png')

# forest = RecognClass('small_data/water_15.png')
# land = RecognClass('small_data/road_15.png')
# grass = RecognClass('small_data/grass_15.png')

classes = [forest, land, grass]

for clas in classes:
    clas.image_to_matrix()

base_class = classes[0]
base_class.get_avg_vector()
base_class.get_limits()


for clas in classes:
    clas.avg_vector = base_class.avg_vector
    clas.higher_limit = base_class.higher_limit
    clas.lower_limit = base_class.lower_limit
    clas.matrix_to_binary()
    clas.get_etalon_vector()


ieit = IEIT(classes)
ieit.get_neighbors()
ieit.optimize_radius()
ieit.optimize_delta()


with open('output_data/forest_data.txt', 'w') as file:
    file.write(f"{forest.filename} \n\n")
    file.writelines(f"Base Matrix: \n {numpy.matrix(forest.matrix)} \n\n")
    file.write(f"AVG Vector: \n {forest.avg_vector} \n\n")
    file.write(f"Higher Limit: \n {forest.higher_limit} \n\n")
    file.write(f"Lower Limit: \n {forest.lower_limit} \n\n")
    file.write(f"Binary Matrix: \n {numpy.matrix(forest.binary_matrix)} \n\n")
    file.write(f"Etalon Vector : \n {forest.etalon_vector} \n\n")
    file.write(f"Neighbor file : \n {forest.neighbor.filename} \n\n")
    file.write(f"Perfect radius : \n {forest.perfect_radius} \n\n")
    file.write(f"KFE : \n {forest.kfe} \n\n")

with open('output_data/land_data.txt', 'w') as file:
    file.write(f"{land.filename} \n\n")
    file.writelines(f"Base Matrix: \n {numpy.matrix(land.matrix)} \n\n")
    file.write(f"AVG Vector: \n {land.avg_vector} \n\n")
    file.write(f"Higher Limit: \n {land.higher_limit} \n\n")
    file.write(f"Lower Limit: \n {land.lower_limit} \n\n")
    file.write(f"Binary Matrix: \n {numpy.matrix(land.binary_matrix)} \n\n")
    file.write(f"Etalon Vector : \n {land.etalon_vector} \n\n")
    file.write(f"Neighbor file : \n {land.neighbor.filename} \n\n")
    file.write(f"Perfect radius : \n {land.perfect_radius} \n\n")
    file.write(f"KFE : \n {land.kfe} \n\n")

with open('output_data/grass_data.txt', 'w') as file:
    file.write(f"{grass.filename} \n\n")
    file.writelines(f"Base Matrix: \n {numpy.matrix(grass.matrix)} \n\n")
    file.write(f"AVG Vector: \n {grass.avg_vector} \n\n")
    file.write(f"Higher Limit: \n {grass.higher_limit} \n\n")
    file.write(f"Lower Limit: \n {grass.lower_limit} \n\n")
    file.write(f"Binary Matrix: \n {numpy.matrix(grass.binary_matrix)} \n\n")
    file.write(f"Etalon Vector : \n {grass.etalon_vector} \n\n")
    file.write(f"Neighbor file : \n {grass.neighbor.filename} \n\n")
    file.write(f"Perfect radius : \n {grass.perfect_radius} \n\n")
    file.write(f"KFE : \n {grass.kfe} \n\n")