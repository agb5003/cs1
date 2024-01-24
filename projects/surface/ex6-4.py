import math
import pytest


class Solid:
    def surface_to_volume_ratio(self):
        return self.surface_area() / self.volume()

class Cube(Solid):
    def __init__(self, edge_length):
        self.edge_length = edge_length

    def volume(self):
        return math.pow(self.edge_length, 3)

    def surface_area(self):
        return 6 * math.pow(self.edge_length, 2)

class Sphere(Solid):
    def __init__(self, radius):
        self.radius = radius

    def volume(self):
        return (4/3) * math.pi * math.pow(self.radius, 3)

    def surface_area(self):
        return 4 * math.pi * math.pow(self.radius, 2)

def test_solids():
    for a in range(1, 10):
        shape1 = Cube(a)
        assert shape1.surface_to_volume_ratio() == pytest.approx(6 / a)
        shape2 = Sphere(a)
        assert shape2.surface_to_volume_ratio() == pytest.approx(3 / a)

test_solids()