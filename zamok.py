import pygame
import sys
import random
import math
import os

# Инициализация Pygame
pygame.init()
pygame.mouse.set_visible(False)

# Установка полноэкранного режима
screen_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Темный Принц: Восхождение Тьмы")

# Загрузка кастомных шрифтов
try:
    title_font = pygame.font.Font("dark_font.ttf", 72)
    main_font = pygame.font.Font("dark_font.ttf", 36)
    small_font = pygame.font.Font("dark_font.ttf", 24)
except:
    title_font = pygame.font.SysFont("arial", 72, bold=True)
    main_font = pygame.font.SysFont("arial", 36)
    small_font = pygame.font.SysFont("arial", 24)

# Цвета в мрачной теме
BLACK = (0, 0, 0)
DARK_GRAY = (30, 30, 30)
BLOOD_RED = (136, 8, 8)
DARK_RED = (80, 0, 0)
DARK_PURPLE = (40, 0, 60)
DARK_GOLD = (180, 150, 50)
DARK_SILVER = (100, 100, 120)
LIGHT_BLUE = (100, 150, 200)
ASH_GRAY = (80, 80, 80)
BONE_WHITE = (220, 220, 200)

# Функция для загрузки изображений с обработкой ошибок
def load_image(name, size=None):
    try:
        image = pygame.image.load(name)
        if size:
            image = pygame.transform.scale(image, size)
        return image.convert_alpha()
    except pygame.error:
        print(f"Не могу загрузить изображение: {name}")
        # Создаем заглушку если изображение не найдено
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
        surf.fill((*color, 200))
        font = pygame.font.SysFont(None, 20)
        text = font.render(name.split('/')[-1].split('\\')[-1], True, BONE_WHITE)
        text_rect = text.get_rect(center=(25, 25))
        surf.blit(text, text_rect)
        return surf

# Функции для создания более детализированных текстур персонажей
def create_detailed_dark_prince(size):
    texture = pygame.Surface(size, pygame.SRCALPHA)
    # Тело
    pygame.draw.ellipse(texture, (60, 40, 80), (10, 30, size[0]-20, size[1]-40))
    # Голова
    pygame.draw.circle(texture, (80, 60, 100), (size[0]//2, 20), 15)
    # Плащ
    pygame.draw.polygon(texture, (40, 20, 60), [
        (5, 30), (size[0]-5, 30), 
        (size[0]-5, size[1]-10), (size[0]-25, size[1]-5),
        (25, size[1]-5), (5, size[1]-10)
    ])
    # Корона
    pygame.draw.rect(texture, DARK_GOLD, (size[0]//2-12, 5, 24, 10))
    for i in range(5):
        pygame.draw.rect(texture, DARK_GOLD, (size[0]//2-12 + i*6, 0, 3, 10))
    # Глаза
    pygame.draw.circle(texture, (200, 50, 50), (size[0]//2-8, 18), 4)
    pygame.draw.circle(texture, (200, 50, 50), (size[0]//2+8, 18), 4)
    # Меч
    pygame.draw.rect(texture, (200, 200, 220), (size[0]//2-2, 40, 4, 30))
    pygame.draw.rect(texture, (120, 80, 40), (size[0]//2-5, 70, 10, 8))
    return texture

def create_detailed_skeleton(size):
    texture = pygame.Surface(size, pygame.SRCALPHA)
    # Череп
    pygame.draw.circle(texture, (200, 200, 200), (size[0]//2, 15), 12)
    # Глазницы
    pygame.draw.ellipse(texture, (40, 40, 40), (size[0]//2-8, 10, 6, 8))
    pygame.draw.ellipse(texture, (40, 40, 40), (size[0]//2+2, 10, 6, 8))
    # Тело (позвоночник)
    pygame.draw.rect(texture, (180, 180, 180), (size[0]//2-4, 25, 8, 25))
    # Ребра
    for i in range(3):
        y_pos = 30 + i*8
        pygame.draw.ellipse(texture, (160, 160, 160), (size[0]//2-10, y_pos, 20, 6))
    # Руки
    pygame.draw.line(texture, (180, 180, 180), (size[0]//2, 30), (size[0]//2-15, 45), 4)
    pygame.draw.line(texture, (180, 180, 180), (size[0]//2, 30), (size[0]//2+15, 45), 4)
    # Ноги
    pygame.draw.line(texture, (180, 180, 180), (size[0]//2, 50), (size[0]//2-10, 70), 4)
    pygame.draw.line(texture, (180, 180, 180), (size[0]//2, 50), (size[0]//2+10, 70), 4)
    # Меч
    pygame.draw.rect(texture, (150, 150, 160), (size[0]//2-15, 40, 3, 25))
    return texture

def create_detailed_demon(size):
    texture = pygame.Surface(size, pygame.SRCALPHA)
    # Тело
    pygame.draw.ellipse(texture, (160, 40, 40), (10, 20, size[0]-20, size[1]-30))
    # Голова
    pygame.draw.circle(texture, (180, 60, 60), (size[0]//2, 15), 12)
    # Рога
    pygame.draw.polygon(texture, (120, 60, 40), [(size[0]//2-8, 5), (size[0]//2-15, 0), (size[0]//2-8, 10)])
    pygame.draw.polygon(texture, (120, 60, 40), [(size[0]//2+8, 5), (size[0]//2+15, 0), (size[0]//2+8, 10)])
    # Глаза
    pygame.draw.circle(texture, (255, 255, 0), (size[0]//2-5, 15), 3)
    pygame.draw.circle(texture, (255, 255, 0), (size[0]//2+5, 15), 3)
    # Крылья
    pygame.draw.ellipse(texture, (120, 30, 30, 150), (-10, 25, 40, 20))
    pygame.draw.ellipse(texture, (120, 30, 30, 150), (size[0]-30, 25, 40, 20))
    # Хвост
    pygame.draw.ellipse(texture, (140, 40, 40), (size[0]//2-2, size[1]-20, 4, 15))
    pygame.draw.circle(texture, (180, 80, 80), (size[0]//2, size[1]-5), 4)
    return texture

def create_detailed_ghost(size):
    texture = pygame.Surface(size, pygame.SRCALPHA)
    # Призрачное тело
    points = []
    for i in range(10):
        angle = math.pi * i / 9
        radius = 15 + random.randint(-3, 3)
        x = size[0]//2 + math.cos(angle) * radius
        y = 20 + math.sin(angle) * radius
        points.append((x, y))
    
    for i in range(10, 20):
        angle = math.pi * i / 9
        radius = 25 + random.randint(-5, 5)
        x = size[0]//2 + math.cos(angle) * radius
        y = 40 + math.sin(angle) * radius
        points.append((x, y))
    
    pygame.draw.polygon(texture, (200, 200, 220, 180), points)
    
    # Глаза
    pygame.draw.circle(texture, (100, 100, 200, 220), (size[0]//2-6, 25), 4)
    pygame.draw.circle(texture, (100, 100, 200, 220), (size[0]//2+6, 25), 4)
    
    # Руки
    pygame.draw.ellipse(texture, (180, 180, 200, 160), (size[0]//2-20, 35, 10, 15))
    pygame.draw.ellipse(texture, (180, 180, 200, 160), (size[0]//2+10, 35, 10, 15))
    
    return texture

def create_detailed_dragon(size):
    texture = pygame.Surface(size, pygame.SRCALPHA)
    # Тело
    pygame.draw.ellipse(texture, (200, 80, 40), (50, 40, size[0]-100, size[1]-60))
    # Голова
    pygame.draw.circle(texture, (220, 100, 60), (size[0]//2, 30), 20)
    # Шея
    pygame.draw.ellipse(texture, (180, 70, 35), (size[0]//2-15, 30, 30, 40))
    # Глаза
    pygame.draw.circle(texture, (255, 255, 0), (size[0]//2-8, 25), 6)
    pygame.draw.circle(texture, (255, 255, 0), (size[0]//2+8, 25), 6)
    # Рога
    pygame.draw.polygon(texture, (150, 100, 50), [(size[0]//2-15, 15), (size[0]//2-25, 5), (size[0]//2-10, 10)])
    pygame.draw.polygon(texture, (150, 100, 50), [(size[0]//2+15, 15), (size[0]//2+25, 5), (size[0]//2+10, 10)])
    # Крылья
    wing_points = [
        (80, 50), (20, 30), (10, 60), (40, 80), (80, 70)
    ]
    pygame.draw.polygon(texture, (180, 70, 35, 180), wing_points)
    
    wing_points2 = [
        (size[0]-80, 50), (size[0]-20, 30), (size[0]-10, 60), (size[0]-40, 80), (size[0]-80, 70)
    ]
    pygame.draw.polygon(texture, (180, 70, 35, 180), wing_points2)
    # Хвост
    tail_points = [
        (size[0]-50, size[1]//2), (size[0]-10, size[1]//2-10), 
        (size[0]-5, size[1]//2+10), (size[0]-40, size[1]//2+5)
    ]
    pygame.draw.polygon(texture, (180, 70, 35), tail_points)
    # Ноги
    pygame.draw.rect(texture, (180, 70, 35), (70, size[1]-40, 15, 30))
    pygame.draw.rect(texture, (180, 70, 35), (size[0]-85, size[1]-40, 15, 30))
    
    # Пламя из пасти
    for i in range(5):
        flame_height = random.randint(5, 15)
        flame_width = random.randint(3, 8)
        flame_x = size[0]//2 - 10 + i*5
        pygame.draw.ellipse(texture, (255, 200, 0), (flame_x, 45, flame_width, flame_height))
        pygame.draw.ellipse(texture, (255, 100, 0), (flame_x, 45, flame_width, flame_height//2))
    
    return texture

# Функции для создания фонов разных уровней
def create_detailed_background_level1():
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Градиент от темно-серого к черному
    for y in range(SCREEN_HEIGHT):
        shade = max(10, 50 - y // 20)
        pygame.draw.line(bg, (shade, shade, shade), (0, y), (SCREEN_WIDTH, y))
    
    # Гробница - каменные стены
    for x in range(0, SCREEN_WIDTH, 50):
        for y in range(0, SCREEN_HEIGHT, 50):
            stone_color = (random.randint(30, 50), random.randint(25, 45), random.randint(20, 40))
            pygame.draw.rect(bg, stone_color, (x, y, 50, 50), 1)
            # Трещины на камнях
            if random.random() > 0.7:
                crack_x = x + random.randint(5, 45)
                pygame.draw.line(bg, (20, 20, 20), (crack_x, y+5), (crack_x, y+45), 1)
    
    # Саркофаги
    for i in range(3):
        x = 200 + i * 300
        y = SCREEN_HEIGHT - 150
        pygame.draw.rect(bg, (40, 35, 30), (x, y, 120, 80))
        pygame.draw.rect(bg, (50, 45, 35), (x+10, y+10, 100, 60))
        # Крышка саркофага
        pygame.draw.polygon(bg, (35, 30, 25), [(x, y), (x+120, y), (x+100, y-20), (x+20, y-20)])
    
    # Светящиеся грибы
    for i in range(10):
        x = random.randint(50, SCREEN_WIDTH-50)
        y = random.randint(SCREEN_HEIGHT-200, SCREEN_HEIGHT-100)
        # Ножка гриба
        pygame.draw.rect(bg, (120, 100, 80), (x, y, 5, 15))
        # Шляпка
        pygame.draw.ellipse(bg, (150, 50, 150, 100), (x-10, y-5, 25, 10))
        # Свечение
        for r in range(3, 0, -1):
            alpha = 50 - r * 15
            glow = pygame.Surface((30 + r*10, 20 + r*5), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (150, 50, 150, alpha), (0, 0, 30 + r*10, 20 + r*5))
            bg.blit(glow, (x-15 - r*5, y-10 - r*2))
    
    return bg

def create_detailed_background_level2():
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Градиент адского неба
    for y in range(SCREEN_HEIGHT):
        r = min(100, 30 + y // 10)
        g = max(0, 10 - y // 20)
        b = max(0, 5 - y // 30)
        pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Лавовые реки
    lava_y = SCREEN_HEIGHT - 100
    lava_points = []
    for x in range(0, SCREEN_WIDTH, 10):
        y_offset = math.sin(x / 50) * 20
        lava_points.append((x, lava_y + y_offset))
    
    if len(lava_points) > 1:
        pygame.draw.polygon(bg, (150, 50, 0), [(0, SCREEN_HEIGHT)] + lava_points + [(SCREEN_WIDTH, SCREEN_HEIGHT)])
        
        # Пузыри лавы
        for i in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(lava_y - 30, SCREEN_HEIGHT)
            size = random.randint(5, 15)
            pygame.draw.circle(bg, (255, 100, 0), (x, y), size)
            pygame.draw.circle(bg, (255, 150, 50), (x, y), size-3)
    
    # Врата ада - каменные арки
    for i in range(3):
        x = 150 + i * 350
        arch_height = 300
        arch_width = 100
        
        # Колонны
        pygame.draw.rect(bg, (60, 50, 40), (x, SCREEN_HEIGHT - arch_height, 20, arch_height))
        pygame.draw.rect(bg, (60, 50, 40), (x + arch_width - 20, SCREEN_HEIGHT - arch_height, 20, arch_height))
        
        # Арка
        pygame.draw.arc(bg, (60, 50, 40), (x, SCREEN_HEIGHT - arch_height - 50, arch_width, 100), math.pi, 2*math.pi, 20)
        
        # Пламя внутри арок
        for j in range(5):
            flame_x = x + 20 + j * 15
            flame_height = random.randint(50, 100)
            flame_points = [
                (flame_x, SCREEN_HEIGHT),
                (flame_x - 10, SCREEN_HEIGHT - flame_height),
                (flame_x, SCREEN_HEIGHT - flame_height - 20),
                (flame_x + 10, SCREEN_HEIGHT - flame_height),
                (flame_x, SCREEN_HEIGHT)
            ]
            pygame.draw.polygon(bg, (255, 100, 0), flame_points)
            pygame.draw.polygon(bg, (255, 200, 0), flame_points, 2)
    
    return bg

def create_detailed_background_level3():
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Градиент для логова дракона
    for y in range(SCREEN_HEIGHT):
        r = min(80, 40 + y // 15)
        g = max(0, 20 - y // 25)
        b = max(0, 10 - y // 35)
        pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Пещера - сталактиты и сталагмиты
    for i in range(30):
        # Сталактиты (сверху)
        x = random.randint(0, SCREEN_WIDTH)
        width = random.randint(5, 20)
        height = random.randint(20, 60)
        points = [
            (x, 0),
            (x - width, height),
            (x + width, height)
        ]
        pygame.draw.polygon(bg, (70, 60, 50), points)
        
        # Сталагмиты (снизу)
        x = random.randint(0, SCREEN_WIDTH)
        width = random.randint(5, 25)
        height = random.randint(30, 80)
        points = [
            (x, SCREEN_HEIGHT),
            (x - width, SCREEN_HEIGHT - height),
            (x + width, SCREEN_HEIGHT - height)
        ]
        pygame.draw.polygon(bg, (70, 60, 50), points)
    
    # Сокровища дракона
    treasure_x = SCREEN_WIDTH // 2 - 200
    treasure_y = SCREEN_HEIGHT - 150
    
    # Золотые монеты
    for i in range(100):
        coin_x = treasure_x + random.randint(0, 400)
        coin_y = treasure_y + random.randint(0, 100)
        pygame.draw.circle(bg, (255, 215, 0), (coin_x, coin_y), 5)
        pygame.draw.circle(bg, (200, 150, 0), (coin_x, coin_y), 3)
    
    # Драгоценные камни
    gem_colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 0, 255)]
    for i in range(20):
        gem_x = treasure_x + random.randint(0, 400)
        gem_y = treasure_y + random.randint(0, 100)
        color = random.choice(gem_colors)
        size = random.randint(8, 15)
        pygame.draw.rect(bg, color, (gem_x, gem_y, size, size))
        pygame.draw.rect(bg, (255, 255, 255), (gem_x, gem_y, size, size), 1)
    
    # Кости жертв
    for i in range(10):
        bone_x = random.randint(100, SCREEN_WIDTH-100)
        bone_y = SCREEN_HEIGHT - 80
        # Череп
        pygame.draw.circle(bg, (200, 200, 200), (bone_x, bone_y), 10)
        # Глазницы
        pygame.draw.circle(bg, (50, 50, 50), (bone_x-3, bone_y-2), 2)
        pygame.draw.circle(bg, (50, 50, 50), (bone_x+3, bone_y-2), 2)
        # Ребра
        for j in range(3):
            pygame.draw.ellipse(bg, (180, 180, 180), (bone_x-15+j*10, bone_y+15, 8, 15))
    
    return bg

def create_potion_texture():
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    # Бутылка
    pygame.draw.ellipse(surf, (100, 100, 150), (5, 5, 30, 35))
    # Жидкость
    pygame.draw.ellipse(surf, (200, 20, 20), (8, 10, 24, 25))
    # Горлышко
    pygame.draw.rect(surf, (150, 150, 180), (17, 0, 6, 8))
    return surf

def create_sword_texture():
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    # Клинок
    pygame.draw.polygon(surf, (200, 200, 220), [(10, 5), (40, 5), (40, 15), (10, 15)])
    # Рукоять
    pygame.draw.rect(surf, (120, 80, 40), (5, 10, 10, 30))
    # Навершие
    pygame.draw.circle(surf, (180, 150, 50), (10, 45), 5)
    return surf

def create_cursor_texture():
    surf = pygame.Surface((25, 25), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 255, 255), (12, 12), 10, 2)
    pygame.draw.line(surf, (255, 255, 255), (12, 2), (12, 8), 2)
    pygame.draw.line(surf, (255, 255, 255), (2, 12), (8, 12), 2)
    return surf

# Загрузка/создание текстур
try:
    # Загрузка фонов для разных уровней
    bg_level1 = load_image("backgrounds/bg_level1.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_level2 = load_image("backgrounds/bg_level2.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_level3 = load_image("backgrounds/bg_level3.png", (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Загрузка персонажей с прозрачным фоном
    dark_prince_img = load_image("characters/dark_prince.png", (80, 100))
    skeleton_img = load_image("characters/skeleton.png", (60, 80))
    demon_img = load_image("characters/demon.png", (70, 90))
    ghost_img = load_image("characters/ghost.png", (65, 85))
    dragon_img = load_image("characters/dragon.png", (200, 140))
    
except Exception as e:
    print(f"Ошибка загрузки изображений: {e}")
    print("Создаются детализированные текстуры...")
    
    # Создаем детализированные фоны для разных уровней
    bg_level1 = create_detailed_background_level1()
    bg_level2 = create_detailed_background_level2()  
    bg_level3 = create_detailed_background_level3()
    
    # Создаем детализированных персонажей
    dark_prince_img = create_detailed_dark_prince((80, 100))
    skeleton_img = create_detailed_skeleton((60, 80))
    demon_img = create_detailed_demon((70, 90))
    ghost_img = create_detailed_ghost((65, 85))
    dragon_img = create_detailed_dragon((200, 140))

# Загрузка предметов и курсора (остаются без изменений)
try:
    health_potion_img = load_image("items/health_potion.png", (40, 40))
    sword_img = load_image("items/sword.png", (50, 50))
    cursor_img = load_image("ui/cursor.png", (25, 25))
except:
    health_potion_img = create_potion_texture()
    sword_img = create_sword_texture()
    cursor_img = create_cursor_texture()

# Класс анимации атаки (без изменений)
class AttackEffect:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.radius = 20
        self.max_radius = 50
        self.lifetime = 15
        self.current_life = 0
    
    def update(self):
        self.current_life += 1
        self.radius = self.max_radius * (1 - self.current_life / self.lifetime)
        return self.current_life < self.lifetime
    
    def draw(self, screen):
        alpha = 200 * (1 - self.current_life / self.lifetime)
        surf = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 200, 50, alpha), (self.radius, self.radius), self.radius)
        screen.blit(surf, (self.x - self.radius, self.y - self.radius))

# Класс игрока (без изменений)
class Player:
    def __init__(self):
        self.health = 100
        self.max_health = 100
        self.damage = 25
        self.x = 100
        self.y = SCREEN_HEIGHT - 200
        self.speed = 5
        self.rect = pygame.Rect(self.x - 40, self.y - 50, 80, 100)
        self.attack_cooldown = 0
        self.score = 0
        self.health_potions = 0
        self.direction = "right"
        self.level = 1
        self.enemies_killed = 0
        self.attack_effects = []
        
        # Физика платформера
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_power = -16
        self.on_ground = False
        self.max_fall_speed = 15
    
    def move(self, dx, dy):
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
            
        self.velocity_x = dx * self.speed
        
        if dy < 0 and self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False
    
    def update_physics(self, platforms):
        if not self.on_ground:
            self.velocity_y += self.gravity
            if self.velocity_y > self.max_fall_speed:
                self.velocity_y = self.max_fall_speed
        
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        if self.x < 40:
            self.x = 40
        elif self.x > SCREEN_WIDTH - 40:
            self.x = SCREEN_WIDTH - 40
            
        self.rect.center = (self.x, self.y)
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 15:
                    self.y = platform.rect.top - 50
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0 and self.rect.top >= platform.rect.bottom - 15:
                    self.y = platform.rect.bottom + 50
                    self.velocity_y = 0
                elif self.velocity_x > 0 and self.rect.right <= platform.rect.left + 15:
                    self.x = platform.rect.left - 40
                    self.velocity_x = 0
                elif self.velocity_x < 0 and self.rect.left >= platform.rect.right - 15:
                    self.x = platform.rect.right + 40
                    self.velocity_x = 0
        
        self.rect.center = (self.x, self.y)
    
    def attack(self, mouse_pos):
        if self.attack_cooldown == 0:
            self.attack_cooldown = 15
            
            # Создаем эффект атаки
            attack_x = self.x
            attack_y = self.y - 20
            if self.direction == "right":
                attack_x += 45
            else:
                attack_x -= 45
                
            self.attack_effects.append(AttackEffect(attack_x, attack_y, self.direction))
            
            # Проверяем попадание по врагам
            attack_rect = pygame.Rect(attack_x - 30, attack_y - 30, 60, 60)
            damage = self.damage + random.randint(-5, 5)
            return damage, attack_rect
        return 0, None
    
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Обновляем эффекты атаки
        for effect in self.attack_effects[:]:
            if not effect.update():
                self.attack_effects.remove(effect)
    
    def draw(self, screen):  # Исправлено: правильный отступ
        # Рисуем игрока
        if self.direction == "right":
            screen.blit(dark_prince_img, (self.x - 40, self.y - 50))
        else:
            # Отражаем изображение для левого направления
            flipped_img = pygame.transform.flip(dark_prince_img, True, False)
            screen.blit(flipped_img, (self.x - 40, self.y - 50))
        
        # Рисуем эффекты атаки
        for effect in self.attack_effects:
            effect.draw(screen)
        
        # Рисуем индикатор здоровья
        health_width = 100
        health_height = 10
        health_x = self.x - health_width // 2
        health_y = self.y - 70
        
        # Фон индикатора здоровья
        pygame.draw.rect(screen, DARK_RED, (health_x, health_y, health_width, health_height))
        # Текущее здоровье
        health_percent = self.health / self.max_health
        pygame.draw.rect(screen, BLOOD_RED, (health_x, health_y, health_width * health_percent, health_height))
        # Рамка
        pygame.draw.rect(screen, BONE_WHITE, (health_x, health_y, health_width, health_height), 1)

# Класс врага (нужно дописать)
class Enemy:
    def __init__(self, enemy_type, x, y, level):
        self.type = enemy_type
        self.x = x
        self.y = y
        self.level = level
        
        # Устанавливаем характеристики в зависимости от типа врага и уровня
        if enemy_type == "skeleton":
            self.health = 30 + level * 10
            self.max_health = 30 + level * 10
            self.damage = 10 + level * 3
            self.speed = 2 + level * 0.5
            self.rect = pygame.Rect(x - 30, y - 40, 60, 80)
            self.image = skeleton_img
        elif enemy_type == "demon":
            self.health = 50 + level * 15
            self.max_health = 50 + level * 15
            self.damage = 15 + level * 4
            self.speed = 1.5 + level * 0.4
            self.rect = pygame.Rect(x - 35, y - 45, 70, 90)
            self.image = demon_img
        elif enemy_type == "ghost":
            self.health = 20 + level * 8
            self.max_health = 20 + level * 8
            self.damage = 8 + level * 2
            self.speed = 3 + level * 0.6
            self.rect = pygame.Rect(x - 32, y - 42, 65, 85)
            self.image = ghost_img
        elif enemy_type == "dragon":
            self.health = 200 + level * 50
            self.max_health = 200 + level * 50
            self.damage = 30 + level * 10
            self.speed = 1 + level * 0.2
            self.rect = pygame.Rect(x - 100, y - 70, 200, 140)
            self.image = dragon_img
        
        self.direction = 1  # 1 для движения вправо, -1 для движения влево
        self.attack_cooldown = 0
        self.velocity_y = 0
        self.on_ground = False
    
    def move_towards_player(self, player_x, platforms):
        # Простое движение к игроку
        if self.x < player_x:
            self.direction = 1
            self.x += self.speed
        else:
            self.direction = -1
            self.x -= self.speed
        
        # Простая гравитация для врагов
        if not self.on_ground:
            self.velocity_y += 0.8
            if self.velocity_y > 15:
                self.velocity_y = 15
        
        self.y += self.velocity_y
        self.rect.center = (self.x, self.y)
        self.on_ground = False
        
        # Проверка столкновений с платформами
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 15:
                    self.y = platform.rect.top - (self.rect.height // 2)
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0 and self.rect.top >= platform.rect.bottom - 15:
                    self.y = platform.rect.bottom + (self.rect.height // 2)
                    self.velocity_y = 0
        
        self.rect.center = (self.x, self.y)
    
    def attack(self):
        if self.attack_cooldown == 0:
            self.attack_cooldown = 30
            return self.damage + random.randint(-3, 3)
        return 0
    
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def draw(self, screen):
        # Рисуем врага
        if self.direction == 1:
            screen.blit(self.image, (self.x - self.rect.width//2, self.y - self.rect.height//2))
        else:
            flipped_img = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_img, (self.x - self.rect.width//2, self.y - self.rect.height//2))
        
        # Индикатор здоровья врага
        health_width = 60
        health_height = 5
        health_x = self.x - health_width // 2
        health_y = self.y - self.rect.height // 2 - 10
        
        # Фон индикатора здоровья
        pygame.draw.rect(screen, DARK_RED, (health_x, health_y, health_width, health_height))
        # Текущее здоровье
        health_percent = self.health / self.max_health
        pygame.draw.rect(screen, BLOOD_RED, (health_x, health_y, health_width * health_percent, health_height))

# Класс платформы
class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
    
    def draw(self, screen):
        pygame.draw.rect(screen, DARK_GRAY, self.rect)
        pygame.draw.rect(screen, ASH_GRAY, self.rect, 2)

# Класс предмета
class Item:
    def __init__(self, item_type, x, y):
        self.type = item_type
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x - 20, y - 20, 40, 40)
        
        if item_type == "health_potion":
            self.image = health_potion_img
        elif item_type == "sword":
            self.image = sword_img
    
    def draw(self, screen):
        screen.blit(self.image, (self.x - 20, self.y - 20))

# Класс игры
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.platforms = []
        self.items = []
        self.level = 1
        self.game_state = "menu"  # menu, playing, game_over, level_complete
        self.spawn_timer = 0
        self.level_timer = 0
        self.level_duration = 1800  # 30 секунд на уровень (60 FPS * 30)
        self.generate_level()
    
    def generate_level(self):
        self.platforms = []
        self.items = []
        
        # Создаем базовые платформы
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))  # Земля
        
        if self.level == 1:
            # Платформы для уровня 1
            self.platforms.append(Platform(200, SCREEN_HEIGHT - 150, 200, 20))
            self.platforms.append(Platform(500, SCREEN_HEIGHT - 200, 150, 20))
            self.platforms.append(Platform(300, SCREEN_HEIGHT - 300, 200, 20))
        elif self.level == 2:
            # Платформы для уровня 2
            self.platforms.append(Platform(100, SCREEN_HEIGHT - 150, 150, 20))
            self.platforms.append(Platform(400, SCREEN_HEIGHT - 200, 200, 20))
            self.platforms.append(Platform(200, SCREEN_HEIGHT - 300, 100, 20))
            self.platforms.append(Platform(500, SCREEN_HEIGHT - 350, 150, 20))
        elif self.level == 3:
            # Платформы для уровня 3
            self.platforms.append(Platform(150, SCREEN_HEIGHT - 150, 100, 20))
            self.platforms.append(Platform(350, SCREEN_HEIGHT - 200, 120, 20))
            self.platforms.append(Platform(200, SCREEN_HEIGHT - 300, 150, 20))
            self.platforms.append(Platform(450, SCREEN_HEIGHT - 350, 100, 20))
            self.platforms.append(Platform(300, SCREEN_HEIGHT - 450, 200, 20))
        
        # Создаем несколько предметов
        for i in range(3):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            item_type = random.choice(["health_potion", "sword"])
            self.items.append(Item(item_type, x, y))
    
    def spawn_enemy(self):
        if len(self.enemies) < 5 + self.level:  # Максимум врагов на уровне
            x = random.choice([-50, SCREEN_WIDTH + 50])
            y = SCREEN_HEIGHT - 100
            
            # Выбираем тип врага в зависимости от уровня
            if self.level == 1:
                enemy_type = random.choice(["skeleton", "skeleton", "ghost"])
            elif self.level == 2:
                enemy_type = random.choice(["skeleton", "demon", "ghost"])
            else:
                enemy_type = random.choice(["skeleton", "demon", "ghost", "dragon"])
            
            self.enemies.append(Enemy(enemy_type, x, y, self.level))
    
    def check_collisions(self):
        # Проверка столкновений игрока с предметами
        for item in self.items[:]:
            if self.player.rect.colliderect(item.rect):
                if item.type == "health_potion":
                    self.player.health = min(self.player.max_health, self.player.health + 30)
                    self.player.health_potions += 1
                elif item.type == "sword":
                    self.player.damage += 5
                
                self.items.remove(item)
        
        # Проверка атак игрока
        for enemy in self.enemies[:]:
            for attack_effect in self.player.attack_effects:
                attack_rect = pygame.Rect(
                    attack_effect.x - attack_effect.radius,
                    attack_effect.y - attack_effect.radius,
                    attack_effect.radius * 2,
                    attack_effect.radius * 2
                )
                
                if enemy.rect.colliderect(attack_rect):
                    enemy.health -= self.player.damage
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.player.score += 10 * self.level
                        self.player.enemies_killed += 1
                    break
        
        # Проверка атак врагов
        for enemy in self.enemies:
            if enemy.rect.colliderect(self.player.rect) and enemy.attack_cooldown == 0:
                damage = enemy.attack()
                self.player.health -= damage
    
    def update(self):
        if self.game_state == "playing":
            # Обновление игрока
            self.player.update()
            self.player.update_physics(self.platforms)
            
            # Обновление врагов
            for enemy in self.enemies:
                enemy.update()
                enemy.move_towards_player(self.player.x, self.platforms)
            
            # Спавн врагов
            self.spawn_timer += 1
            if self.spawn_timer >= 120 - self.level * 10:  # Чаще спавним на высоких уровнях
                self.spawn_enemy()
                self.spawn_timer = 0
            
            # Проверка столкновений
            self.check_collisions()
            
            # Таймер уровня
            self.level_timer += 1
            if self.level_timer >= self.level_duration:
                self.level_complete()
            
            # Проверка смерти игрока
            if self.player.health <= 0:
                self.game_state = "game_over"
            
            # Проверка завершения уровня (убийство босса)
            if self.level == 3:
                dragon_exists = any(enemy.type == "dragon" for enemy in self.enemies)
                if not dragon_exists and self.level_timer > 300:  # Даем время до появления дракона
                    self.level_complete()
    
    def level_complete(self):
        if self.level < 3:
            self.level += 1
            self.player.level = self.level
            self.generate_level()
            self.enemies = []
            self.level_timer = 0
            self.game_state = "level_complete"
        else:
            self.game_state = "victory"
    
    def draw(self, screen):
        # Рисуем фон в зависимости от уровня
        if self.level == 1:
            screen.blit(bg_level1, (0, 0))
        elif self.level == 2:
            screen.blit(bg_level2, (0, 0))
        else:
            screen.blit(bg_level3, (0, 0))
        
        # Рисуем платформы
        for platform in self.platforms:
            platform.draw(screen)
        
        # Рисуем предметы
        for item in self.items:
            item.draw(screen)
        
        # Рисуем врагов
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Рисуем игрока
        self.player.draw(screen)
        
        # Рисуем интерфейс
        self.draw_ui(screen)
        
        # Рисуем курсор
        mouse_pos = pygame.mouse.get_pos()
        screen.blit(cursor_img, (mouse_pos[0] - 12, mouse_pos[1] - 12))
    
    def draw_ui(self, screen):
        # Информация о здоровье
        health_text = main_font.render(f"Здоровье: {self.player.health}/{self.player.max_health}", True, BONE_WHITE)
        screen.blit(health_text, (20, 20))
        
        # Счет
        score_text = main_font.render(f"Счет: {self.player.score}", True, BONE_WHITE)
        screen.blit(score_text, (20, 60))
        
        # Уровень
        level_text = main_font.render(f"Уровень: {self.level}", True, BONE_WHITE)
        screen.blit(level_text, (20, 100))
        
        # Зелья здоровья
        potion_text = main_font.render(f"Зелья: {self.player.health_potions}", True, BONE_WHITE)
        screen.blit(potion_text, (20, 140))
        
        # Таймер уровня
        time_left = (self.level_duration - self.level_timer) // 60
        timer_text = main_font.render(f"Время: {time_left}с", True, BONE_WHITE)
        screen.blit(timer_text, (SCREEN_WIDTH - 200, 20))
        
        # Убито врагов
        kills_text = main_font.render(f"Убито: {self.player.enemies_killed}", True, BONE_WHITE)
        screen.blit(kills_text, (SCREEN_WIDTH - 200, 60))
        
        # Экран меню
        if self.game_state == "menu":
            self.draw_menu(screen)
        elif self.game_state == "game_over":
            self.draw_game_over(screen)
        elif self.game_state == "level_complete":
            self.draw_level_complete(screen)
        elif self.game_state == "victory":
            self.draw_victory(screen)
    
    def draw_menu(self, screen):
        # Затемнение экрана
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        # Заголовок
        title_text = title_font.render("Темный Принц: Восхождение Тьмы", True, BLOOD_RED)
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//4))
        
        # Кнопка начала игры
        start_button = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2, 300, 60)
        pygame.draw.rect(screen, DARK_RED, start_button)
        pygame.draw.rect(screen, BLOOD_RED, start_button, 3)
        
        start_text = main_font.render("Начать игру", True, BONE_WHITE)
        screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2 + 15))
        
        # Инструкции
        instructions = [
            "Управление: WASD или стрелки для движения, ПКМ для атаки",
            "Цель: победить всех врагов и пройти 3 уровня",
            "Собирайте зелья для лечения и мечи для увеличения урона"
        ]
        
        for i, instruction in enumerate(instructions):
            instr_text = small_font.render(instruction, True, ASH_GRAY)
            screen.blit(instr_text, (SCREEN_WIDTH//2 - instr_text.get_width()//2, SCREEN_HEIGHT//2 + 100 + i*30))
    
    def draw_game_over(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        game_over_text = title_font.render("ПОРАЖЕНИЕ", True, BLOOD_RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//3))
        
        score_text = main_font.render(f"Ваш счет: {self.player.score}", True, BONE_WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
        
        restart_text = main_font.render("Нажмите R для перезапуска", True, ASH_GRAY)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 60))
    
    def draw_level_complete(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        complete_text = title_font.render(f"Уровень {self.level-1} пройден!", True, DARK_GOLD)
        screen.blit(complete_text, (SCREEN_WIDTH//2 - complete_text.get_width()//2, SCREEN_HEIGHT//3))
        
        continue_text = main_font.render("Нажмите ПРОБЕЛ для продолжения", True, BONE_WHITE)
        screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2))
    
    def draw_victory(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        victory_text = title_font.render("ПОБЕДА!", True, DARK_GOLD)
        screen.blit(victory_text, (SCREEN_WIDTH//2 - victory_text.get_width()//2, SCREEN_HEIGHT//3))
        
        score_text = main_font.render(f"Финальный счет: {self.player.score}", True, BONE_WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
        
        kills_text = main_font.render(f"Врагов убито: {self.player.enemies_killed}", True, BONE_WHITE)
        screen.blit(kills_text, (SCREEN_WIDTH//2 - kills_text.get_width()//2, SCREEN_HEIGHT//2 + 40))
        
        restart_text = main_font.render("Нажмите R для новой игры", True, ASH_GRAY)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 100))

# Основной игровой цикл
def main():
    game = Game()
    clock = pygame.time.Clock()
    
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if event.key == pygame.K_r and (game.game_state == "game_over" or game.game_state == "victory"):
                    game = Game()  # Перезапуск игры
                
                if event.key == pygame.K_SPACE and game.game_state == "level_complete":
                    game.game_state = "playing"
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    if game.game_state == "menu":
                        mouse_pos = pygame.mouse.get_pos()
                        start_button = pygame.Rect(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2, 300, 60)
                        if start_button.collidepoint(mouse_pos):
                            game.game_state = "playing"
                    
                    elif game.game_state == "playing":
                        # Использование зелья здоровья
                        if game.player.health_potions > 0 and game.player.health < game.player.max_health:
                            game.player.health = min(game.player.max_health, game.player.health + 30)
                            game.player.health_potions -= 1
                
                if event.button == 3:  # ПКМ - атака
                    if game.game_state == "playing":
                        game.player.attack(pygame.mouse.get_pos())
        
        # Получение состояния клавиш для движения
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if game.game_state == "playing":
            # Движение влево/вправо
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx = -1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx = 1
            
            # Прыжок
            if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                dy = -1
            
            game.player.move(dx, dy)
        
        # Обновление игры
        game.update()
        
        # Отрисовка
        game.draw(screen)
        pygame.display.flip()
        
        # Ограничение FPS
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 
    

