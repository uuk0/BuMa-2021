import itertools
import numpy


def calculate(n: int):

    def filter_1(value):
        a, b = value
        return a < b and (a < 1 or a + 1 != b) and (a != 1 or b != n)

    connections = list(filter(
        filter_1,
        itertools.combinations(range(n+1), 2)
    ))
    mutations = itertools.combinations((0, 1), len(connections))
    array = numpy.nd


print(calculate(8))


