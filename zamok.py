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

# Функции для создания текстур
def create_character_texture(color, size, name):
    texture = pygame.Surface(size, pygame.SRCALPHA)
    # Тело
    pygame.draw.ellipse(texture, color, (10, 10, size[0]-20, size[1]-20))
    # Голова
    pygame.draw.circle(texture, color, (size[0]//2, 20), 15)
    # Глаза
    pygame.draw.circle(texture, (255, 255, 255), (size[0]//2-8, 18), 3)
    pygame.draw.circle(texture, (255, 255, 255), (size[0]//2+8, 18), 3)
    # Текст с названием
    font = pygame.font.SysFont(None, 12)
    text = font.render(name, True, (255, 255, 255))
    texture.blit(text, (5, size[1]-20))
    return texture

def create_background(color):
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg.fill(color)
    # Добавляем детали на фон
    for i in range(200):
        x = random.randint(0, SCREEN_WIDTH-1)
        y = random.randint(0, SCREEN_HEIGHT-1)
        radius = random.randint(1, 3)
        pygame.draw.circle(bg, (color[0]+20, color[1]+20, color[2]+20), (x, y), radius)
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

# Загрузка текстур
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
    
    # Загрузка предметов
    health_potion_img = load_image("items/health_potion.png", (40, 40))
    sword_img = load_image("items/sword.png", (50, 50))
    
    # Загрузка курсора
    cursor_img = load_image("ui/cursor.png", (25, 25))
    
except Exception as e:
    print(f"Ошибка загрузки изображений: {e}")
    print("Создаются простые текстуры...")
    
    # Создаем фоны для разных уровней
    bg_level1 = create_background((40, 30, 20))
    bg_level2 = create_background((60, 20, 40))  
    bg_level3 = create_background((80, 20, 20))
    
    # Создаем персонажей
    dark_prince_img = create_character_texture((80, 60, 120), (80, 100), "PRINCE")
    skeleton_img = create_character_texture((150, 150, 150), (60, 80), "SKELETON")
    demon_img = create_character_texture((180, 40, 40), (70, 90), "DEMON")
    ghost_img = create_character_texture((180, 180, 220), (65, 85), "GHOST")
    dragon_img = create_character_texture((220, 80, 40), (200, 140), "DRAGON")
    
    # Создаем предметы
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
        self.health_potions = 0  # Начинаем без зелий
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
    
    def draw(self, screen):
        # Рисуем игрока
        if self.direction == "right":
            screen.blit(dark_prince_img, (self.x - 40, self.y - 50))
        else:
            flipped_img = pygame.transform.flip(dark_prince_img, True, False)
            screen.blit(flipped_img, (self.x - 40, self.y - 50))
        
        # Рисуем эффекты атаки
        for effect in self.attack_effects:
            effect.draw(screen)
        
        # Рисуем здоровье
        pygame.draw.rect(screen, DARK_RED, (self.x - 40, self.y - 60, 80, 8))
        pygame.draw.rect(screen, BLOOD_RED, (self.x - 40, self.y - 60, 80 * (self.health / self.max_health), 8))
    
    def use_health_potion(self):
        if self.health_potions > 0:
            self.health = min(self.max_health, self.health + 40)
            self.health_potions -= 1
            return True
        return False

# Класс врага
class Enemy:
    def __init__(self, enemy_type, x, y):
        self.type = enemy_type
        self.x = x
        self.y = y
        self.direction = "left"
        
        if enemy_type == "skeleton":
            self.health = 30
            self.max_health = 30
            self.damage = 10
            self.speed = 2
            self.rect = pygame.Rect(self.x - 30, self.y - 40, 60, 80)
            self.image = skeleton_img
        elif enemy_type == "demon":
            self.health = 40
            self.max_health = 40
            self.damage = 15
            self.speed = 3
            self.rect = pygame.Rect(self.x - 35, self.y - 45, 70, 90)
            self.image = demon_img
        elif enemy_type == "ghost":
            self.health = 25
            self.max_health = 25
            self.damage = 12
            self.speed = 4
            self.rect = pygame.Rect(self.x - 32, self.y - 42, 65, 85)
            self.image = ghost_img
        elif enemy_type == "dragon":
            self.health = 150
            self.max_health = 150
            self.damage = 25
            self.speed = 1.5
            self.rect = pygame.Rect(self.x - 100, self.y - 70, 200, 140)
            self.image = dragon_img
            self.special_attack_cooldown = 0
        
        self.attack_cooldown = 0
    
    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = max(1, math.sqrt(dx * dx + dy * dy))
        dx, dy = dx / dist, dy / dist
        
        if dx > 0:
            self.direction = "right"
        else:
            self.direction = "left"
            
        self.x += dx * self.speed
        self.y += dy * self.speed
        self.rect.center = (self.x, self.y)
    
    def attack(self):
        if self.attack_cooldown == 0:
            self.attack_cooldown = 30
            damage = self.damage + random.randint(-3, 3)
            
            if self.type == "dragon" and self.special_attack_cooldown == 0:
                self.special_attack_cooldown = 100
                damage = int(damage * 1.5)
            
            return damage
        return 0
    
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        if self.type == "dragon" and self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
    
    def draw(self, screen):
        if self.direction == "right":
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            flipped_img = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_img, (self.rect.x, self.rect.y))
        
        health_width = 70
        if self.type == "dragon":
            health_width = 160
        
        pygame.draw.rect(screen, DARK_RED, (self.x - health_width//2, self.y - 70, health_width, 8))
        pygame.draw.rect(screen, BLOOD_RED, (self.x - health_width//2, self.y - 70, health_width * (self.health / self.max_health), 8))
        
        if self.type == "dragon":
            if self.special_attack_cooldown > 0:
                pygame.draw.rect(screen, DARK_RED, (self.x - health_width//2, self.y - 80, health_width, 6))
            else:
                pygame.draw.rect(screen, DARK_GOLD, (self.x - health_width//2, self.y - 80, health_width, 6))

# Класс платформы
class Platform:
    def __init__(self, x, y, width, height, platform_type="stone"):
        self.rect = pygame.Rect(x, y, width, height)
        self.type = platform_type
        
        # Создаем текстуру платформы
        self.texture = pygame.Surface((width, height), pygame.SRCALPHA)
        
        if platform_type == "stone":
            base_color = (80, 70, 60)
            for i in range(width * height // 50):
                px = random.randint(0, width-1)
                py = random.randint(0, height-1)
                pygame.draw.circle(self.texture, (100, 90, 80, 150), (px, py), random.randint(1, 3))
            pygame.draw.rect(self.texture, base_color, (0, 0, width, height), 3)
    
    def draw(self, screen):
        screen.blit(self.texture, self.rect.topleft)
        # Добавляем тень
        shadow_rect = self.rect.move(4, 4)
        shadow = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 80))
        screen.blit(shadow, shadow_rect.topleft)

# Класс предмета
class Item:
    def __init__(self, item_type, x, y):
        self.type = item_type
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x - 20, y - 20, 40, 40)
        self.float_offset = 0
        self.float_direction = 1
        self.rotation = 0
    
    def update(self):
        # Плавающая анимация
        self.float_offset += 0.1 * self.float_direction
        if abs(self.float_offset) > 4:
            self.float_direction *= -1
        
        # Вращение для меча
        if self.type == "sword":
            self.rotation = (self.rotation + 1) % 360
        
        self.rect.y = self.y - 20 + self.float_offset
    
    def draw(self, screen):
        if self.type == "health_potion":
            screen.blit(health_potion_img, (self.x - 20, self.y - 20 + self.float_offset))
        elif self.type == "sword":
            rotated_sword = pygame.transform.rotate(sword_img, self.rotation)
            screen.blit(rotated_sword, (self.x - rotated_sword.get_width()//2, 
                                       self.y - rotated_sword.get_height()//2 + self.float_offset))

# Класс для управления волнами врагов
class WaveManager:
    def __init__(self):
        self.current_wave = 1
        self.max_waves = 3
        self.wave_complete = False
        self.enemies_spawned = 0
        self.enemies_per_wave = 0
        self.spawn_timer = 0
        self.spawn_delay = 120
        self.wave_started = False
        
    def start_wave(self, wave_number):
        self.current_wave = wave_number
        self.wave_complete = False
        self.enemies_spawned = 0
        self.spawn_timer = 0
        self.wave_started = True
        
        if wave_number == 1:
            self.enemies_per_wave = 3
        elif wave_number == 2:
            self.enemies_per_wave = 4
        elif wave_number == 3:
            self.enemies_per_wave = 1
    
    def update(self):
        if self.wave_started and not self.wave_complete:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay and self.enemies_spawned < self.enemies_per_wave:
                self.spawn_timer = 0
                return True
        return False
    
    def enemy_spawned(self):
        self.enemies_spawned += 1
        if self.enemies_spawned >= self.enemies_per_wave:
            self.wave_started = False
    
    def check_wave_complete(self, enemies):
        return len(enemies) == 0 and not self.wave_started
    
    def next_wave(self):
        if self.current_wave < self.max_waves:
            self.current_wave += 1
            return True
        return False

# Класс для управления уровнями
class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.max_level = 3
        self.level_complete = False
        self.wave_manager = WaveManager()
        self.platforms = []
        self.create_platforms()
    
    def get_background(self):
        """Возвращает фон для текущего уровня"""
        if self.current_level == 1:
            return bg_level1
        elif self.current_level == 2:
            return bg_level2
        elif self.current_level == 3:
            return bg_level3
        return bg_level1
    
    def create_platforms(self):
        """Создает платформы для уровня"""
        self.platforms = []
        # Основная платформа (земля)
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60, "stone"))
        
        if self.current_level == 1:
            self.platforms.append(Platform(200, SCREEN_HEIGHT - 160, 160, 25, "stone"))
            self.platforms.append(Platform(500, SCREEN_HEIGHT - 210, 160, 25, "stone"))
            self.platforms.append(Platform(800, SCREEN_HEIGHT - 160, 160, 25, "stone"))
        elif self.current_level == 2:
            self.platforms.append(Platform(150, SCREEN_HEIGHT - 190, 130, 25, "stone"))
            self.platforms.append(Platform(350, SCREEN_HEIGHT - 260, 130, 25, "stone"))
            self.platforms.append(Platform(550, SCREEN_HEIGHT - 190, 130, 25, "stone"))
            self.platforms.append(Platform(750, SCREEN_HEIGHT - 260, 130, 25, "stone"))
        elif self.current_level == 3:
            self.platforms.append(Platform(200, SCREEN_HEIGHT - 210, 220, 25, "stone"))
            self.platforms.append(Platform(600, SCREEN_HEIGHT - 310, 220, 25, "stone"))
            self.platforms.append(Platform(1000, SCREEN_HEIGHT - 210, 220, 25, "stone"))
    
    def spawn_enemy(self, enemy_type):
        if enemy_type == "skeleton":
            return Enemy("skeleton", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 110)
        elif enemy_type == "demon":
            return Enemy("demon", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 190)
        elif enemy_type == "ghost":
            return Enemy("ghost", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 260)
        elif enemy_type == "dragon":
            return Enemy("dragon", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 210)
        return None
    
    # ... остальные методы класса LevelManager
    
    def spawn_enemy(self, enemy_type):
        if enemy_type == "skeleton":
            return Enemy("skeleton", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 110)
        elif enemy_type == "demon":
            return Enemy("demon", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 190)
        elif enemy_type == "ghost":
            return Enemy("ghost", SCREEN_WIDTH - 100, SCREEN_HEIGHT - 260)
        elif enemy_type == "dragon":
            return Enemy("dragon", SCREEN_WIDTH // 2, SCREEN_HEIGHT - 210)
        return None
    
    def get_level_items(self):
        """Генерирует предметы для уровня, появляющиеся снизу"""
        items = []
        platform = self.platforms[0]  # Основная платформа
        
        if self.current_level == 1:
            # 3 зелья на первом уровне
            for i in range(3):
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = platform.rect.top - 30  # Над платформой
                items.append(Item("health_potion", x, y))
                
        elif self.current_level == 2:
            # 2 зелья и 1 меч на втором уровне
            for i in range(2):
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = platform.rect.top - 30
                items.append(Item("health_potion", x, y))
            
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = platform.rect.top - 30
            items.append(Item("sword", x, y))
                
        elif self.current_level == 3:
            # 3 зелья на третьем уровне
            for i in range(3):
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = platform.rect.top - 30
                items.append(Item("health_potion", x, y))
                
        return items
    
    def check_level_complete(self, enemies):
        return len(enemies) == 0
    
    def next_level(self):
        if self.current_level < self.max_level:
            self.current_level += 1
            self.level_complete = False
            self.create_platforms()  # Пересоздаем платформы для нового уровня
            return True
        return False
    
    def get_level_name(self):
        level_names = {
            1: "Гробница Забвения",
            2: "Врата Ада", 
            3: "Логово Дракона"
        }
        return level_names.get(self.current_level, f"Уровень {self.current_level}")
    
    def get_level_description(self):
        descriptions = {
            1: "Скелеты восстали из могил...",
            2: "Демоны стерегут врата в преисподнюю...",
            3: "Древний дракон пробудился от вечного сна..."
        }
        return descriptions.get(self.current_level, "")

# Функция для отрисовки мрачного интерфейса
def draw_dark_ui(screen, player, level_manager, enemies, game_state):
    # Фон интерфейса
    pygame.draw.rect(screen, (0, 0, 0, 180), (0, 0, SCREEN_WIDTH, 100))
    pygame.draw.rect(screen, (0, 0, 0, 180), (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40))
    
    # Здоровье
    health_bg = pygame.Rect(20, 20, 200, 25)
    health_fill = pygame.Rect(20, 20, 200 * (player.health / player.max_health), 25)
    pygame.draw.rect(screen, DARK_RED, health_bg)
    pygame.draw.rect(screen, BLOOD_RED, health_fill)
    pygame.draw.rect(screen, DARK_GRAY, health_bg, 2)
    
    health_text = main_font.render(f"{player.health}/{player.max_health}", True, BONE_WHITE)
    screen.blit(health_text, (25, 22))
    
    # Зелья
    potion_icon = pygame.transform.scale(health_potion_img, (30, 30))
    screen.blit(potion_icon, (240, 18))
    potions_text = main_font.render(f"×{player.health_potions}", True, BONE_WHITE)
    screen.blit(potions_text, (275, 22))
    
    # Информация об уровне
    level_text = main_font.render(level_manager.get_level_name(), True, DARK_GOLD)
    screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 20))
    
    wave_text = small_font.render(f"Волна: {level_manager.wave_manager.current_wave}/3", True, LIGHT_BLUE)
    screen.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, 60))
    
    # Статистика
    score_text = small_font.render(f"Счет: {player.score}", True, DARK_GOLD)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 20))
    
    enemies_text = small_font.render(f"Врагов: {len(enemies)}", True, LIGHT_BLUE)
    screen.blit(enemies_text, (SCREEN_WIDTH - 150, 50))
    
    kills_text = small_font.render(f"Убито: {player.enemies_killed}", True, BLOOD_RED)
    screen.blit(kills_text, (SCREEN_WIDTH - 150, 80))
    
    # Управление
    if game_state == "playing":
        controls_text = small_font.render("WASD - движение | ЛКМ - атака | H - зелье | ESC - выход", True, ASH_GRAY)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, SCREEN_HEIGHT - 30))

# Функция для начального экрана
def show_start_screen():
    start = True
    
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    start = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # Затемнение фона
        screen.fill(BLACK)
        
        # Заголовок
        title_text = title_font.render("ТЕМНЫЙ ПРИНЦ", True, DARK_GOLD)
        subtitle_text = main_font.render("Восхождение Тьмы", True, BLOOD_RED)
        
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
        screen.blit(subtitle_text, (SCREEN_WIDTH//2 - subtitle_text.get_width()//2, SCREEN_HEIGHT//2 - 30))
        
        # Мигающая подсказка
        if pygame.time.get_ticks() % 1000 < 500:
            start_text = main_font.render("Нажмите ENTER чтобы начать", True, BONE_WHITE)
            screen.blit(start_text, (SCREEN_WIDTH//2 - start_text.get_width()//2, SCREEN_HEIGHT//2 + 100))
        
        # Авторы
        author_text = small_font.render("Darkness Games © 2024", True, ASH_GRAY)
        screen.blit(author_text, (SCREEN_WIDTH - author_text.get_width() - 20, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
        pygame.time.delay(30)

# Основная функция игры
def main():
    show_start_screen()
    
    clock = pygame.time.Clock()
    player = Player()
    level_manager = LevelManager()
    enemies = []
    items = level_manager.get_level_items()
    
    level_manager.wave_manager.start_wave(1)
    game_state = "playing"
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        current_bg = level_manager.get_background()  # Получаем фон для текущего уровня
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and game_state != "playing":
                    return main()
                if event.key == pygame.K_h and game_state == "playing":
                    player.use_health_potion()
                if event.key == pygame.K_RETURN and game_state == "wave_complete":
                    if level_manager.wave_manager.next_wave():
                        level_manager.wave_manager.start_wave(level_manager.wave_manager.current_wave)
                        game_state = "playing"
                    elif level_manager.next_level():
                        # Обновляем предметы для нового уровня
                        items = level_manager.get_level_items()
                        player.health = player.max_health
                        level_manager.wave_manager.start_wave(1)
                        game_state = "playing"
                    else:
                        game_state = "victory"
            
            # Атака левой кнопкой мыши
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_state == "playing":
                damage, attack_rect = player.attack(mouse_pos)
                if damage > 0 and attack_rect:
                    for enemy in enemies[:]:
                        if attack_rect.colliderect(enemy.rect):
                            enemy.health -= damage
                            if enemy.health <= 0:
                                player.score += 10
                                player.enemies_killed += 1
                                if enemy.type == "dragon":
                                    player.score += 100
                                enemies.remove(enemy)
        
        if game_state == "playing":
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx -= 1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy -= 1
            
            player.move(dx, dy)
            player.update_physics(level_manager.platforms)
            player.update()
            
            # Обновляем предметы
            for item in items:
                item.update()
            
            # Спавн врагов
            if level_manager.wave_manager.update():
                wave = level_manager.wave_manager.current_wave
                if wave == 1:
                    enemy = level_manager.spawn_enemy("skeleton")
                elif wave == 2:
                    if level_manager.wave_manager.enemies_spawned < 2:
                        enemy = level_manager.spawn_enemy("demon")
                    else:
                        enemy = level_manager.spawn_enemy("ghost")
                elif wave == 3:
                    enemy = level_manager.spawn_enemy("dragon")
                
                if enemy:
                    enemies.append(enemy)
                    level_manager.wave_manager.enemy_spawned()
            
            # Движение врагов
            for enemy in enemies:
                enemy.move_towards(player.x, player.y)
                enemy.update()
                
                if player.rect.colliderect(enemy.rect):
                    damage = enemy.attack()
                    if damage > 0:
                        player.health -= damage
            
            # Сбор предметов
            for item in items[:]:
                if player.rect.colliderect(item.rect):
                    if item.type == "health_potion":
                        player.health_potions += 1
                        # Восстанавливаем немного здоровья при сборе зелья
                        player.health = min(player.max_health, player.health + 10)
                    elif item.type == "sword":
                        player.damage += 8  # Увеличиваем урон
                    items.remove(item)
            
            # Проверка условий
            if player.health <= 0:
                game_state = "game_over"
            
            if level_manager.wave_manager.check_wave_complete(enemies):
                game_state = "wave_complete"
        
        # Отрисовка
        screen.blit(current_bg, (0, 0))  # Используем фон текущего уровня
        
        for platform in level_manager.platforms:
            platform.draw(screen)
        
        for item in items:
            item.draw(screen)
        
        for enemy in enemies:
            enemy.draw(screen)
        
        player.draw(screen)
        
        # Интерфейс
        draw_dark_ui(screen, player, level_manager, enemies, game_state)
        
        # Курсор мыши
        screen.blit(cursor_img, (mouse_pos[0] - 12, mouse_pos[1] - 12))
        
        # Экран Game Over
        if game_state == "game_over":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            
            game_over_text = title_font.render("ПОРАЖЕНИЕ", True, BLOOD_RED)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
            
            score_text = main_font.render(f"Счет: {player.score}", True, DARK_GOLD)
            screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
            
            kills_text = main_font.render(f"Убито врагов: {player.enemies_killed}", True, LIGHT_BLUE)
            screen.blit(kills_text, (SCREEN_WIDTH//2 - kills_text.get_width()//2, SCREEN_HEIGHT//2 + 50))
            
            restart_text = main_font.render("Нажмите R для перезапуска", True, BONE_WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 120))
            
            exit_text = small_font.render("ESC для выхода", True, ASH_GRAY)
            screen.blit(exit_text, (SCREEN_WIDTH//2 - exit_text.get_width()//2, SCREEN_HEIGHT//2 + 180))
        
        # Экран завершения волны
        elif game_state == "wave_complete":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 50, 0, 150))
            screen.blit(overlay, (0, 0))
            
            wave_text = title_font.render("ВОЛНА ПРОЙДЕНА", True, DARK_GOLD)
            screen.blit(wave_text, (SCREEN_WIDTH//2 - wave_text.get_width()//2, SCREEN_HEIGHT//2 - 100))
            
            # Показываем информацию в зависимости от ситуации
            if level_manager.wave_manager.current_wave < level_manager.wave_manager.max_waves:
                next_text = main_font.render(f"Волна {level_manager.wave_manager.current_wave + 1}", True, BONE_WHITE)
                screen.blit(next_text, (SCREEN_WIDTH//2 - next_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
                
                # Добавляем награду за прохождение волны
                reward_text = main_font.render("+1 зелье здоровья", True, BLOOD_RED)
                screen.blit(reward_text, (SCREEN_WIDTH//2 - reward_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
                
                continue_text = main_font.render("Нажмите ENTER чтобы продолжить", True, LIGHT_BLUE)
                screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + 80))
                
            elif level_manager.current_level < level_manager.max_level:
                level_text = main_font.render(f"Уровень {level_manager.current_level + 1}", True, BONE_WHITE)
                screen.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
                
                # Награда за уровень
                reward_text = main_font.render("+2 зелья здоровья", True, BLOOD_RED)
                screen.blit(reward_text, (SCREEN_WIDTH//2 - reward_text.get_width()//2, SCREEN_HEIGHT//2 + 20))
                
                continue_text = main_font.render("Нажмите ENTER чтобы продолжить", True, LIGHT_BLUE)
                screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + 80))
                
            else:
                victory_text = main_font.render("Все уровни пройдены!", True, DARK_GOLD)
                screen.blit(victory_text, (SCREEN_WIDTH//2 - victory_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
                
                continue_text = main_font.render("Нажмите ENTER для победы", True, LIGHT_BLUE)
                screen.blit(continue_text, (SCREEN_WIDTH//2 - continue_text.get_width()//2, SCREEN_HEIGHT//2 + 80))
        
        # Экран победы
        elif game_state == "victory":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 80, 0, 180))
            screen.blit(overlay, (0, 0))
            
            victory_text = title_font.render("ПОБЕДА!", True, DARK_GOLD)
            screen.blit(victory_text, (SCREEN_WIDTH//2 - victory_text.get_width()//2, SCREEN_HEIGHT//2 - 150))
            
            dragon_text = main_font.render("Дракон повержен!", True, BONE_WHITE)
            screen.blit(dragon_text, (SCREEN_WIDTH//2 - dragon_text.get_width()//2, SCREEN_HEIGHT//2 - 70))
            
            score_text = main_font.render(f"Финальный счет: {player.score}", True, DARK_GOLD)
            screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
            
            kills_text = main_font.render(f"Врагов уничтожено: {player.enemies_killed}", True, LIGHT_BLUE)
            screen.blit(kills_text, (SCREEN_WIDTH//2 - kills_text.get_width()//2, SCREEN_HEIGHT//2 + 60))
            
            restart_text = main_font.render("Нажмите R для новой игры", True, BONE_WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 140))
            
            exit_text = small_font.render("ESC для выхода", True, ASH_GRAY)
            screen.blit(exit_text, (SCREEN_WIDTH//2 - exit_text.get_width()//2, SCREEN_HEIGHT//2 + 200))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
