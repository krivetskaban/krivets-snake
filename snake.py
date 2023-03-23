import pygame
import sys
import random
import os
from pygame import mixer

# Data folder path
data_folder = "data"

snake_head_file = os.path.join(data_folder, "k.png")

eat_sounds_files = [
    os.path.join(data_folder, "eat1.mp3"),
    os.path.join(data_folder, "eat2.mp3"),
    os.path.join(data_folder, "eat3.mp3"),
    os.path.join(data_folder, "eat4.mp3"),
]

dead_sounds_files = [
    os.path.join(data_folder, "dead1.mp3"),
    os.path.join(data_folder, "dead2.mp3"),
    os.path.join(data_folder, "dead3.mp3"),
    os.path.join(data_folder, "dead4.mp3"),
    os.path.join(data_folder, "dead5.mp3"),
]

bgm_file = os.path.join(data_folder, "bgm.mp3")

# Initialize pygame and mixer
pygame.init()
mixer.init()

# Define dimensions and colors
cell_size = 25
cell_number = 27
screen_width = cell_number * cell_size
screen_height = cell_number * cell_size
grid_width = screen_width // cell_size
grid_height = screen_height // cell_size
background_color = (175, 215, 70)
snake_color = (0, 0, 0)
food_color = (255, 50, 50)

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

def check_for_updates(current_version, version_url, download_url):
    try:
        response = requests.get(version_url)
        response.raise_for_status()
        latest_version = json.loads(response.text)["version"]

        if latest_version > current_version:
            print(f"Найдена новая версия: {latest_version}. Загрузка...")
            download_response = requests.get(download_url)
            download_response.raise_for_status()

            with open("new_version.zip", "wb") as f:
                f.write(download_response.content)

            with zipfile.ZipFile("new_version.zip", "r") as zip_ref:
                zip_ref.extractall()

            os.remove("new_version.zip")
            print("Обновление завершено. Перезапустите игру.")
            sys.exit()

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при проверке обновлений: {e}")

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

class Snake:
    def __init__(self):
        self.body = [[5, 5], [6, 5], [7, 5]]
        self.direction = (-1, 0)

    def move(self):
        new_head = [(self.body[0][0] + self.direction[0]) % grid_width, (self.body[0][1] + self.direction[1]) % grid_height]
        self.body.insert(0, new_head)
        self.body.pop()

    def eat_food(self, food):
        if self.body[0] == food.position:
            self.body.append(self.body[-1])
            food.randomize_position()
            return True
        return False

    def check_collision(self):
        if self.body[0] in self.body[1:]:
            return True
        return False

    def draw(self):
        for index, block in enumerate(self.body):
            if index == 0:
                head_image = pygame.image.load(snake_head_file)
                head_image = pygame.transform.scale(head_image, (cell_size, cell_size))
                screen.blit(head_image, (block[0] * cell_size, block[1] * cell_size))
            else:
                pygame.draw.rect(screen, snake_color, pygame.Rect(block[0] * cell_size, block[1] * cell_size, cell_size, cell_size))

class Food:
    def __init__(self):
        self.position = [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]

    def randomize_position(self):
        self.position = [random.randint(0, grid_width - 1), random.randint(0, grid_height - 1)]

    def draw(self):
        pygame.draw.rect(screen, food_color, pygame.Rect(self.position[0] * cell_size, self.position[1] * cell_size, cell_size, cell_size))

snake = Snake()
food = Food()

clock = pygame.time.Clock()

# Create variables for the score and font
score = 0
font = pygame.font.Font(None, 36)

def game_over_screen(score):
    game_over_text = font.render("Игра окончена", True, (255, 0, 0))
    score_text = font.render(f"Счет: {score}", True, (255, 0, 0))

    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 - score_text.get_height() // 2 + 30))

    pygame.display.update()
    pygame.time.delay(2000)

def update_speed(score):
    base_speed = 10
    speed_increase = 1
    max_speed = 20

    speed = base_speed + min(score * speed_increase, max_speed - base_speed)
    return speed

mixer.music.load(bgm_file)
mixer.music.set_volume(0.3)
mixer.music.play(-1)

def play_random_sound(sounds_files):
    random_sound = random.choice(sounds_files)
    sound = mixer.Sound(random_sound)
    sound.play()

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
        draw_text("Пауза", font, (0, 0, 0), screen, screen_width // 2 - 50, screen_height // 2 - 20)
        pygame.display.update()
        clock.tick(5)

def main_menu(score=0):
    menu = True
    main_font = pygame.font.Font(None, 48)
    sub_font = pygame.font.Font(None, 36)
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    settings_menu()
                if event.key == pygame.K_RETURN:
                    menu = False

        screen.fill(background_color)
        draw_text("Нажмите Enter чтобы начать игру", main_font, (0, 0, 0), screen,
                  screen_width // 2 - 240, screen_height // 2 - 60)
        draw_text("Нажми S для настроек игры", sub_font, (0, 0, 0), screen,
                  screen_width // 2 - 150, screen_height // 2)
        draw_text(f"Текущий счет: {score}", sub_font, (0, 0, 0), screen,
                  screen_width // 2 - 95, screen_height // 2 + 60)
        pygame.display.update()
        clock.tick(15)

def settings_menu():
    global sound_muted
    settings = True
    while settings:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    sound_muted = not sound_muted
                    mixer.music.set_volume(0 if sound_muted else 0.3)
                if event.key == pygame.K_ESCAPE:
                    settings = False

        screen.fill(background_color)
        draw_text("Settings", font, (0, 0, 0), screen, 20, screen_height // 2 - 40)
        draw_text("Нажми M для включения/отключения звука", font, (0, 0, 0), screen, 20, screen_height // 2)
        draw_text("Нажми ESC для выхода в главное меню", font, (0, 0, 0), screen, 20, screen_height // 2 + 40)
        pygame.display.update()
        clock.tick(15)

sound_muted = False
main_menu()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake.direction[1] == 0:
                    snake.direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                if snake.direction[1] == 0:
                    snake.direction = (0, 1)
            elif event.key == pygame.K_LEFT:
                if snake.direction[0] == 0:
                    snake.direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                if snake.direction[0] == 0:
                    snake.direction = (1, 0)
            elif event.key == pygame.K_p:
                pause_game()
            elif event.key == pygame.K_ESCAPE:
                main_menu(score)
                snake = Snake()
                food = Food()

    if snake.eat_food(food):
        score += 1
        if not sound_muted:
            play_random_sound(eat_sounds_files)

    snake.move()

    if snake.check_collision():
        game_over_screen(score)
        main_menu()

        # Reset game state
        snake = Snake()
        food = Food()
        score = 0

    screen.fill(background_color)

    snake.draw()
    food.draw()

    score_text = font.render(f"Счет: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    speed = update_speed(score)
    clock.tick(speed)

