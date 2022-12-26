from recogn_classes import RecognClass
from IEIT import IEIT
import numpy
import sys
numpy.set_printoptions(threshold=sys.maxsize)


water = RecognClass('test_data/water.png')
land = RecognClass('test_data/land.png')
forest = RecognClass('test_data/forest.png')


def learn(classes: list):
    """This func is for gathering all needed data and putting it together for learning process"""

    base_class = classes[0]
    base_class.image_to_matrix()
    base_class.get_avg_vector()
    base_class.get_limits()

    for c in classes:
        c.image_to_matrix()
        c.avg_vector = base_class.avg_vector
        c.higher_limit = base_class.higher_limit
        c.lower_limit = base_class.lower_limit
        c.matrix_to_binary()
        c.get_etalon_vector()

    ieit = IEIT(classes)
    ieit.get_neighbors()
    ieit.optimize_radius()
    # ieit.optimize_delta()

    for c in classes:
        c.write_to_file()

    return 'Learning ends'


def exam(filename, classes: list):
    base_class = classes[0]
    examen = RecognClass(filename)
    examen.image_to_matrix()
    examen.avg_vector = base_class.avg_vector
    examen.higher_limit = base_class.higher_limit
    examen.lower_limit = base_class.lower_limit
    examen.matrix_to_binary()
    examen.get_etalon_vector()

    results_dict = {}

    for clas in classes:
        distance = IEIT.calculate_distance(clas.etalon_vector, examen.etalon_vector)
        f = 1 - distance/clas.perfect_radius
        results_dict[clas.filename] = f
        print(f"Class: {clas.filename}, Distance: {distance}, Radius: {clas.perfect_radius}, f = {f}")

    max_f = max(results_dict, key=results_dict.get)

    if results_dict[max_f] >= 0:
        return f"\nExamenee is seems to be {max_f}"
    else:
        return f"Examenee is Unknown Class"


learning = learn([water, land, forest])

ex = exam('test_data/exam_water.png', [water, land, forest])
print(ex)
