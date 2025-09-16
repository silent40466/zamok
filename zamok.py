import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Установка полноэкранного режима
screen_info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Темный Принц против сил зла")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)

# Загрузка текстур (заглушки - в реальной игре замените на настоящие текстуры)
def create_texture(color, size):
    texture = pygame.Surface(size)
    texture.fill(color)
    for i in range(100):
        x, y = random.randint(0, size[0]-1), random.randint(0, size[1]-1)
        pygame.draw.circle(texture, (min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255)), (x, y), 1)
    return texture

# Создание текстур
textures = {
    "castle": create_texture((100, 80, 60), (100, 100)),
    "floor": create_texture((120, 100, 80), (50, 50)),
    "dark_prince": create_texture((60, 60, 100), (40, 60)),
    "skeleton": create_texture((200, 200, 200), (40, 60)),
    "demon": create_texture((200, 50, 50), (50, 70)),
    "ghost": create_texture((200, 200, 250), (40, 60)),
    "dragon": create_texture((255, 100, 50), (120, 80)),
    "health_potion": create_texture((255, 0, 0), (20, 20)),
    "sword": create_texture((200, 200, 220), (30, 50))
}

# Класс игрока
class Player:
    def __init__(self):
        self.health = 100
        self.max_health = 100
        self.damage = 25
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.speed = 5
        self.rect = pygame.Rect(self.x - 20, self.y - 30, 40, 60)
        self.attack_cooldown = 0
        self.score = 0
        self.health_potions = 3
    
    def move(self, dx, dy):
        # Проверка границ экрана
        if 0 < self.x + dx < SCREEN_WIDTH:
            self.x += dx
        if 0 < self.y + dy < SCREEN_HEIGHT:
            self.y += dy
        self.rect.center = (self.x, self.y)
    
    def attack(self):
        if self.attack_cooldown == 0:
            self.attack_cooldown = 20
            return self.damage + random.randint(-5, 5)
        return 0
    
    def update(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def draw(self, screen):
        # Рисуем игрока
        screen.blit(textures["dark_prince"], (self.x - 20, self.y - 30))
        
        # Рисуем здоровье
        pygame.draw.rect(screen, RED, (self.x - 20, self.y - 50, 40, 5))
        pygame.draw.rect(screen, GREEN, (self.x - 20, self.y - 50, 40 * (self.health / self.max_health), 5))
    
    def use_health_potion(self):
        if self.health_potions > 0:
            self.health = min(self.max_health, self.health + 30)
            self.health_potions -= 1
            return True
        return False

# Класс врага
class Enemy:
    def __init__(self, enemy_type, x, y):
        self.type = enemy_type
        self.x = x
        self.y = y
        
        if enemy_type == "skeleton":
            self.health = 30
            self.max_health = 30
            self.damage = 10
            self.speed = 2
            self.rect = pygame.Rect(self.x - 20, self.y - 30, 40, 60)
        elif enemy_type == "demon":
            self.health = 40
            self.max_health = 40
            self.damage = 15
            self.speed = 3
            self.rect = pygame.Rect(self.x - 25, self.y - 35, 50, 70)
        elif enemy_type == "ghost":
            self.health = 25
            self.max_health = 25
            self.damage = 12
            self.speed = 4
            self.rect = pygame.Rect(self.x - 20, self.y - 30, 40, 60)
        elif enemy_type == "dragon":
            self.health = 100
            self.max_health = 100
            self.damage = 20
            self.speed = 1
            self.rect = pygame.Rect(self.x - 60, self.y - 40, 120, 80)
        
        self.attack_cooldown = 0
    
    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        dist = max(1, math.sqrt(dx * dx + dy * dy))
        dx, dy = dx / dist, dy / dist
        
        self.x += dx * self.speed
        self.y += dy * self.speed
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
        if self.type == "skeleton":
            screen.blit(textures["skeleton"], (self.x - 20, self.y - 30))
        elif self.type == "demon":
            screen.blit(textures["demon"], (self.x - 25, self.y - 35))
        elif self.type == "ghost":
            screen.blit(textures["ghost"], (self.x - 20, self.y - 30))
        elif self.type == "dragon":
            screen.blit(textures["dragon"], (self.x - 60, self.y - 40))
        
        # Рисуем здоровье
        health_width = 40
        if self.type == "dragon":
            health_width = 100
        
        pygame.draw.rect(screen, RED, (self.x - health_width//2, self.y - 60, health_width, 5))
        pygame.draw.rect(screen, GREEN, (self.x - health_width//2, self.y - 60, health_width * (self.health / self.max_health), 5))

# Класс предмета
class Item:
    def __init__(self, item_type, x, y):
        self.type = item_type
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x - 10, y - 10, 20, 20)
    
    def draw(self, screen):
        if self.type == "health_potion":
            screen.blit(textures["health_potion"], (self.x - 10, self.y - 10))
        elif self.type == "sword":
            screen.blit(textures["sword"], (self.x - 15, self.y - 25))

# Основная функция игры
def main():
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    small_font = pygame.font.SysFont(None, 24)
    
    player = Player()
    enemies = []
    items = []
    
    # Создаем врагов
    for i in range(5):
        enemies.append(Enemy("skeleton", random.randint(100, SCREEN_WIDTH-100), random.randint(100, SCREEN_HEIGHT-100)))
    
    for i in range(3):
        enemies.append(Enemy("demon", random.randint(100, SCREEN_WIDTH-100), random.randint(100, SCREEN_HEIGHT-100)))
    
    for i in range(3):
        enemies.append(Enemy("ghost", random.randint(100, SCREEN_WIDTH-100), random.randint(100, SCREEN_HEIGHT-100)))
    
    # Добавляем дракона (босса)
    boss = Enemy("dragon", SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4)
    enemies.append(boss)
    
    # Добавляем предметы
    for i in range(5):
        items.append(Item("health_potion", random.randint(50, SCREEN_WIDTH-50), random.randint(50, SCREEN_HEIGHT-50)))
    
    for i in range(2):
        items.append(Item("sword", random.randint(50, SCREEN_WIDTH-50), random.randint(50, SCREEN_HEIGHT-50)))
    
    game_state = "playing"  # "playing", "game_over", "victory"
    
    # Основной игровой цикл
    running = True
    while running:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and game_state != "playing":
                    return main()  # Перезапуск игры
                if event.key == pygame.K_SPACE and game_state == "playing":
                    # Атака
                    for enemy in enemies:
                        if player.rect.colliderect(enemy.rect):
                            damage = player.attack()
                            if damage > 0:
                                enemy.health -= damage
                                if enemy.health <= 0:
                                    player.score += 10
                                    if enemy.type == "dragon":
                                        player.score += 100  # Бонус за дракона
                if event.key == pygame.K_h and game_state == "playing":
                    # Использование зелья здоровья
                    player.use_health_potion()
        
        if game_state == "playing":
            # Движение игрока
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx -= player.speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx += player.speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy -= player.speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy += player.speed
            
            player.move(dx, dy)
            player.update()
            
            # Движение врагов
            for enemy in enemies:
                enemy.move_towards(player.x, player.y)
                enemy.update()
                
                # Проверка столкновения с игроком
                if player.rect.colliderect(enemy.rect):
                    damage = enemy.attack()
                    if damage > 0:
                        player.health -= damage
            
            # Проверка столкновения с предметами
            for item in items[:]:
                if player.rect.colliderect(item.rect):
                    if item.type == "health_potion":
                        player.health_potions += 1
                    elif item.type == "sword":
                        player.damage += 5
                    items.remove(item)
            
            # Удаление мертвых врагов
            for enemy in enemies[:]:
                if enemy.health <= 0:
                    enemies.remove(enemy)
            
            # Проверка условий окончания игры
            if player.health <= 0:
                game_state = "game_over"
            
            if len(enemies) == 0:
                game_state = "victory"
        
        # Отрисовка
        # Рисуем фон замка
        for x in range(0, SCREEN_WIDTH, 100):
            for y in range(0, SCREEN_HEIGHT, 100):
                screen.blit(textures["castle"], (x, y))
        
        # Рисуем пол
        for x in range(0, SCREEN_WIDTH, 50):
            for y in range(0, SCREEN_HEIGHT, 50):
                screen.blit(textures["floor"], (x, y))
        
        # Рисуем предметы
        for item in items:
            item.draw(screen)
        
        # Рисуем врагов
        for enemy in enemies:
            enemy.draw(screen)
        
        # Рисуем игрока
        player.draw(screen)
        
        # Рисуем интерфейс
        pygame.draw.rect(screen, PURPLE, (10, 10, 200, 30))
        pygame.draw.rect(screen, GREEN, (10, 10, 200 * (player.health / player.max_health), 30))
        health_text = font.render(f"Здоровье: {player.health}/{player.max_health}", True, WHITE)
        screen.blit(health_text, (15, 12))
        
        score_text = font.render(f"Счет: {player.score}", True, GOLD)
        screen.blit(score_text, (SCREEN_WIDTH - 200, 10))
        
        potions_text = font.render(f"Зелья: {player.health_potions}", True, RED)
        screen.blit(potions_text, (10, 50))
        
        enemies_text = font.render(f"Врагов: {len(enemies)}", True, BLUE)
        screen.blit(enemies_text, (10, 90))
        
        # Подсказки управления
        controls_text = small_font.render("Управление: WASD/Стрелки - движение, SPACE - атака, H - зелье здоровья", True, WHITE)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT - 30))
        
        # Отображение состояния игры
        if game_state == "game_over":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            game_over_text = font.render("ИГРА ОКОНЧЕНА", True, RED)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            
            restart_text = font.render("Нажмите R для перезапуска", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 20))
        
        elif game_state == "victory":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 50, 0, 180))
            screen.blit(overlay, (0, 0))
            
            victory_text = font.render("ПОБЕДА! Вы очистили замок от зла!", True, GOLD)
            screen.blit(victory_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 50))
            
            score_text = font.render(f"Ваш счет: {player.score}", True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
            
            restart_text = font.render("Нажмите R для перезапуска", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
    