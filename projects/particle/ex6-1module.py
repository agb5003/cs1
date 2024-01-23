import pygame
import random

def bounce_on_boundary(p):
    x, y = p.x, p.y
    vx, vy = p.vel.x, p.vel.y
    width, height = p.world.width, p.world.height
    radius = p.radius
    e = 0.95
    if (x < 0 + radius and vx < 0) or (x > width - radius and vx > 0):
        p.vel.x *= -e
    if y > height - radius and vy > 0:
        p.vel.y *= -e
        # constrain particle on or above the floor
        p.pos.y = height - radius

class BounceOnBoundaryStrategy:
    def __init__(self, restitution = 0.95):
        self.restitution = restitution
    def __call__(self, p):
        x, y = p.x, p.y
        vx, vy = p.vel.x, p.vel.y
        width, height = p.world.width, p.world.height
        radius = p.radius
        e = self.restitution
        if (x < 0 + radius and vx < 0) or (x > width - radius and vx > 0):
            p.vel.x *= -e
        if y > height - radius and vy > 0:
            p.vel.y *= -e
            # constrain particle on or above the floor
            p.pos.y = height - radius

class BounceLimited:
    def __init__(self, restitution = 0.95, max_bounces = 4):
        self.restitution = restitution
        self.max_bounces = max_bounces
        self.bounce_count = 0
    def __call__(self, p):
        if self.bounce_count < self.max_bounces:
            # Bounce particle if max bounce has not been reached
            x, y = p.x, p.y
            vx, vy = p.vel.x, p.vel.y
            width, height = p.world.width, p.world.height
            radius = p.radius
            e = self.restitution
            if (x < 0 + radius and vx < 0) or (x > width - radius and vx > 0):
                p.vel.x *= -e
                self.bounce_count += 1
            if y > height - radius and vy > 0:
                p.vel.y *= -e
                # constrain particle on or above the floor
                p.pos.y = height - radius
                self.bounce_count += 1
        else:
            # we can delete the particle from the list to clean up after the max bounce is reached
            p.is_alive = False
            '''
            Important note: this will look like the particle doesn't bounce for the final count, but this is because the particle disappears immediately after the collision with the boundary, which doesn't look like a "bounce" to us. Asynchronous wait or sleep can be used but since I would have to use an external library I will not use them.
            '''

class World:
    def __init__(self, width, height, dt, gy):
        self.width = width
        self.height = height
        self.dt = dt
        self.gravity_acc = pygame.math.Vector2(0, gy)

class Particle:
    def __init__(self, pos, vel, world, radius=10.0, color = "green", postmove_strategy = None):
        self.is_alive = True
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(vel)
        self.world = world
        self.radius = radius
        self.color = pygame.Color(color)
        self.postmove_strategy = postmove_strategy

    def update(self):
        self.vel += self.world.gravity_acc * self.world.dt
        self.pos += self.vel * self.world.dt
        if self.postmove_strategy is not None:
            # This calls the correct strategy if postmove_strategy is not None
            self.postmove_strategy(self)
            # e.g. if postmove_strategy was defined to be BounceOnBoundaryStrategy, it will call this object.
        else:
            self.update_after_move()

    def update_after_move(self):
        if self.x < 0 or self.x > self.world.width or self.y > self.world.height:
            self.is_alive = False

    def draw(self, screen):
        radius = 10
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    @property
    def x(self):
        return self.pos.x
    
    @property
    def y(self):
        return self.pos.y
    
# ConfinedParticle inherits Particle. Instead of leaving the screen, ConfinedParticle will bounce after colliding with boundaries.
class ConfinedParticle(Particle):
    def update_after_move(self):
        x, y = self.x, self.y
        vx, vy = self.vel.x, self.vel.y
        width, height = self.world.width, self.world.height
        radius = self.radius
        e = 0.9
        # note to self: these local variables are pass by value, so they can't be used to assign values (need to use self.pos and self.vel).
        if (x - radius < 0 and vx < 0) or (x + radius > width and vx > 0):
            # Collision with left and right boundaries
            self.vel.x *= -e
        if y + radius > height and vy > 0:
            # Collision with ground (bottom boundary)
            self.vel.y *= -e
            # Normal force (constrain particle to above the floor)
            self.pos.y = height - radius