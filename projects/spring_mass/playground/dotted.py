import pygame
import sys
import math

pygame.init()

width, height = 400, 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

def draw_dotted_line(surface, color, start_pos, end_pos, dot_radius=1, gap_length=5):
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    dot_count = int(distance / (dot_radius * 2 + gap_length))

    if dot_count == 0:
        return  # Prevent division by zero

    dx = dx / dot_count
    dy = dy / dot_count

    for i in range(dot_count):
        pygame.draw.circle(surface, color, (int(start_pos[0] + i * dx), int(start_pos[1] + i * dy)), dot_radius)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    draw_dotted_line(screen, (0, 0, 0), (50, 50), (350, 350), dot_radius=5, gap_length=10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
