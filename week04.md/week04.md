import pygame
import sys
import base64
from io import BytesIO

pygame.init()

# ====== 창 설정 ======
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Collision Detection with Image Size")

# ====== 색상 ======
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 150, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# ====== 글꼴 ======
font = pygame.font.SysFont(None, 30)

# ====== Base64 스프라이트 로드 ======
sprite_base64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAEYAAABGCAYAAABxLuKEAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFn"
    "ZVJlYWR5ccllPAAAAyFpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/"
    "IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6"
    "bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNS1jMDE0IDc5LjE1MTQ4MSwgMjAxMy8w"
    "My8xMy0xMjowOToxNSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9y"
    "Zy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIg"
    "eG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDov"
    "L25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20v"
    "eGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9w"
    "IENDIChXaW5kb3dzKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo3NUNEOEIwMTczMzQxMUUzQjlD"
    "NUI3NDgxQTNDMkQ3OCIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo3NUNEOEIwMjczMzQxMUUzQjlD"
    "NUI3NDgxQTNDMkQ3OCI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlk"
    "Ojc1Q0Q4QUZGNzMzNDExRTNCOUM1Qjc0ODFBM0MyRDc4IiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlk"
    "Ojc1Q0Q4QjAwNzMzNDExRTNCOUM1Qjc0ODFBM0MyRDc4Ii8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3Jk"
    "ZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+OwGVngAAA0NJREFUeNrsnMFqGkEY"
    "x2fWRXuRCH2A+AaxJVBoD90+QU4VSQt6qDWhFyk99BaPPZTUSyHGHlIKRexDdAsVagll8gbmDQwGWs3u"
    "fJ1tbJqiu+6664zOzoAo7mBmf/6///efZQ0GAKTG5MAKjAKjwKwEGIyxr3nfD3fvW+fn6O7zD1/8zF/0"
    "uvVl+YYohRpgmmEvby3DerRlWES3sVvECBtMX7mv+4+KqpTYOG48XbNAIwxM1vo5QGw1/RvDYXbz5acz"
    "kaUkXDE20qoOlCuQCGV+pZK1WCvmx7tn6xcWJeyl4y3IUcw/YjR778XH01gqZmTZtb9QJk48oR3F0nyd"
    "9sxKqOSqNISMzv72VuzAOO3ZRx3WYwXm20Fl67I9zyST7bx5vBcjxfhXArPYauf19rr0YLqNnb3r7Xkm"
    "QsecE5h7++barp0wZ0Oi59aJ/mvXEwvFxvV9lFTtmiXcuhuUmSWFaV3KUuoeVDa82rMP7XHdR3EDAyiC"
    "1sva9/Grh2vSgBmrxQjNhZXhKJkqSQPmzk7jJEI7J5KVEphRfI7fK3wrA0aL5JsGwm+9vPZGiJrhVYdM"
    "6cAkdZ1EUI/yKeb2k7enzGd6oWyXgnyKuWy38/uMcy3Y64reSoOBED6DOfqLAMXMf3IYJAYTLuhhIi2Y"
    "MEGPV7ATBgbj4CUBnP1FjGJgnvQKRHowOg5eShhAfsVsVg7PAgc9iuRXzHgEUAD0eAY7wWCCeAYmIlYo"
    "BEyQoMc72AkFEyzoxUgxQYIe72AnHIyfoCci2IlXjK+gByR2YPwEPRHBTjgYJ+ixJ09FpEYX8QMzNmDi"
    "Fexm3bkpLRiMsRlNOpYMDAJK3P0Fk9iCGQe9/rRjNohVzMJvHGq320X2N0pux5PWIKch+889M2DbV+8P"
    "UzdNjxI8yufz7xfaNTnAz7KH4XZwpKfdVmOI9J+l+JHFMg4FRmAp9dykPxgMcpZlTb0nT9f1fjqdJh6f"
    "udrm6/Uji3K5/JkdN1z2Umaz2XzgsddSpaQ8RoFRYBQYBUaBUWDUUGCWPPm2Wq0N9lT3uSWoFgqFE97J"
    "V8j/dtA0LUMpNdiJe01zgBnOXFVKMdtdTxuEKcHwO1dKj1HmK9n4LcAAwvdMMLRYaKIAAAAASUVORK5C"
    "YII="
)
sprite_data = base64.b64decode(sprite_base64)
sprite_image = pygame.image.load(BytesIO(sprite_data)).convert_alpha()

# ====== 플레이어와 고정 오브젝트 생성 ======
player_sprite = pygame.transform.scale(sprite_image, (100, 80))
fixed_sprite_original = pygame.transform.scale(sprite_image, (120, 90))

player_width, player_height = player_sprite.get_size()
fixed_width, fixed_height = fixed_sprite_original.get_size()

player = pygame.Rect(100, 100, player_width, player_height)
fixed = pygame.Rect(0, 0, fixed_width, fixed_height)
fixed.center = (400, 300)

# ====== 회전 변수 ======
rotation_speed = 1       # 기본 속도
fast_rotation_speed = 5  # Z키 누르면 빨라짐
fixed_angle = 0

clock = pygame.time.Clock()
FPS = 60
speed = 3

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    # 플레이어 이동
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    # Z키로 회전 속도 조절
    current_rotation_speed = fast_rotation_speed if keys[pygame.K_z] else rotation_speed
    fixed_angle += current_rotation_speed

    # 회전 처리
    rotated_fixed_sprite = pygame.transform.rotate(fixed_sprite_original, fixed_angle)
    rotated_rect = rotated_fixed_sprite.get_rect(center=fixed.center)

    # 중심 좌표
    player_center = player.center
    fixed_center = fixed.center
    player_radius = max(player_width, player_height) // 2
    fixed_radius = max(fixed_width, fixed_height) // 2

    # ======== 충돌 감지 ========
    # 1. 원형 충돌
    dx = player_center[0] - fixed_center[0]
    dy = player_center[1] - fixed_center[1]
    circle_collision = dx*dx + dy*dy <= (player_radius + fixed_radius)**2

    # 2. AABB 충돌
    aabb_collision = player.colliderect(rotated_rect)

    # 3. OBB 충돌 (근사)
    obb_points = [
        rotated_rect.topleft,
        rotated_rect.topright,
        rotated_rect.bottomright,
        rotated_rect.bottomleft
    ]
    obb_collision = aabb_collision  # 근사로 표시

    # ======== 화면 표시 ========
    bg_color = YELLOW if circle_collision else BLACK
    screen.fill(bg_color)

    screen.blit(player_sprite, player.topleft)
    screen.blit(rotated_fixed_sprite, rotated_rect.topleft)

    # 디버깅용
    pygame.draw.rect(screen, RED, player, 2)                      # 플레이어 AABB
    pygame.draw.circle(screen, BLUE, player_center, player_radius, 2)  # 플레이어 원형
    pygame.draw.rect(screen, RED, rotated_rect, 2)               # 회전 이미지 AABB
    pygame.draw.circle(screen, BLUE, fixed_center, fixed_radius, 2)    # 고정 원형
    pygame.draw.polygon(screen, GREEN, obb_points, 2)            # OBB

    # 화면 왼쪽 상단 충돌 결과
    status_texts = [
        f"Circle: {'HIT' if circle_collision else 'OK'}",
        f"AABB: {'HIT' if aabb_collision else 'OK'}",
        f"OBB: {'HIT' if obb_collision else 'OK'}"
    ]
    for i, text in enumerate(status_texts):
        img = font.render(text, True, WHITE)
        screen.blit(img, (10, 10 + i*30))

    pygame.display.flip()

pygame.quit()
sys.exit()