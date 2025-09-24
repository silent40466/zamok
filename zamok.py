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
    # Тело (более детализированное)
    pygame.draw.ellipse(texture, (50, 30, 70), (10, 30, size[0]-20, size[1]-40))
    pygame.draw.ellipse(texture, (70, 50, 90), (12, 32, size[0]-24, size[1]-44))
    
    # Голова
    pygame.draw.circle(texture, (70, 50, 90), (size[0]//2, 20), 16)
    pygame.draw.circle(texture, (90, 70, 110), (size[0]//2, 20), 14)
    
    # Плащ (более детализированный)
    cloak_points = [
        (5, 30), (size[0]-5, 30), 
        (size[0]-5, size[1]-10), (size[0]-25, size[1]-5),
        (25, size[1]-5), (5, size[1]-10)
    ]
    pygame.draw.polygon(texture, (30, 10, 50), cloak_points)
    pygame.draw.polygon(texture, (50, 30, 70), cloak_points, 2)
    
    # Детали плаща
    for i in range(5):
        y_pos = 40 + i * 15
        pygame.draw.line(texture, (20, 5, 40), (10, y_pos), (size[0]-10, y_pos), 1)
    
    # Корона (более детализированная)
    pygame.draw.rect(texture, DARK_GOLD, (size[0]//2-15, 5, 30, 12))
    pygame.draw.rect(texture, (200, 170, 60), (size[0]//2-15, 5, 30, 12), 2)
    
    for i in range(5):
        x_pos = size[0]//2 - 12 + i * 6
        pygame.draw.rect(texture, DARK_GOLD, (x_pos, 0, 4, 12))
        pygame.draw.rect(texture, (200, 170, 60), (x_pos, 0, 4, 12), 1)
    
    # Глаза (свечение)
    pygame.draw.circle(texture, (250, 50, 50), (size[0]//2-8, 18), 6)
    pygame.draw.circle(texture, (250, 50, 50), (size[0]//2+8, 18), 6)
    pygame.draw.circle(texture, (255, 100, 100), (size[0]//2-8, 18), 3)
    pygame.draw.circle(texture, (255, 100, 100), (size[0]//2+8, 18), 3)
    
    # Доспехи
    pygame.draw.rect(texture, (80, 60, 100), (size[0]//2-15, 35, 30, 15))
    pygame.draw.rect(texture, (100, 80, 120), (size[0]//2-15, 35, 30, 15), 2)
    
    # Меч (более детализированный)
    pygame.draw.rect(texture, (220, 220, 240), (size[0]//2-3, 40, 6, 35))
    pygame.draw.rect(texture, (180, 180, 200), (size[0]//2-3, 40, 6, 35), 1)
    
    # Рукоять меча
    pygame.draw.rect(texture, (140, 100, 60), (size[0]//2-7, 40, 14, 8))
    pygame.draw.rect(texture, (160, 120, 80), (size[0]//2-7, 40, 14, 8), 2)
    
    # Навершие меча
    pygame.draw.circle(texture, (180, 150, 50), (size[0]//2, 75), 6)
    pygame.draw.circle(texture, (200, 170, 70), (size[0]//2, 75), 3)
    
    return texture

def create_detailed_skeleton(size):
    texture = pygame.Surface(size, pygame.SRCALPHA)
    # Череп (более детализированный)
    pygame.draw.circle(texture, (210, 210, 210), (size[0]//2, 15), 14)
    pygame.draw.circle(texture, (190, 190, 190), (size[0]//2, 15), 12)
    
    # Глазницы
    pygame.draw.ellipse(texture, (40, 40, 40), (size[0]//2-10, 8, 8, 10))
    pygame.draw.ellipse(texture, (40, 40, 40), (size[0]//2+2, 8, 8, 10))
    
    # Носовая полость
    pygame.draw.polygon(texture, (40, 40, 40), [
        (size[0]//2-3, 18), (size[0]//2+3, 18), (size[0]//2, 22)
    ])
    
    # Тело (позвоночник с деталями)
    pygame.draw.rect(texture, (170, 170, 170), (size[0]//2-5, 25, 10, 30))
    pygame.draw.rect(texture, (150, 150, 150), (size[0]//2-5, 25, 10, 30), 1)
    
    # Ребра (более детализированные)
    for i in range(4):
        y_pos = 30 + i*9
        pygame.draw.ellipse(texture, (160, 160, 160), (size[0]//2-12, y_pos, 24, 8))
        pygame.draw.ellipse(texture, (140, 140, 140), (size[0]//2-12, y_pos, 24, 8), 1)
    
    # Руки (с суставами)
    pygame.draw.line(texture, (170, 170, 170), (size[0]//2, 30), (size[0]//2-18, 45), 5)
    pygame.draw.line(texture, (170, 170, 170), (size[0]//2, 30), (size[0]//2+18, 45), 5)
    
    # Суставы рук
    pygame.draw.circle(texture, (190, 190, 190), (size[0]//2-9, 38), 4)
    pygame.draw.circle(texture, (190, 190, 190), (size[0]//2+9, 38), 4)
    pygame.draw.circle(texture, (190, 190, 190), (size[0]//2-18, 45), 4)
    pygame.draw.circle(texture, (190, 190, 190), (size[0]//2+18, 45), 4)
    
    # Кисти
    pygame.draw.circle(texture, (180, 180, 180), (size[0]//2-23, 50), 5)
    pygame.draw.circle(texture, (180, 180, 180), (size[0]//2+23, 50), 5)
    
    # Ноги (с суставами)
    pygame.draw.line(texture, (170, 170, 170), (size[0]//2, 50), (size[0]//2-12, 70), 5)
    pygame.draw.line(texture, (170, 170, 170), (size[0]//2, 50), (size[0]//2+12, 70), 5)
    
    # Суставы ног
    pygame.draw.circle(texture, (190, 190, 190), (size[0]//2-6, 60), 4)
    pygame.draw.circle(texture, (190, 190, 190), (size[0]//2+6, 60), 4)
    
    # Стопы
    pygame.draw.ellipse(texture, (180, 180, 180), (size[0]//2-15, 68, 10, 5))
    pygame.draw.ellipse(texture, (180, 180, 180), (size[0]//2+5, 68, 10, 5))
    
    # Меч (более детализированный)
    pygame.draw.rect(texture, (160, 160, 170), (size[0]//2-18, 35, 4, 30))
    pygame.draw.rect(texture, (140, 140, 150), (size[0]//2-18, 35, 4, 30), 1)
    
    # Рукоять меча
    pygame.draw.rect(texture, (100, 70, 30), (size[0]//2-20, 35, 8, 10))
    pygame.draw.rect(texture, (120, 90, 50), (size[0]//2-20, 35, 8, 10), 1)
    
    # Трещины на костях
    for i in range(3):
        crack_x = size[0]//2 - 4 + random.randint(-2, 2)
        crack_y = 30 + i * 15
        pygame.draw.line(texture, (100, 100, 100), (crack_x, crack_y), (crack_x, crack_y+5), 1)
    
    return texture

def create_detailed_demon(size):
    texture = pygame.Surface(size, pygame.SRCALPHA)
    # Тело (мускулистое)
    pygame.draw.ellipse(texture, (150, 30, 30), (10, 20, size[0]-20, size[1]-30))
    pygame.draw.ellipse(texture, (170, 50, 50), (12, 22, size[0]-24, size[1]-34))
    
    # Мускулы
    pygame.draw.ellipse(texture, (130, 20, 20), (15, 25, 20, 15))
    pygame.draw.ellipse(texture, (130, 20, 20), (size[0]-35, 25, 20, 15))
    
    # Голова
    pygame.draw.circle(texture, (170, 50, 50), (size[0]//2, 15), 14)
    pygame.draw.circle(texture, (190, 70, 70), (size[0]//2, 15), 12)
    
    # Рога (закрученные)
    horn_points_left = [
        (size[0]//2-8, 5), (size[0]//2-18, 0), (size[0]//2-15, -8), (size[0]//2-5, -3)
    ]
    pygame.draw.polygon(texture, (110, 50, 30), horn_points_left)
    
    horn_points_right = [
        (size[0]//2+8, 5), (size[0]//2+18, 0), (size[0]//2+15, -8), (size[0]//2+5, -3)
    ]
    pygame.draw.polygon(texture, (110, 50, 30), horn_points_right)
    
    # Глаза (горящие)
    pygame.draw.circle(texture, (255, 255, 0), (size[0]//2-6, 13), 5)
    pygame.draw.circle(texture, (255, 255, 0), (size[0]//2+6, 13), 5)
    pygame.draw.circle(texture, (255, 200, 0), (size[0]//2-6, 13), 3)
    pygame.draw.circle(texture, (255, 200, 0), (size[0]//2+6, 13), 3)
    
    # Рот
    pygame.draw.arc(texture, (100, 0, 0), (size[0]//2-8, 18, 16, 10), math.pi, 2*math.pi, 2)
    
    # Крылья (кожаные)
    wing_points_left = [
        (5, 25), (0, 15), (-10, 30), (5, 50), (15, 40)
    ]
    pygame.draw.polygon(texture, (120, 20, 20, 200), wing_points_left)
    
    wing_points_right = [
        (size[0]-5, 25), (size[0], 15), (size[0]+10, 30), (size[0]-5, 50), (size[0]-15, 40)
    ]
    pygame.draw.polygon(texture, (120, 20, 20, 200), wing_points_right)
    
    # Хвост
    tail_points = [
        (size[0]//2, size[1]-20), (size[0]//2+10, size[1]-30),
        (size[0]//2-5, size[1]-35), (size[0]//2, size[1]-25)
    ]
    pygame.draw.polygon(texture, (140, 30, 30), tail_points)
    
    # Ноги
    pygame.draw.ellipse(texture, (140, 30, 30), (20, size[1]-30, 15, 25))
    pygame.draw.ellipse(texture, (140, 30, 30), (size[0]-35, size[1]-30, 15, 25))
    
    # Когти
    for i in range(3):
        pygame.draw.polygon(texture, (80, 80, 90), [
            (25+i*5, size[1]-5), (22+i*5, size[1]-10), (28+i*5, size[1]-10)
        ])
        pygame.draw.polygon(texture, (80, 80, 90), [
            (size[0]-25-i*5, size[1]-5), (size[0]-22-i*5, size[1]-10), (size[0]-28-i*5, size[1]-10)
        ])
    
    # Пламенная аура
    for i in range(8):
        flame_radius = random.randint(3, 8)
        flame_x = random.randint(5, size[0]-5)
        flame_y = random.randint(size[1]-15, size[1]-5)
        alpha = random.randint(100, 200)
        pygame.draw.circle(texture, (255, 100, 0, alpha), (flame_x, flame_y), flame_radius)
    
    return texture

def create_detailed_ghost(size):
    texture = pygame.Surface(size, pygame.SRCALPHA)
    
    # Призрачное тело (более волнистое)
    points = []
    num_points = 15
    
    for i in range(num_points):
        angle = 2 * math.pi * i / (num_points - 1)
        radius_var = random.randint(-4, 4)
        
        if i < num_points // 2:
            radius = 18 + radius_var
            x = size[0]//2 + math.cos(angle) * radius
            y = 25 + math.sin(angle) * radius
        else:
            radius = 28 + radius_var
            x = size[0]//2 + math.cos(angle) * radius
            y = 45 + math.sin(angle) * radius
        
        points.append((x, y))
    
    # Основное тело
    pygame.draw.polygon(texture, (190, 190, 210, 160), points)
    
    # Внутреннее свечение
    inner_points = []
    for point in points:
        inner_points.append((point[0] + random.randint(-2, 2), point[1] + random.randint(-2, 2)))
    
    pygame.draw.polygon(texture, (210, 210, 230, 120), inner_points)
    
    # Глаза (пустые)
    pygame.draw.circle(texture, (80, 80, 120, 200), (size[0]//2-8, 30), 6)
    pygame.draw.circle(texture, (80, 80, 120, 200), (size[0]//2+8, 30), 6)
    
    # Зрачки
    pygame.draw.circle(texture, (40, 40, 80, 220), (size[0]//2-8, 30), 3)
    pygame.draw.circle(texture, (40, 40, 80, 220), (size[0]//2+8, 30), 3)
    
    # Рот (призрачный)
    pygame.draw.arc(texture, (80, 80, 120, 180), (size[0]//2-10, 35, 20, 10), 0, math.pi, 2)
    
    # Руки (более волнистые)
    for i in range(5):
        y_pos = 40 + i * 8
        x_offset = math.sin(i * 0.8) * 5
        pygame.draw.ellipse(texture, (180, 180, 200, 140), 
                          (size[0]//2-25 + x_offset, y_pos, 12, 10))
        pygame.draw.ellipse(texture, (180, 180, 200, 140), 
                          (size[0]//2+13 + x_offset, y_pos, 12, 10))
    
    # Призрачная дымка
    for i in range(10):
        x = random.randint(0, size[0])
        y = random.randint(20, size[1])
        radius = random.randint(2, 5)
        alpha = random.randint(30, 80)
        pygame.draw.circle(texture, (220, 220, 240, alpha), (x, y), radius)
    
    return texture

def create_detailed_dragon(size):
    texture = pygame.Surface(size, pygame.SRCALPHA)
    
    # Тело (чешуйчатое)
    pygame.draw.ellipse(texture, (190, 70, 40), (50, 40, size[0]-100, size[1]-60))
    
    # Чешуя
    for i in range(10):
        for j in range(5):
            scale_x = 60 + i * 12
            scale_y = 50 + j * 15
            scale_size = 10
            pygame.draw.ellipse(texture, (170, 50, 20), (scale_x, scale_y, scale_size, scale_size))
            pygame.draw.ellipse(texture, (210, 90, 60), (scale_x+1, scale_y+1, scale_size-2, scale_size-2))
    
    # Голова
    pygame.draw.circle(texture, (210, 90, 60), (size[0]//2, 30), 22)
    pygame.draw.circle(texture, (230, 110, 80), (size[0]//2, 30), 20)
    
    # Глазы (злые)
    pygame.draw.circle(texture, (255, 255, 0), (size[0]//2-10, 25), 8)
    pygame.draw.circle(texture, (255, 255, 0), (size[0]//2+10, 25), 8)
    pygame.draw.circle(texture, (255, 200, 0), (size[0]//2-10, 25), 5)
    pygame.draw.circle(texture, (255, 200, 0), (size[0]//2+10, 25), 5)
    pygame.draw.circle(texture, (0, 0, 0), (size[0]//2-10, 25), 2)
    pygame.draw.circle(texture, (0, 0, 0), (size[0]//2+10, 25), 2)
    
    # Ноздри
    pygame.draw.circle(texture, (100, 40, 20), (size[0]//2-5, 35), 3)
    pygame.draw.circle(texture, (100, 40, 20), (size[0]//2+5, 35), 3)
    
    # Рога (большие и ветвистые)
    left_horn_points = [
        (size[0]//2-18, 10), (size[0]//2-30, 0), (size[0]//2-25, -15),
        (size[0]//2-15, -10), (size[0]//2-20, 5)
    ]
    pygame.draw.polygon(texture, (140, 80, 40), left_horn_points)
    
    right_horn_points = [
        (size[0]//2+18, 10), (size[0]//2+30, 0), (size[0]//2+25, -15),
        (size[0]//2+15, -10), (size[0]//2+20, 5)
    ]
    pygame.draw.polygon(texture, (140, 80, 40), right_horn_points)
    
    # Шея (мускулистая)
    pygame.draw.ellipse(texture, (180, 60, 35), (size[0]//2-18, 30, 36, 45))
    
    # Крылья (кожаные с прожилками)
    wing_points_left = [
        (60, 50), (10, 20), (-20, 60), (0, 90), (40, 80), (60, 70)
    ]
    pygame.draw.polygon(texture, (170, 60, 35, 180), wing_points_left)
    
    # Прожилки на крыльях
    pygame.draw.line(texture, (150, 50, 25, 200), (20, 50), (10, 70), 2)
    pygame.draw.line(texture, (150, 50, 25, 200), (30, 45), (20, 65), 2)
    pygame.draw.line(texture, (150, 50, 25, 200), (40, 55), (30, 75), 2)
    
    wing_points_right = [
        (size[0]-60, 50), (size[0]-10, 20), (size[0]+20, 60), 
        (size[0], 90), (size[0]-40, 80), (size[0]-60, 70)
    ]
    pygame.draw.polygon(texture, (170, 60, 35, 180), wing_points_right)
    
    # Прожилки на правом крыле
    pygame.draw.line(texture, (150, 50, 25, 200), (size[0]-20, 50), (size[0]-10, 70), 2)
    pygame.draw.line(texture, (150, 50, 25, 200), (size[0]-30, 45), (size[0]-20, 65), 2)
    pygame.draw.line(texture, (150, 50, 25, 200), (size[0]-40, 55), (size[0]-30, 75), 2)
    
    # Хвост (длинный и гибкий)
    tail_points = [
        (size[0]-50, size[1]//2), (size[0]-10, size[1]//2-20), 
        (size[0], size[1]//2+10), (size[0]-40, size[1]//2+15),
        (size[0]-60, size[1]//2-5)
    ]
    pygame.draw.polygon(texture, (180, 70, 35), tail_points)
    
    # Шипы на хвосте
    for i in range(4):
        spike_x = size[0]-50 + i*15
        spike_y = size[1]//2 - 5 + math.sin(i) * 10
        pygame.draw.polygon(texture, (140, 60, 30), [
            (spike_x, spike_y), (spike_x-5, spike_y-8), (spike_x+5, spike_y-8)
        ])
    
    # Ноги (мощные)
    pygame.draw.ellipse(texture, (170, 60, 35), (65, size[1]-50, 20, 40))
    pygame.draw.ellipse(texture, (170, 60, 35), (size[0]-85, size[1]-50, 20, 40))
    
    # Когти
    for i in range(3):
        pygame.draw.polygon(texture, (100, 100, 110), [
            (70+i*5, size[1]-10), (67+i*5, size[1]-15), (73+i*5, size[1]-15)
        ])
        pygame.draw.polygon(texture, (100, 100, 110), [
            (size[0]-70-i*5, size[1]-10), (size[0]-67-i*5, size[1]-15), 
            (size[0]-73-i*5, size[1]-15)
        ])
    
    # Пламя из пасти (более эффектное)
    for i in range(8):
        flame_height = random.randint(10, 25)
        flame_width = random.randint(5, 12)
        flame_x = size[0]//2 - 15 + i*4
        flame_color = (255, 200, 0) if i % 2 == 0 else (255, 100, 0)
        
        flame_points = [
            (flame_x, 50), (flame_x - flame_width//2, 50 + flame_height),
            (flame_x + flame_width//2, 50 + flame_height)
        ]
        pygame.draw.polygon(texture, flame_color, flame_points)
        pygame.draw.polygon(texture, (255, 255, 100), flame_points, 1)
    
    return texture

# Функции для создания фонов разных уровней
def create_detailed_background_level1():
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for y in range(SCREEN_HEIGHT):
        shade = max(10, 50 - y // 20)
        pygame.draw.line(bg, (shade, shade, shade), (0, y), (SCREEN_WIDTH, y))
    
    for x in range(0, SCREEN_WIDTH, 50):
        for y in range(0, SCREEN_HEIGHT, 50):
            stone_color = (random.randint(30, 50), random.randint(25, 45), random.randint(20, 40))
            pygame.draw.rect(bg, stone_color, (x, y, 50, 50), 1)
            if random.random() > 0.7:
                crack_x = x + random.randint(5, 45)
                pygame.draw.line(bg, (20, 20, 20), (crack_x, y+5), (crack_x, y+45), 1)
    
    for i in range(3):
        x = 200 + i * 300
        y = SCREEN_HEIGHT - 150
        pygame.draw.rect(bg, (40, 35, 30), (x, y, 120, 80))
        pygame.draw.rect(bg, (50, 45, 35), (x+10, y+10, 100, 60))
        pygame.draw.polygon(bg, (35, 30, 25), [(x, y), (x+120, y), (x+100, y-20), (x+20, y-20)])
    
    for i in range(10):
        x = random.randint(50, SCREEN_WIDTH-50)
        y = random.randint(SCREEN_HEIGHT-200, SCREEN_HEIGHT-100)
        pygame.draw.rect(bg, (120, 100, 80), (x, y, 5, 15))
        pygame.draw.ellipse(bg, (150, 50, 150, 100), (x-10, y-5, 25, 10))
        for r in range(3, 0, -1):
            alpha = 50 - r * 15
            glow = pygame.Surface((30 + r*10, 20 + r*5), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (150, 50, 150, alpha), (0, 0, 30 + r*10, 20 + r*5))
            bg.blit(glow, (x-15 - r*5, y-10 - r*2))
    
    return bg

def create_detailed_background_level2():
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for y in range(SCREEN_HEIGHT):
        r = min(100, 30 + y // 10)
        g = max(0, 10 - y // 20)
        b = max(0, 5 - y // 30)
        pygame.draw.line(bg, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    lava_y = SCREEN_HEIGHT - 100
    lava_points = []
    for x in range(0, SCREEN_WIDTH, 10):
        y_offset = math.sin(x / 50) * 20
        lava_points.append((x, lava_y + y_offset))
    
    if len(lava_points) > 1:
        pygame.draw.polygon(bg, (150, 50, 0), [(0, SCREEN_HEIGHT)] + lava_points + [(SCREEN_WIDTH, SCREEN_HEIGHT)])
        for i in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(lava_y - 30, SCREEN_HEIGHT)
            size = random.randint(5, 15)
            pygame.draw.circle(bg, (255, 100, 0), (x, y), size)
            pygame.draw.circle(bg, (255, 150, 50), (x, y), size-3)
    
    for i in range(3):
        x = 150 + i * 350
        arch_height = 300
        arch_width = 100
        
        pygame.draw.rect(bg, (60, 50, 40), (x, SCREEN_HEIGHT - arch_height, 20, arch_height))
        pygame.draw.rect(bg, (60, 50, 40), (x + arch_width - 20, SCREEN_HEIGHT - arch_height, 20, arch_height))
        pygame.draw.arc(bg, (60, 50, 40), (x, SCREEN_HEIGHT - arch_height - 50, arch_width, 100), math.pi, 2*math.pi, 20)
        
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
    # Свечение
    for i in range(3):
        radius = 15 - i * 5
        alpha = 50 - i * 15
        glow = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 50, 50, alpha), (radius, radius), radius)
        surf.blit(glow, (20 - radius, 20 - radius))
    return surf

def create_sword_texture():
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    # Клинок
    pygame.draw.polygon(surf, (200, 200, 220), [(10, 5), (40, 5), (40, 15), (10, 15)])
    # Рукоять
    pygame.draw.rect(surf, (120, 80, 40), (5, 10, 10, 30))
    # Навершие
    pygame.draw.circle(surf, (180, 150, 50), (10, 45), 5)
    # Детализация клинка
    pygame.draw.line(surf, (180, 180, 200), (15, 7), (35, 7), 1)
    pygame.draw.line(surf, (180, 180, 200), (15, 13), (35, 13), 1)
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

# Загрузка предметов и курсора
try:
    health_potion_img = load_image("items/health_potion.png", (40, 40))
    sword_img = load_image("items/sword.png", (50, 50))
    cursor_img = load_image("ui/cursor.png", (25, 25))
except:
    health_potion_img = create_potion_texture()
    sword_img = create_sword_texture()
    cursor_img = create_cursor_texture()

# Класс анимации атаки
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

# Класс эффекта выпадения предмета
class DropEffect:
    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type
        self.target_y = y - 20
        self.speed = 3
        self.collected = False
        self.rect = pygame.Rect(x - 20, y - 20, 40, 40)
        
        if item_type == "health_potion":
            self.image = health_potion_img
    
    def update(self):
        if self.y > self.target_y:
            self.y -= self.speed
            self.rect.y = self.y - 20
        return not self.collected
    
    def draw(self, screen):
        screen.blit(self.image, (self.x - 20, self.y - 20))
        
        # Свечение вокруг предмета
        glow_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 50, 50, 50), (30, 30), 30)
        screen.blit(glow_surf, (self.x - 30, self.y - 30))

# Класс игрока
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
        
        support_platform = None
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 15:
                    self.y = platform.rect.top - 50
                    self.velocity_y = 0
                    self.on_ground = True
                    support_platform = platform
                elif self.velocity_y < 0 and self.rect.top >= platform.rect.bottom - 15:
                    self.y = platform.rect.bottom + 50
                    self.velocity_y = 0
                elif self.velocity_x > 0 and self.rect.right <= platform.rect.left + 15:
                    self.x = platform.rect.left - 40
                    self.velocity_x = 0
                elif self.velocity_x < 0 and self.rect.left >= platform.rect.right - 15:
                    self.x = platform.rect.right + 40
                    self.velocity_x = 0
        
        # Если стоим на движущейся платформе — переносим вместе с ней
        if self.on_ground and support_platform is not None and hasattr(support_platform, "last_dx"):
            self.x += support_platform.last_dx
        
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
    
    def draw(self, screen):
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

# Класс врага
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
            self.drop_chance = 0.3  # 30% шанс выпадения зелья
        elif enemy_type == "demon":
            self.health = 50 + level * 15
            self.max_health = 50 + level * 15
            self.damage = 15 + level * 4
            self.speed = 1.5 + level * 0.4
            self.rect = pygame.Rect(x - 35, y - 45, 70, 90)
            self.image = demon_img
            self.drop_chance = 0.5  # 50% шанс выпадения зелья
        elif enemy_type == "ghost":
            self.health = 20 + level * 8
            self.max_health = 20 + level * 8
            self.damage = 8 + level * 2
            self.speed = 3 + level * 0.6
            self.rect = pygame.Rect(x - 32, y - 42, 65, 85)
            self.image = ghost_img
            self.drop_chance = 0.4  # 40% шанс выпадения зелья
        elif enemy_type == "dragon":
            self.health = 200 + level * 50
            self.max_health = 200 + level * 50
            self.damage = 30 + level * 10
            self.speed = 1 + level * 0.2
            self.rect = pygame.Rect(x - 100, y - 70, 200, 140)
            self.image = dragon_img
            self.drop_chance = 1.0  # 100% шанс выпадения зелья
        
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
        support_platform = None
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0 and self.rect.bottom <= platform.rect.top + 15:
                    self.y = platform.rect.top - (self.rect.height // 2)
                    self.velocity_y = 0
                    self.on_ground = True
                    support_platform = platform
                elif self.velocity_y < 0 and self.rect.top >= platform.rect.bottom - 15:
                    self.y = platform.rect.bottom + (self.rect.height // 2)
                    self.velocity_y = 0
        
        # Если стоим на движущейся платформе — переносим вместе с ней
        if self.on_ground and support_platform is not None and hasattr(support_platform, "last_dx"):
            self.x += support_platform.last_dx
        
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
    def __init__(self, x, y, width, height, vx=0, move_range=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (random.randint(30, 50), random.randint(25, 45), random.randint(20, 40))
        # Параметры движения по оси X
        self.vx = vx
        # move_range: (min_x, max_x) абсолютные границы перемещения по X
        self.move_range = move_range
        self.direction = 1
        self.last_dx = 0
    
    def update(self):
        self.last_dx = 0
        if self.vx != 0 and self.move_range is not None:
            new_x = self.rect.x + self.vx * self.direction
            if new_x < self.move_range[0]:
                new_x = self.move_range[0]
                self.direction *= -1
            elif new_x + self.rect.width > self.move_range[1]:
                new_x = self.move_range[1] - self.rect.width
                self.direction *= -1
            self.last_dx = new_x - self.rect.x
            self.rect.x = new_x
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, (self.color[0]+20, self.color[1]+20, self.color[2]+20), self.rect, 2)
        
        # Текстура платформы
        for i in range(0, self.rect.width, 20):
            for j in range(0, self.rect.height, 10):
                if random.random() > 0.7:
                    stone_color = (self.color[0]-10, self.color[1]-10, self.color[2]-10)
                    pygame.draw.rect(screen, stone_color, 
                                   (self.rect.x + i, self.rect.y + j, 15, 5))

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
        
        # Анимация парения
        hover_offset = math.sin(pygame.time.get_ticks() / 200) * 3
        screen.blit(self.image, (self.x - 20, self.y - 20 + hover_offset))

# Класс игры
class Game:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.platforms = []
        self.items = []
        self.drop_effects = []  # Эффекты выпадения предметов
        self.level = 1
        self.game_state = "menu"  # menu, playing, game_over, level_complete
        self.spawn_timer = 0
        self.level_timer = 0
        self.level_duration = 1800  # 30 секунд на уровень (60 FPS * 30)
        self.generate_level()
    
    def generate_level(self):
        self.platforms = []
        self.items = []
        self.drop_effects = []
        
        # Создаем базовые платформы
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))  # Земля
        
        # Больше платформ для каждого уровня
        if self.level == 1:
            # Платформы уровня 1: широкие, на всю ширину экрана
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 150, SCREEN_WIDTH, 22))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 260, SCREEN_WIDTH, 18))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 360, SCREEN_WIDTH, 18))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 460, SCREEN_WIDTH, 16))
            # Горизонтальная движущаяся платформа
            self.platforms.append(Platform(100, SCREEN_HEIGHT - 220, 200, 18, vx=3, move_range=(50, SCREEN_WIDTH - 50)))
            
        elif self.level == 2:
            # Платформы уровня 2: широкие, на всю ширину экрана
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 160, SCREEN_WIDTH, 22))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 240, SCREEN_WIDTH, 18))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 320, SCREEN_WIDTH, 18))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 420, SCREEN_WIDTH, 18))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 520, SCREEN_WIDTH, 16))
            self.platforms.append(Platform(50, SCREEN_HEIGHT - 300, 220, 18, vx=2, move_range=(30, SCREEN_WIDTH - 30)))
            
        elif self.level == 3:
            # Платформы уровня 3: широкие, на всю ширину экрана
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 170, SCREEN_WIDTH, 22))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 260, SCREEN_WIDTH, 18))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 340, SCREEN_WIDTH, 18))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 420, SCREEN_WIDTH, 18))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 500, SCREEN_WIDTH, 18))
            self.platforms.append(Platform(0, SCREEN_HEIGHT - 580, SCREEN_WIDTH, 16))
            self.platforms.append(Platform(150, SCREEN_HEIGHT - 380, 260, 18, vx=2, move_range=(80, SCREEN_WIDTH - 80)))
        
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
        
        # Проверка столкновений с выпавшими предметами
        for drop in self.drop_effects[:]:
            if self.player.rect.colliderect(drop.rect):
                if drop.item_type == "health_potion":
                    self.player.health = min(self.player.max_health, self.player.health + 30)
                    self.player.health_potions += 1
                    drop.collected = True
                    self.drop_effects.remove(drop)
        
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
                        # Шанс выпадения зелья при убийстве врага
                        if random.random() < enemy.drop_chance:
                            self.drop_effects.append(DropEffect(enemy.x, enemy.y, "health_potion"))
                        
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
            
            # Движение платформ (если есть движущиеся)
            for platform in self.platforms:
                if hasattr(platform, "update"):
                    platform.update()
            
            # Обновление врагов
            for enemy in self.enemies:
                enemy.update()
                enemy.move_towards_player(self.player.x, self.platforms)
            
            # Обновление эффектов выпадения
            for drop in self.drop_effects[:]:
                if not drop.update():
                    self.drop_effects.remove(drop)
            
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
        
        # Рисуем эффекты выпадения
        for drop in self.drop_effects:
            drop.draw(screen)
        
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
        
        # Урон
        damage_text = main_font.render(f"Урон: {self.player.damage}", True, BONE_WHITE)
        screen.blit(damage_text, (SCREEN_WIDTH - 200, 100))
        
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
            "ЛКМ - использовать зелье здоровья (если есть)",
            "Цель: победить всех врагов и пройти 3 уровня",
            "Собирайте зелья для лечения и мечи для увеличения урона",
            "Враги выпадают зелья с случайным шансом при смерти"
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
        
        kills_text = main_font.render(f"Врагов убито: {self.player.enemies_killed}", True, BONE_WHITE)
        screen.blit(kills_text, (SCREEN_WIDTH//2 - kills_text.get_width()//2, SCREEN_HEIGHT//2 + 40))
        
        restart_text = main_font.render("Нажмите R для перезапуска", True, ASH_GRAY)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 100))
    
    def draw_level_complete(self, screen):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        complete_text = title_font.render(f"Уровень {self.level-1} пройден!", True, DARK_GOLD)
        screen.blit(complete_text, (SCREEN_WIDTH//2 - complete_text.get_width()//2, SCREEN_HEIGHT//3))
        
        stats_text = main_font.render(f"Врагов убито на уровне: {self.player.enemies_killed}", True, BONE_WHITE)
        screen.blit(stats_text, (SCREEN_WIDTH//2 - stats_text.get_width()//2, SCREEN_HEIGHT//2 - 40))
        
        continue_text = main_font.render("Нажмите ПРОБЕЛ для продолжения", True, BONE_WHITE)
        screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
    
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
        
        level_text = main_font.render(f"Пройдено уровней: 3", True, BONE_WHITE)
        screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, SCREEN_HEIGHT//2 + 80))
        
        restart_text = main_font.render("Нажмите R для новой игры", True, ASH_GRAY)
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 140))

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
       
    


