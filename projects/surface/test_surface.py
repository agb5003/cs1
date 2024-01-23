import pytest
import surface

def test_solids():
    for a in range(1, 10):
        shape1 = surface.Cube(a)
        assert shape1.surface_to_volume_ratio() == pytest.approx(6 / a)
        shape2 = surface.Sphere(a)
        assert shape2.surface_to_volume_ratio() == pytest.approx(3 / a)