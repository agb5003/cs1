'''
Exercise 7-2

This exercise simulates the phenomenon of resonance. In a simple spring-mass system, when a 
harmonic force is acted on the moving mass, if its frequency is close to the natural oscillation 
frequency of the system, the resulting motion becomes that of constructive interference, which 
means the amplitude will grow unbounded in a system with no friction or damping. In a system with 
damping, the amplitude will not grow unbounded, however it will still grow, or decay at a slower 
rate than if the frequency of the harmonic force were far from the natural frequency.

In this exercise, when ran, you will see two springs. The top one is forced by a harmonic force 
with a frequency of 0.075, while the bottom one has frequency 0.12. The natural frequency of the 
system is sqrt(k/m) = ~0.071. Even though the masses and spring constants are identical, the top 
system will grow in amplitude, so much so that the moving mass will even collide with the fixed 
one, while the bottom one will slowly decay in amplitude. This can be confirmed by putting two 
fingers on the bottom system: one at the leftmost point and one at the rightmost point of the mass' 
oscillation. After a few moments, the oscillation will never reach those two points again.

'''

import pygame
import spring_mass as spm
import math

PgVector = pygame.math.Vector2
        
class DottedLineDrawer(spm.LineDrawer):
    def __call__(self, screen, pos1, pos2):
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        dot_radius = 2
        gap_length = 5
        distance = math.sqrt(dx**2 + dy**2)
        dot_count = int(distance / (dot_radius * 2 + gap_length))

        if dot_count == 0:
            return  # Prevent division by zero

        dx = dx / dot_count
        dy = dy / dot_count

        for i in range(dot_count + 1):
            pygame.draw.circle(screen, self.color, (int(pos1[0] + i * dx), int(pos1[1] + i * dy)), dot_radius)


def compute_harmonic_force(amplitude, frequency):
    time = pygame.time.get_ticks() // 16
    return PgVector((amplitude * math.sin(frequency * time)), 0)

class ForcedPointMass(spm.PointMass):
    def __init__(self, pos, vel, world, radius=10.0, mass=10.0,
                 viscous_damping=0.01, restitution=0.95, harmonic_force = False, 
                 amplitude=0, frequency=0, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or CircleDrawer("blue", 1)

        self.pos = PgVector(pos)
        self.vel = PgVector(vel)
        self.radius = radius
        self.mass = mass
        self.viscous_damping = viscous_damping
        self.restitution = restitution

        self.harmonic_force = harmonic_force

        if harmonic_force == True:
            self.amplitude = amplitude
            self.frequency = frequency

        self.total_force = PgVector((0, 0))
        self.message_list = []


    def generate_force(self):
        force_g = spm.compute_gravity_force(self.mass, self.world.gravity_acc)
        force_v = spm.compute_viscous_damping_force(self.viscous_damping, self.vel)
        if self.harmonic_force == True:
            force_f = compute_harmonic_force(self.amplitude, self.frequency)
            self.receive_force(force_g + force_v + force_f)
        else:
            self.receive_force(force_g + force_v)


def main():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    frames_per_second = 60

    # Gravity acceleration is zero
    world = spm.World((width, height), dt=1.0, gravity_acc=(0, 0))
    actor_list = []

    moving_drawer = spm.CircleDrawer("green", 0)
    fixed_drawer = spm.CircleDrawer("grey", 0)

    # Boundaries are deleted to allow for overflow when amplitude grows

    # Particles with springs
    spring_const = 0.05
    natural_len = 250
    line_drawer = DottedLineDrawer("white", 3)

    # Natural frequency is 0.071, Let's set first system to have 0.075 force freq and 0.12 for second system
    p3 = spm.FixedPointMass((100, 100), (0, 0), world, drawer=fixed_drawer)
    p4 = ForcedPointMass((400, 100), (0, 0), world, harmonic_force=True, amplitude=1, frequency=0.072, drawer=moving_drawer)
    sp34 = spm.Spring(p3, p4, world, spring_const, natural_len, line_drawer)

    p5 = spm.FixedPointMass((100, 200), (0, 0), world, drawer=fixed_drawer)
    p6 = ForcedPointMass((400, 200), (0, 0), world, harmonic_force=True, amplitude=1, frequency=0.12, drawer=moving_drawer)
    sp56 = spm.Spring(p5, p6, world, spring_const, natural_len, line_drawer)

    # The first system grows in amplitude, while the second stagnates or even loses amplitude.

    actor_list += [p3, p4, sp34, p5, p6, sp56]

    actor_list.append(spm.CollisionResolver(world, actor_list))
    
    while True:
        clock.tick(frames_per_second)

        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                should_quit = True
        if should_quit:
            break

        for a in actor_list:
            a.update()
        actor_list[:] = [a for a in actor_list if a.is_alive]

        screen.fill(pygame.Color("black"))
        for a in actor_list:
            a.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()