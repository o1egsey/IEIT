from recogn_classes import RecognClass
from IEIT import IEIT

forest_class = RecognClass('images/forest.png')
field_class = RecognClass('images/field.png')
road_class = RecognClass('images/road.png')

classes = [forest_class, field_class, road_class]

for clas in classes:
    clas.image_to_matrix()
    clas.get_avg_vector()
    clas.get_limits()
    clas.matrix_to_binary()
    clas.get_etalon_vector()


ieit = IEIT(classes)
ieit.get_neighbors()
ieit.optimize_radius()
