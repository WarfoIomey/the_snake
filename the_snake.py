from random import choice, randrange
from typing import Union, Optional

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Центр поля
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """
    Родительский класс для создания яблок и змеи
    Атрибуты:
        1) position: tuple
             позиция объекта на игровом поле
        2) body_color: tuple
             цвет объекта
    Методы:
        1) draw -> None
            метод для переопределения в дочерних классах, для оторисовки
    """

    position: tuple = CENTER
    body_color: tuple = BOARD_BACKGROUND_COLOR

    def __init__(self, position, body_color) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        # Отрисовка объектов
        pass


class Apple(GameObject):
    '''
    Дочерний класс GameObject
    Атрибуты:
        1) body_color: tuple
            цвет яблока
        2) position: tuple
            яблоко появляется в случайном месте на игровом поле
    Методы:
        1) __init__ -> None
            задает цвет яблоку
            вызвав свойство randomize_position задает случайное расположение
        2) draw -> None
            рисует яблоко на поле квадротом 20х20
    Декоратор:
        1) randomize_position -> tuple
            случайно генерирует расположение яблока
    '''
    body_color = APPLE_COLOR
    position = (
        randrange(0, SCREEN_WIDTH, 20),
        randrange(0, SCREEN_HEIGHT, 20),
    )

    def __init__(self, body_color) -> None:
        self.body_color = body_color
        self.position = self.randomize_position
  
    def draw(self) -> None:
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    @property
    def randomize_position(self) -> tuple:
        return (
            randrange(0, SCREEN_WIDTH, 20),
            randrange(0, SCREEN_HEIGHT, 20),
        )


class Snake(GameObject):
    length: int = 1
    positions = [CENTER]
    last: tuple = CENTER
    direction: tuple = RIGHT
    next_direction: Optional[tuple] = None
    body_color = SNAKE_COLOR

    def __init__(self, position, body_color) -> None:
        super().__init__(position, body_color)

    def update_direction(self) -> None:
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        coordinate_x = self.positions[0][0]
        coordinate_y = self.positions[0][1]
        if coordinate_x + self.direction[0] * GRID_SIZE > SCREEN_WIDTH - 1:
            self.positions.insert(
                0,
                (
                    0,
                    coordinate_y + self.direction[1] * GRID_SIZE,
                )
            )
        elif coordinate_y + self.direction[1] * GRID_SIZE > SCREEN_HEIGHT - 1:
            self.positions.insert(
                0,
                (
                    coordinate_x + self.direction[0] * GRID_SIZE,
                    0,
                )
            )
        elif coordinate_x + self.direction[0] * GRID_SIZE < 0:
            self.positions.insert(
                0,
                (
                    640,
                    coordinate_y + self.direction[1] * GRID_SIZE,
                )
            )
        elif coordinate_y + self.direction[1] * GRID_SIZE < 0:
            self.positions.insert(
                0,
                (
                    coordinate_x + self.direction[0] * GRID_SIZE,
                    480,
                )
            )
        else:
            self.positions.insert(
                0,
                (
                    coordinate_x + self.direction[0] * GRID_SIZE,
                    coordinate_y + self.direction[1] * GRID_SIZE,
                )
            )
        self.last = self.positions[-1]
        self.positions.pop()

    def draw(self) -> None:
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    @property
    def get_head_position(self) -> tuple:
        return self.positions[0]

    def added_body_snake(self) -> None:
        if len(self.positions) != self.length:
            if self.length == 1:
                self.positions.append(
                    (
                        self.positions[-1][0] + GRID_SIZE * self.direction[0],
                        self.positions[-1][1] + GRID_SIZE * self.direction[1],
                    )
                )
            else:
                self.positions.append(
                    (
                        self.positions[-1][0] - GRID_SIZE * self.direction[0],
                        self.positions[-1][1] - GRID_SIZE * self.direction[1],
                    )
                )

    def reset(self) -> None:
        for cell_body in self.positions:
            last_rect = pygame.Rect(cell_body, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.positions = [CENTER]



def handle_keys(game_object) -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    pygame.init()
    snake = Snake(position=CENTER, body_color=SNAKE_COLOR)
    apple = Apple(body_color=APPLE_COLOR)
    snake.draw()
    apple.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if apple.position == snake.get_head_position:
            snake.length += 1
            apple.position = apple.randomize_position
            snake.added_body_snake()
        for position_body_snake in snake.positions[1:]:
            if snake.positions[0] == position_body_snake:
                snake.reset()
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
