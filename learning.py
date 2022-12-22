from recogn_classes import RecognClass
from IEIT import IEIT

water = RecognClass('photos/water15x15.png')
sand = RecognClass('photos/sand15x15.png')
grass = RecognClass('photos/grass15x15.png')

classes = [water, sand, grass]

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
    print(clas.perfect_radius)
    print(clas.etalon_vector)