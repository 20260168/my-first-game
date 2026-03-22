import pygame
import sys
import random
import math

pygame.init()
screen = pygame.display.set_mode((1600, 800))
pygame.display.set_caption("My First Pygame")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

clock = pygame.time.Clock()
running = True
game_over = False

x = 400
y = 300
size = 15

font = pygame.font.SysFont(None, 30)
big_font = pygame.font.SysFont(None, 100)

# 장애물
obstacles = []
spawn_timer = 0
spawn_delay = 15  # 1초

# 시작 시간
start_ticks = pygame.time.get_ticks()
elapsed_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            x -= 7
        if keys[pygame.K_RIGHT]:
            x += 7
        if keys[pygame.K_UP]:
            y -= 7
        if keys[pygame.K_DOWN]:
            y += 7

        # 화면 래핑
        if x < -size:
            x = 1600 + size
        elif x > 1600 + size:
            x = -size
        if y < -size:
            y = 800 + size
        elif y > 800 + size:
            y = -size

        # 장애물 생성
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            spawn_timer = 0
            side = random.choice(["top", "bottom", "left", "right"])
            radius = random.randint(20, 60)

            if side == "top":
                ox = random.randint(0, 1600)
                oy = -radius
                dx = random.uniform(-2, 2)
                dy = random.uniform(2, 5)
            elif side == "bottom":
                ox = random.randint(0, 1600)
                oy = 800 + radius
                dx = random.uniform(-2, 2)
                dy = random.uniform(-5, -2)
            elif side == "left":
                ox = -radius
                oy = random.randint(0, 800)
                dx = random.uniform(2, 5)
                dy = random.uniform(-2, 2)
            elif side == "right":
                ox = 1600 + radius
                oy = random.randint(0, 800)
                dx = random.uniform(-5, -2)
                dy = random.uniform(-2, 2)

            obstacles.append([ox, oy, dx, dy, radius])

        # 장애물 이동
        for obs in obstacles:
            obs[0] += obs[2]
            obs[1] += obs[3]

        # 충돌 체크
        for obs in obstacles:
            dist = math.hypot(x - obs[0], y - obs[1])
            if dist < size + obs[4]:
                game_over = True
                # 충돌 시 마지막 시간 저장
                elapsed_time = pygame.time.get_ticks() - start_ticks
                break

        # 살아있는 동안 시간 갱신
        if not game_over:
            elapsed_time = pygame.time.get_ticks() - start_ticks

    # 화면 그리기
    screen.fill(WHITE)

    # 삼각형
    points = [
        (x, y - size),
        (x - size, y + size),
        (x + size, y + size)
    ]
    pygame.draw.polygon(screen, BLUE, points)

    # 장애물
    for obs in obstacles:
        pygame.draw.circle(screen, BLACK, (int(obs[0]), int(obs[1])), obs[4])

    # FPS + 좌표
    fps = clock.get_fps()
    text = f"FPS: {int(fps)}  X: {x}  Y: {y}"
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (10, 10))

    # 🔥 생존 시간 (0.1초 단위)
    time_seconds = elapsed_time / 1000  # ms → s
    time_text = f"Time: {time_seconds:.1f}s"
    time_surface = font.render(time_text, True, BLACK)
    screen.blit(time_surface, (1400, 10))  # 오른쪽 위

    # GAME OVER
    if game_over:
        go_text = big_font.render("GAME OVER", True, RED)
        screen.blit(go_text, (600, 350))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()