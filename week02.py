import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ULTRA Fancy Particle Playground ✨")

clock = pygame.time.Clock()

particles = []

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 8)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.randint(50, 100)
        self.size = random.randint(3, 6)

        self.hue = random.randint(0, 360)

    def update(self):
        self.x += self.vx
        self.y += self.vy

        self.vy += 0.1  # gravity
        self.life -= 1
        self.hue += 2

    def draw(self, surf):
        if self.life > 0:
            color = pygame.Color(0)
            color.hsva = (self.hue % 360, 80, 100, 100)

            # glow surface
            glow_size = self.size * 4
            glow = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)

            for i in range(glow_size, 0, -2):
                alpha = int(255 * (i / glow_size) ** 2)
                pygame.draw.circle(
                    glow,
                    (color.r, color.g, color.b, alpha),
                    (glow_size // 2, glow_size // 2),
                    i // 2
                )

            surf.blit(glow, (self.x - glow_size//2, self.y - glow_size//2))

            pygame.draw.circle(
                surf,
                color,
                (int(self.x), int(self.y)),
                self.size
            )

    def alive(self):
        return self.life > 0


def draw_background(surface, t):
    for y in range(HEIGHT):
        c = int(40 + 40 * math.sin(y * 0.01 + t))
        color = (10, c, 70 + c//2)
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))

    # sparkle stars
    for _ in range(30):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        surface.set_at((x, y), (255, 255, 255))


running = True
time = 0

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed()

    if buttons[0]:
        for _ in range(12):
            particles.append(Particle(mouse[0], mouse[1]))

    # 자동 랜덤 폭발
    if random.random() < 0.05:
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        for _ in range(40):
            particles.append(Particle(x, y))

    time += 0.03

    draw_background(screen, time)

    for p in particles:
        p.update()
        p.draw(screen)

    particles = [p for p in particles if p.alive()]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()