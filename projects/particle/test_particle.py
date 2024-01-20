import pytest
import particle

@pytest.mark.parametrize("x0, y0, vx0, vy0", [
    (0,0,5,10),
    (300,200,-7,12),
    (500,300,-4,-10),
])

def test_particle_move(x0, y0, vx0, vy0):
    # Test with initial velocities
    width, height = 600, 400
    dt, g = 2, 4
    w = particle.World(width, height, dt, g)
    p = particle.Particle((x0, y0), (vx0, vy0), w)
    p.update()
    assert p.x == x0 + vx0 * dt
    assert p.y == y0 + (vy0 + g * dt) * dt
    p.update()
    assert p.x == x0 + 2 * vx0 * dt
    assert p.y == y0 + (vy0 + g * dt) * dt + (vy0 + 2 * g * dt) * dt


@pytest.mark.parametrize("x0, y0, vx0, vy0", [
(0, 0, 5, 10),
(300, 200, -7, 12),
(500, 300, -4, -10),
])

def test_particle_move_analytically(x0, y0, vx0, vy0):
    # Test if consistent with analytical parabolic motion
    width, height = 600, 400
    dt, g = 1, 0.5
    w = particle.World(width, height, dt, g)

    p = particle.Particle((x0, y0), (vx0, vy0), w)
    N = 2000
    for _ in range(N):
        p.update()
    assert p.x == x0 + vx0 * (N * dt)
    py_discrete = y0 + vy0 * (N * dt) + 1/2 * g * N * (N + 1) * dt ** 2
    assert p.y == py_discrete
    py_continuous = y0 + vy0 * (N * dt) + 1/2 * g * N ** 2 * dt ** 2
    assert p.y == pytest.approx(py_continuous, 1e-3)


@pytest.mark.parametrize("x0, y0, vx0, vy0, expected", [
    (300, 200, 5, 10, True),
    (300, 200, -5, -10, True),
    (599, 200, 5, 10, False),
    (300, 399, 5, 10, False),
    (-1, 399, 5, 10, False),
    (0, 0, 5, 10, True),
    (0, 0, -5, 10, False),
])

def test_particle_liveness_after_move(x0, y0, vx0, vy0, expected):
    # Test if particle goes off screen after one update
    width, height = 600, 400
    dt, g = 1, 0.5
    w = particle.World(width, height, dt, g)
    p = particle.Particle((x0, y0), (vx0, vy0), w)
    p.update()
    assert p.is_alive == expected