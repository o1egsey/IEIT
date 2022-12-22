from recogn_classes import RecognClass
from IEIT import IEIT

forest = RecognClass('photos/forest.png')
road = RecognClass('photos/road.png')
grass = RecognClass('photos/gras.png')

classes = [forest, road, grass]

for clas in classes:
    clas.image_to_matrix()
    # clas.get_avg_vector()
    # clas.get_limits()
    # clas.matrix_to_binary()
    # clas.get_etalon_vector()


# ieit = IEIT(classes)
# ieit.get_neighbors()
# ieit.optimize_radius()


for clas in classes:
    print(clas.matrix)
