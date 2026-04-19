import pygame
import random
import sys
import os

pygame.init()

try:
    pygame.mixer.init()
    MIXER_AVAILABLE = True
except pygame.error:
    MIXER_AVAILABLE = False

WIDTH, HEIGHT = 800, 600
CELL = 20

MINIMAP_ENABLED = False

# 한국어 폰트 찾기
def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "nanumgothic", "notosanscjk"]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font.get_ascent() > 0:
            return font
    return pygame.font.SysFont(None, size)

font = get_korean_font(24)
font_small = get_korean_font(18)
font_big = get_korean_font(48)
warning_font = get_korean_font(20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 200, 50)
RED = (220, 50, 50)
GRAY = (40, 40, 40)
DARK_GRAY = (20, 120, 20)
OBSTACLE_COLOR = (120, 120, 120)
WARNING_COLOR = (255, 60, 60)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
world_surface = pygame.Surface((WIDTH, HEIGHT))

warning_glyph = warning_font.render("!", True, WARNING_COLOR)

# 경로 관련 함수
def resource_path(*parts):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, *parts)
# 최고 점수 저장용 파일 경로
def writable_path(filename):
    base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)


# 이미지 / 사운드 로드 함수
def load_image(*parts, size=None, alpha=True, fallback_color=(255, 0, 255)):
    path = resource_path(*parts)
    try:
        image = pygame.image.load(path)
        image = image.convert_alpha() if alpha else image.convert()
        if size is not None:
            image = pygame.transform.smoothscale(image, size)
        return image
    except Exception as e:
        print(f"[이미지 로드 실패] {path}: {e}")
        fallback = pygame.Surface(size if size else (CELL, CELL), pygame.SRCALPHA)
        fallback.fill(fallback_color)
        return fallback

def load_sound(*parts):
    if not MIXER_AVAILABLE:
        return None
    path = resource_path(*parts)
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"[사운드 로드 실패] {path}: {e}")
        return None

def play_sound(sound, duration=None):
    if MIXER_AVAILABLE and sound is not None:
        sound.play()
# duration이 지정되면 해당 시간 후 중지
        if duration is not None:
            pygame.time.set_timer(pygame.USEREVENT, duration)

def play_sound_limited(sound, duration_ms):
    """지정된 시간만 사운드 재생"""
    if MIXER_AVAILABLE and sound is not None:
        sound.play()
# 음성 길이 제한을 위해 타이머 설정
        pygame.time.set_timer(pygame.USEREVENT + 1, duration_ms)

def start_bgm():
    if not MIXER_AVAILABLE:
        return
    try:
        pygame.mixer.music.load(resource_path("asset", "sound", "background", "background.wav"))
        pygame.mixer.music.play(-1)  # 무한 반복
    except Exception as e:
        print(f"[배경음악 로드 실패] {e}")

# 배경
background_img = load_image(
    "asset", "image", "background", "RockBG.png",
    size=(WIDTH, HEIGHT),
    alpha=False,
    fallback_color=(50, 50, 50)
)

# 난이도 선택 화면 배경
start_img = load_image(
    "asset", "image", "background", "Start.png",
    size=(WIDTH, HEIGHT),
    alpha=False,
    fallback_color=(50, 50, 50)
)

# 게임오버 화면 배경
gameover_img = load_image(
    "asset", "image", "background", "GameOver.png",
    size=(WIDTH, HEIGHT),
    alpha=False,
    fallback_color=(50, 50, 50)
)

# 점수 아이템 / 독 / 장애물
potato_img = load_image(
    "asset", "image", "score", "potato.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(180, 120, 50)
)

poison_img = load_image(
    "asset", "image", "score", "poison.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(80, 20, 20)
)

rock_img_1 = load_image(
    "asset", "image", "score", "large_rock.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(120, 120, 120)
)

rock_img_2 = load_image(
    "asset", "image", "score", "rock_2.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(150, 150, 150)
)

rock_images = [rock_img_1, rock_img_2]

## 뱀 이미지
snake_body_base = load_image(
    "asset", "image", "snake", "snake_body.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(0, 200, 0)
)

snake_head_base = load_image(
    "asset", "image", "snake", "snake_Head.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(0, 255, 0)
)

snake_tail_base = load_image(
    "asset", "image", "snake", "snake_tail.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(0, 150, 0)
)

snake_corner_down_left = load_image(
    "asset", "image", "snake", "snake_Up_Left.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(0, 220, 0)
)

snake_corner_down_right = load_image(
    "asset", "image", "snake", "snake_Up_Right.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(0, 220, 0)
)

snake_corner_up_left = load_image(
    "asset", "image", "snake", "snake_Down_Left.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(0, 220, 0)
)

snake_corner_up_right = load_image(
    "asset", "image", "snake", "snake_Down_Right.png",
    size=(CELL, CELL),
    alpha=True,
    fallback_color=(0, 220, 0)
)

## 사운드 옵션 이미지
sound_option_img = load_image(
    "asset", "image", "background", "sound_option.png",
    size=(60, 60),
    alpha=True,
    fallback_color=(100, 100, 100)
)

# 사운드
eat_sound = load_sound("asset", "sound", "potato_crunch.wav")
poison_sound = load_sound("asset", "sound", "Mushroom.wav")
gameover_sound = load_sound("asset", "sound", "background", "gameover.wav")  # 게임오버 사운드

start_bgm()


## 사운드 볼륨 관리
class VolumeManager:
    def __init__(self):
        self.bgm_volume = 30 # 0-100
        self.sfx_volume = 70  # 0-100
        self.sound_timers = {}  # 사운드 중지 시간 (사운드별 관리)
        self.update_volumes()
    
    def update_volumes(self):
        if MIXER_AVAILABLE:
            pygame.mixer.music.set_volume(self.bgm_volume / 100.0)
# 효과음 볼륨은 Sound 객체에 직접 설정
    
    def set_bgm_volume(self, volume):
        self.bgm_volume = max(0, min(100, volume))
        self.update_volumes()
    
    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0, min(100, volume))
    
    def play_sound_with_volume(self, sound, duration_ms=None, sound_id=None):
        if MIXER_AVAILABLE and sound is not None:
# 기존 동일 사운드 중지 (동일 sound_id로 다시 재생 시)
            if sound_id is not None and sound_id in self.sound_timers:
# 기존 사운드 중지
                pass 
            
            sound.set_volume(self.sfx_volume / 100.0)
            sound.play()
# duration_ms가 지정되면 해당 시간 후 중지
            if duration_ms is not None and sound_id is not None:
                self.sound_timers[sound_id] = pygame.time.get_ticks() + duration_ms
    
    def play_gameover_sound(self, sound):
# 게임오버 사운드 재생 (BGM 볼륨으로 조절)
        if MIXER_AVAILABLE and sound is not None:
            sound.set_volume(self.bgm_volume / 100.0)  # BGM 볼륨으로 조절
            sound.play()
    
    def update_sound_timer(self):
# 게임 루프에서 호출하여 사운드 시간 제한 확인
        current_time = pygame.time.get_ticks()
        expired_ids = []
        
        for sound_id, stop_time in self.sound_timers.items():
            if current_time >= stop_time:
                expired_ids.append(sound_id)
        
# 만료된 사운드 중지 및 제거
        for sound_id in expired_ids:
            if MIXER_AVAILABLE:
                pygame.mixer.stop()  # 모든 사운드 중지
            del self.sound_timers[sound_id]

volume_manager = VolumeManager()

# 최고 점수 저장 / 불러오기
HIGHSCORE_FILE = "highscore.txt"

def load_highscore():
    path = writable_path(HIGHSCORE_FILE)
    if not os.path.exists(path):
        return 0
    try:
        with open(path, "r", encoding="utf-8") as f:
            return int(f.read().strip())
    except:
        return 0

def save_highscore(score):
    path = writable_path(HIGHSCORE_FILE)
    with open(path, "w", encoding="utf-8") as f:
        f.write(str(score))

# 게임 설정
LEVELS = {
    1: {"delay": 200, "label": "Easy", "camera": 15, "score_per_food": 10},
    2: {"delay": 140, "label": "Normal", "camera": 15, "score_per_food": 15},
    3: {"delay": 90, "label": "Hard", "camera": 15, "score_per_food": 40},
}

OBSTACLE_WARNING_TIME = 1500
OBSTACLE_ACTIVE_TIME = 3000
OBSTACLE_COOLDOWN_TIME = 3000
OBSTACLE_COUNT = 70

# 버섯 효과 설정
MUSHROOM_SPEED_BOOST = 1.5  # 50% 빨라짐
MUSHROOM_BOOST_DURATION = 5000  # 5초
MUSHROOM_RECOVERY_TIME = 0  # 복구 시간 (즉시 원래 속도로 복귀)

ALL_CELLS = [
    (x, y)
    for x in range(0, WIDTH, CELL)
    for y in range(0, HEIGHT, CELL)
]

def random_empty_cell(blocked):
    candidates = [pos for pos in ALL_CELLS if pos not in blocked]
    if not candidates:
        return None
    return random.choice(candidates)

def random_empty_cells(count, blocked):
    candidates = [pos for pos in ALL_CELLS if pos not in blocked]
    if not candidates:
        return set()
    return set(random.sample(candidates, min(count, len(candidates))))

# UI
def confirm_exit():
    yes_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 60, 100, 40)
    no_rect = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 60, 100, 40)

    while True:
        screen.fill(GRAY)

        text1 = font.render("뱀이 굶고 있습니다....", True, WHITE)
        text2 = font.render("정말 나가시겠습니까?", True, WHITE)

        rect1 = text1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
        rect2 = text2.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))

        screen.blit(text1, rect1)
        screen.blit(text2, rect2)

        pygame.draw.rect(screen, (80, 80, 80), yes_rect)
        pygame.draw.rect(screen, (80, 80, 80), no_rect)

        screen.blit(font_small.render("Yes (Q)", True, WHITE),
                    (yes_rect.x + 10, yes_rect.y + 10))
        screen.blit(font_small.render("No (X)", True, WHITE),
                    (no_rect.x + 5, no_rect.y + 10))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif e.key == pygame.K_x:
                    return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(e.pos):
                    pygame.quit()
                    sys.exit()
                elif no_rect.collidepoint(e.pos):
                    return

# 사운드 볼륨 조절 화면
def volume_control_screen():
    bgm_slider_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 40, 300, 20)
    sfx_slider_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 40, 300, 20)
    done_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 120, 100, 40)
    
    dragging_bgm = False
    dragging_sfx = False
    
    while True:
        screen.fill(GRAY)
        
# 제목
        title = font.render("음량 조절", True, GREEN)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
        
# BGM 
        screen.blit(font_small.render("배경 음악", True, WHITE), (WIDTH // 2 - 200, HEIGHT // 2 - 70))
        pygame.draw.rect(screen, (100, 100, 100), bgm_slider_rect)
        bgm_fill_width = (bgm_slider_rect.width * volume_manager.bgm_volume) // 100
        pygame.draw.rect(screen, GREEN, (bgm_slider_rect.x, bgm_slider_rect.y, bgm_fill_width, bgm_slider_rect.height))
        screen.blit(font_small.render(f"{volume_manager.bgm_volume}%", True, WHITE), (WIDTH // 2 + 160, HEIGHT // 2 - 50))
        
# 효과음 
        screen.blit(font_small.render("효과음", True, WHITE), (WIDTH // 2 - 200, HEIGHT // 2 + 10))
        pygame.draw.rect(screen, (100, 100, 100), sfx_slider_rect)
        sfx_fill_width = (sfx_slider_rect.width * volume_manager.sfx_volume) // 100
        pygame.draw.rect(screen, GREEN, (sfx_slider_rect.x, sfx_slider_rect.y, sfx_fill_width, sfx_slider_rect.height))
        screen.blit(font_small.render(f"{volume_manager.sfx_volume}%", True, WHITE), (WIDTH // 2 + 160, HEIGHT // 2 + 30))
        
# 완료 버튼
        pygame.draw.rect(screen, (80, 80, 80), done_rect)
        screen.blit(font_small.render("완료", True, WHITE), (done_rect.x + 25, done_rect.y + 10))
        
        pygame.display.flip()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                confirm_exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if done_rect.collidepoint(e.pos):
                    return
                if bgm_slider_rect.collidepoint(e.pos):
                    dragging_bgm = True
                    dragging_sfx = False
                elif sfx_slider_rect.collidepoint(e.pos):
                    dragging_sfx = True
                    dragging_bgm = False
            if e.type == pygame.MOUSEBUTTONUP:
                dragging_bgm = False
                dragging_sfx = False
            if e.type == pygame.MOUSEMOTION:
                if dragging_bgm:
                    relative_x = e.pos[0] - bgm_slider_rect.x
                    volume_manager.set_bgm_volume(int((relative_x / bgm_slider_rect.width) * 100))
                elif dragging_sfx:
                    relative_x = e.pos[0] - sfx_slider_rect.x
                    volume_manager.set_sfx_volume(int((relative_x / sfx_slider_rect.width) * 100))

def level_select_screen():
    global MINIMAP_ENABLED

    while True:
        screen.blit(start_img, (0, 0))
        
        screen.blit(font_small.render("Game Exit: Q", True, WHITE), (10, 10))

        title = font_big.render("SNAKE", True, GREEN)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 160))

        for lv, info in LEVELS.items():
            t = font.render(f"{lv}: {info['label']}", True, WHITE)
            screen.blit(t, (WIDTH // 2 - t.get_width() // 2, 240 + lv * 40))

        mini_text = "MiniMap: ON" if MINIMAP_ENABLED else "MiniMap: OFF"
        mini_color = GREEN if MINIMAP_ENABLED else RED
        screen.blit(font.render(f"M: {mini_text}", True, mini_color),
                    (WIDTH // 2 - 100, 420))
        
# 사운드 옵션 버튼 (우측 하단)
        sound_rect = pygame.Rect(WIDTH - 80, HEIGHT - 80, 60, 60)
        pygame.draw.rect(screen, (80, 80, 80), sound_rect)
        screen.blit(sound_option_img, sound_rect.topleft)
        screen.blit(font_small.render("S", True, WHITE), (WIDTH - 70, HEIGHT - 70))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                confirm_exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    confirm_exit()
                if e.key == pygame.K_m:
                    MINIMAP_ENABLED = not MINIMAP_ENABLED
                if e.key == pygame.K_s:
                    volume_control_screen()
                if e.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    return int(e.unicode)
            if e.type == pygame.MOUSEBUTTONDOWN:
                sound_rect = pygame.Rect(WIDTH - 80, HEIGHT - 80, 60, 60)
                if sound_rect.collidepoint(e.pos):
                    volume_control_screen()

def game_over_screen(score, highscore, death_reason=""):
    while True:
        screen.blit(gameover_img, (0, 0))

        # GAME OVER 텍스트 (중앙 정렬)
        gameover_text = font_big.render("GAME OVER", True, RED)
        screen.blit(gameover_text, (WIDTH // 2 - gameover_text.get_width() // 2, 200))
        
        # Score 텍스트 (중앙 정렬)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 280))
        
        # HighScore 텍스트 (중앙 정렬)
        highscore_text = font_small.render(f"HighScore: {highscore}", True, WHITE)
        screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, 320))
        
        # 사망 이유 표시 (중앙 정렬)
        if death_reason:
            reason_text = font_small.render(death_reason, True, (255, 200, 100))
            screen.blit(reason_text, (WIDTH // 2 - reason_text.get_width() // 2, 360))

        # 재시작/메뉴 텍스트 (중앙 정렬)
        restart_text = font.render("R: Restart   Q: Menu", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, 400))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                confirm_exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    start_bgm()  # 배경음 다시 시작
                    return "restart"
                elif e.key == pygame.K_q:
                    start_bgm()  # 배경음 다시 시작
                    return "menu"

# 뱀 방향 / 이미지 처리
def get_dir(from_pos, to_pos):
    return ((to_pos[0] - from_pos[0]) // CELL, (to_pos[1] - from_pos[1]) // CELL)

def rotate_cell_sprite(image, angle):
    rotated = pygame.transform.rotate(image, angle)
    if rotated.get_size() != (CELL, CELL):
        rotated = pygame.transform.smoothscale(rotated, (CELL, CELL))
    return rotated

def rotation_for_direction(direction):
    if direction == (0, 1):      # 아래
        return 0
    elif direction == (1, 0):    # 오른쪽
        return 90
    elif direction == (0, -1):   # 위
        return 180
    elif direction == (-1, 0):   # 왼쪽
        return -90
    return 0

def draw_snake(surface, snake):
    if not snake:
        return

    if len(snake) == 1:
        surface.blit(snake_head_base, snake[0])
        return

    # 머리
    head = snake[0]
    neck = snake[1]
    head_dir = get_dir(neck, head)
    head_img = rotate_cell_sprite(snake_head_base, rotation_for_direction(head_dir))
    surface.blit(head_img, head)

    # 몸통
    for i in range(1, len(snake) - 1):
        prev_seg = snake[i - 1]
        cur_seg = snake[i]
        next_seg = snake[i + 1]

        d1 = get_dir(cur_seg, prev_seg)
        d2 = get_dir(cur_seg, next_seg)

        dirs = {d1, d2}

        # snake_body_base가 '세로 방향' 원본이라고 가정
        if dirs == {(1, 0), (-1, 0)}:
            body_img = rotate_cell_sprite(snake_body_base, 90)   # 가로 몸통
        elif dirs == {(0, 1), (0, -1)}:
            body_img = snake_body_base                           # 세로 몸통
        elif dirs == {(0, -1), (-1, 0)}:
            body_img = snake_corner_up_left
        elif dirs == {(0, -1), (1, 0)}:
            body_img = snake_corner_up_right
        elif dirs == {(0, 1), (-1, 0)}:
            body_img = snake_corner_down_left
        elif dirs == {(0, 1), (1, 0)}:
            body_img = snake_corner_down_right
        else:
            body_img = snake_body_base

        if body_img.get_size() != (CELL, CELL):
            body_img = pygame.transform.smoothscale(body_img, (CELL, CELL))

        surface.blit(body_img, cur_seg)

# 꼬리
    tail = snake[-1]
    before_tail = snake[-2]
    tail_dir = get_dir(before_tail, tail)
    tail_img = rotate_cell_sprite(snake_tail_base, rotation_for_direction(tail_dir))
    surface.blit(tail_img, tail)

# 그리기
def draw_world(surface, snake, food, poison, obstacles, warning_cells, obstacle_image_map):
# 배경 이미지
    surface.blit(background_img, (0, 0))

# 아이템
    for f in food:
        surface.blit(potato_img, f)

# 독 아이템
    if poison is not None:
        surface.blit(poison_img, poison)

# 장애물
    for ob in obstacles:
        img = obstacle_image_map.get(ob)
        if img is not None:
            surface.blit(img, ob)
        else:
            pygame.draw.rect(surface, OBSTACLE_COLOR, (*ob, CELL, CELL))
            pygame.draw.rect(surface, BLACK, (*ob, CELL, CELL), 1)

# 장애물 경고 칸
    for w in warning_cells:
        cell_rect = pygame.Rect(*w, CELL, CELL)
        pygame.draw.rect(surface, WARNING_COLOR, cell_rect, 1)
        txt_rect = warning_glyph.get_rect(center=cell_rect.center)
        surface.blit(warning_glyph, txt_rect)

# 뱀
    draw_snake(surface, snake)

# 눈금은 배경 위에서도 보이도록 마지막에 그림
    for x in range(0, WIDTH, CELL):
        pygame.draw.line(surface, (20, 20, 20), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL):
        pygame.draw.line(surface, (20, 20, 20), (0, y), (WIDTH, y))

def draw_minimap(surface, snake, food, poison, obstacles, warning_cells):
    mini_size = 120
    mini = pygame.Surface((mini_size, mini_size), pygame.SRCALPHA)
    mini.fill((30, 30, 30, 120))

    scale_x = mini_size / WIDTH
    scale_y = mini_size / HEIGHT

    for f in food:
        pygame.draw.rect(mini, (220, 50, 50, 200),
                         (f[0] * scale_x, f[1] * scale_y, CELL * scale_x, CELL * scale_y))

# 버섯(poison) 미니맵에 표시 안 함

    for ob in obstacles:
        pygame.draw.rect(mini, (160, 160, 160, 220),
                         (ob[0] * scale_x, ob[1] * scale_y, CELL * scale_x, CELL * scale_y))

    for w in warning_cells:
        pygame.draw.rect(mini, (255, 80, 80, 180),
                         (w[0] * scale_x, w[1] * scale_y, CELL * scale_x, CELL * scale_y))

    for s in snake:
        pygame.draw.rect(mini, (50, 200, 50, 200),
                         (s[0] * scale_x, s[1] * scale_y, CELL * scale_x, CELL * scale_y))

    pygame.draw.rect(mini, (255, 255, 255, 180), (0, 0, mini_size, mini_size), 2)
    surface.blit(mini, (10, 10))

def draw_hud(score, highscore):
    s = font.render(f"Score: {score}", True, WHITE)
    h = font_small.render(f"HighScore: {highscore}", True, WHITE)

    screen.blit(s, (WIDTH // 2 - s.get_width() // 2, 10))
    screen.blit(h, (WIDTH // 2 - h.get_width() // 2, 40))

# 충돌 처리
def resolve_obstacle_spawn_on_snake(snake, obstacles):
    if snake[0] in obstacles:
        return "dead", 0

    cut_index = None
    for i in range(1, len(snake)):
        if snake[i] in obstacles:
            cut_index = i
            break

    if cut_index is not None:
        removed_count = len(snake) - cut_index
        del snake[cut_index:]
        return "cut", removed_count

    return "safe", 0

# 게임 로직
def run_game(level):
    CAMERA_SIZE = LEVELS[level]["camera"]
    SCORE_PER_FOOD = LEVELS[level]["score_per_food"]

    snake = [(WIDTH // 2, HEIGHT // 2), (WIDTH // 2 - CELL, HEIGHT // 2)]
    direction = (CELL, 0)
    queue = []

    food = []
    for _ in range(5):
        pos = random_empty_cell(set(snake) | set(food))
        if pos is not None:
            food.append(pos)

    poison = random_empty_cell(set(snake) | set(food))

    score = 0
    highscore = load_highscore()
    move_timer = 0

    obstacles = set()
    warning_cells = set()
    obstacle_image_map = {}

    obstacle_state = "cooldown"
    obstacle_timer = 0
    
# 버섯 효과 관련
    mushroom_active = False
    mushroom_timer = 0
    mushroom_recovery_timer = 0
    current_delay = LEVELS[level]["delay"]
    
# 버섯 보너스 점수 관련
    last_bonus_time = 0  # 마지막 보너스 적용 시간

    def end_game(death_reason=""):
        nonlocal highscore
# 게임오버 시 모든 사운드 중지
        if MIXER_AVAILABLE:
            pygame.mixer.music.stop()  # 배경음 명시적 중지
            pygame.mixer.stop()  # 모든 효과음 중지
        volume_manager.sound_timers.clear()  # 사운드 타이머 초기화
        
# 게임오버 사운드 재생
        volume_manager.play_gameover_sound(gameover_sound)
        
        if score > highscore:
            highscore = score
            save_highscore(score)
        return game_over_screen(score, highscore, death_reason)

    while True:
        dt = clock.tick(60)
        move_timer += dt
        obstacle_timer += dt
        
# 사운드 시간 제한 업데이트
        volume_manager.update_sound_timer()
        
# 버섯 효과 타이머 관리
        if mushroom_active:
            mushroom_timer += dt
            
# 0.1초마다 2점 추가 (1초 20점 = 0.1초 2점)
            current_time = pygame.time.get_ticks()
            if current_time - last_bonus_time >= 100:  # 100ms = 0.1초
                score += 2
                last_bonus_time = current_time
            
            if mushroom_timer >= MUSHROOM_BOOST_DURATION:
                mushroom_active = False
                mushroom_timer = 0
                current_delay = LEVELS[level]["delay"]  # 즉시 원래 속도로 복귀

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                confirm_exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    queue.append((0, -CELL))
                if e.key == pygame.K_DOWN:
                    queue.append((0, CELL))
                if e.key == pygame.K_LEFT:
                    queue.append((-CELL, 0))
                if e.key == pygame.K_RIGHT:
                    queue.append((CELL, 0))

# 장애물 사이클
        if obstacle_state == "cooldown" and obstacle_timer >= OBSTACLE_COOLDOWN_TIME:
            obstacle_state = "warning"
            obstacle_timer = 0
            blocked = set(snake) | set(food)
            if poison is not None:
                blocked.add(poison)
            warning_cells = random_empty_cells(OBSTACLE_COUNT, blocked)

        elif obstacle_state == "warning" and obstacle_timer >= OBSTACLE_WARNING_TIME:
            obstacle_state = "active"
            obstacle_timer = 0
            obstacles = set(warning_cells)
            warning_cells.clear()

            obstacle_image_map = {
                pos: random.choice(rock_images)
                for pos in obstacles
            }

            result, removed_count = resolve_obstacle_spawn_on_snake(snake, obstacles)

            if result == "dead":
                return end_game("머리만 남아서 사망하였습니다")
            elif result == "cut":
                score -= removed_count * 3
# 머리만 남았는지 확인
                if len(snake) <= 1:
                    return end_game("머리만 남아서 사망하였습니다")

            if any(part in obstacles for part in snake):
                return end_game("정신을 차려보니 밤이었습니다")

        elif obstacle_state == "active" and obstacle_timer >= OBSTACLE_ACTIVE_TIME:
            obstacle_state = "cooldown"
            obstacle_timer = 0
            obstacles.clear()
            obstacle_image_map.clear()

# 뱀 이동
        if move_timer >= current_delay:
            move_timer = 0

            if queue:
                nd = queue.pop(0)
                if not (nd[0] == -direction[0] and nd[1] == -direction[1]):
                    direction = nd

            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

# 사망 원인 판단
            death_reason = ""
            if head in snake:
                death_reason = "꼬리에 부딪쳤습니다"
            elif head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
                death_reason = "길을 잃었습니다"
            elif head in obstacles:
                death_reason = "정신을 차려보니 밤이었습니다"
            
            if death_reason:
                return end_game(death_reason)

            snake.insert(0, head)

            if head in food:
                score += SCORE_PER_FOOD
                volume_manager.play_sound_with_volume(eat_sound, sound_id="eat")
                food.remove(head)

                blocked = set(snake) | set(food) | obstacles | warning_cells
                if poison is not None:
                    blocked.add(poison)

                new_food = random_empty_cell(blocked)
                if new_food is not None:
                    food.append(new_food)

            elif poison is not None and head == poison:
## 버섯 효과: 5초간 50% 빨라짐
                mushroom_active = True
                mushroom_timer = 0
                last_bonus_time = pygame.time.get_ticks()
                current_delay = int(LEVELS[level]["delay"] / MUSHROOM_SPEED_BOOST)
## Mushroom.wav 5초만 재생
                volume_manager.play_sound_with_volume(poison_sound, 5000, sound_id="mushroom")

## 꼬리 3칸 감소
                for _ in range(min(3, len(snake) - 2)):
                    snake.pop()
                
## 머리만 남았는지 확인
                if len(snake) <= 1:
                    return end_game("머리만 남아서 사망하였습니다")

                blocked = set(snake) | set(food) | obstacles | warning_cells
                poison = random_empty_cell(blocked)

            else:
                snake.pop()

            if score > highscore:
                highscore = score

        draw_world(world_surface, snake, food, poison, obstacles, warning_cells, obstacle_image_map)

        hx, hy = snake[0]
        cam_x = max(0, min(hx - (CAMERA_SIZE // 2) * CELL, WIDTH - CAMERA_SIZE * CELL))
        cam_y = max(0, min(hy - (CAMERA_SIZE // 2) * CELL, HEIGHT - CAMERA_SIZE * CELL))

        view = world_surface.subsurface((cam_x, cam_y, CAMERA_SIZE * CELL, CAMERA_SIZE * CELL))
        view = pygame.transform.scale(view, (WIDTH, HEIGHT))

        screen.blit(view, (0, 0))
        draw_hud(score, highscore)

        if MINIMAP_ENABLED:
            draw_minimap(screen, snake, food, poison, obstacles, warning_cells)

        pygame.display.flip()

# 메인 루프
def main():
    while True:
        level = level_select_screen()
        while True:
            result = run_game(level)

            if result == "restart":
                continue
            elif result == "menu":
                break

main()