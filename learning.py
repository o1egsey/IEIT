from recogn_classes import RecognClass
from IEIT import IEIT

water = RecognClass('images/water2.png')
road = RecognClass('images/road.png')
grass = RecognClass('images/grass2.png')

classes = [water, road, grass]

for clas in classes:
    clas.image_to_matrix()
    clas.get_avg_vector()
    clas.get_limits()
    clas.matrix_to_binary()
    clas.get_etalon_vector()


ieit = IEIT(classes)
ieit.get_neighbors()
ieit.optimize_radius()


for clas in classes:
    print(clas.matrix)
    print(clas.neighbor)
    print(clas.perfect_radius)
