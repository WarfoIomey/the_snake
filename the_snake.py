from random import randrange
from typing import Optional

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

# Центр поля.
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)

# Цвет яблока.
APPLE_COLOR = (255, 0, 0)

# Цвет змейки.
SNAKE_COLOR = (0, 255, 0)

# Цвет бомбы.
BAD_FOOD_COLOR = (255, 0, 255)

# Цвет камня.
STONE_COLOR = (169, 169, 169)

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
    """Родительский класс для создания яблок и змей.

    Атрибуты:
        position (tuple): Позиция объекта на игровом поле.
        body_color: (tuple): Цвет объекта.
    """

    position: tuple = CENTER
    body_color: tuple = BOARD_BACKGROUND_COLOR

    def __init__(
            self,
            position=CENTER,
            body_color=BOARD_BACKGROUND_COLOR,
    ) -> None:
        self.position = position
        self.body_color = body_color

    def draw(self) -> None:
        """Метод для отрисовки объектов, предназначен
        для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Дочерний класс GameObject, предназначен для создания еды для змеи.

    Атрибуты:
        body_color (tuple): Цвет еды.
        position (tuple): Расположение еды в случайном месте.
    """

    body_color = APPLE_COLOR
    position = (
        randrange(0, SCREEN_WIDTH, 20),
        randrange(0, SCREEN_HEIGHT, 20),
    )

    def __init__(self, body_color=APPLE_COLOR) -> None:
        self.body_color = body_color
        self.position = self.randomize_position

    def draw(self) -> None:
        """Метод для отрисовки еды на игровом поле.

        Аргументы:
            rect: Объект с расположением и размерами еды.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    @property
    def randomize_position(self) -> tuple:
        """Декоратор для генерации случайного расположения еды.

        Возвращает:
            tuple: Расположение по x и y на игровом поле.
        """
        return (
            randrange(0, SCREEN_WIDTH, 20),
            randrange(0, SCREEN_HEIGHT, 20),
        )


class Stone(Apple):
    """Дочерний класс Apple, предназначен для создания препятствия для змеи.

    Атрибуты:
        body_color (tuple): Цвет камня.
        list_stone (list): Список камней с их расположением.
    """

    body_color: tuple = STONE_COLOR
    count: int = 3
    list_stones: list = []

    def __init__(self, count=3):
        self.count = count
        self.randomize_position_stone()

    def draw(self) -> None:
        """Метод для отрисовки камня на игровом поле.

        Аргументы:
            rect: Объект с расположением и размерами камня.
        """
        for stone in self.list_stones:
            rect = pygame.Rect(stone, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position_stone(self) -> None:
        """Метод для генерации случайного расположения камня."""
        for _ in range(1, self.count + 1):
            self.list_stones.append(
                (
                    randrange(0, SCREEN_WIDTH, 20),
                    randrange(0, SCREEN_HEIGHT, 20),
                )
            )


class Snake(GameObject):
    """Дочерний класс GameObject, предназначен для создания змеи.

    Атрибуты:
        length (int): Длинна змеи по умолчанию 1.
        position (list): Тела змеи разделена на сегменты в ввиде кортежа.
        last (tuple): Старое расположение последнего сегмента змеи.
        direction (tuple): Текущее направления движение змеи.
        next_direction (None, tuple): Следующее направление движения змеи.
        body_color (tuple): Цвет змеи.
    """

    length: int = 1
    positions = [CENTER]
    last: tuple = CENTER
    direction: tuple = RIGHT
    next_direction: Optional[tuple] = None
    body_color = SNAKE_COLOR

    def __init__(self, position=CENTER, body_color=SNAKE_COLOR) -> None:
        super().__init__(position, body_color)

    def update_direction(self) -> None:
        """Обновление движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Метод передвижения змеи по сетке игрового поле,
        с переходом из одной границы поля в другю.
        """
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
        """Отрисовка змеи."""
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
        """Декоратор для получения текущего расположения головы змеи."""
        return self.positions[0]

    def added_body_snake(self) -> None:
        """Метод события при котором змеи съедает яблока,
        в зависимости с какой стороны яблока было съедено
        к телу добавляется сегмент.
        """
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
        """Метод для перезапуска игры,
        прошлое тело змеи затирается игровым полем
        и змея начинает движения с центра и 1 сегментом.
        """
        for cell_body in self.positions:
            last_rect = pygame.Rect(cell_body, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        self.positions = [CENTER]
        self.length = 1


def handle_keys(game_object) -> None:
    """Функция для обработки нажатия клавиатуры"""
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
    """Функция игры"""
    pygame.init()
    snake = Snake()
    apple = Apple()
    bad_food = Apple(body_color=BAD_FOOD_COLOR)
    stone = Stone(count=3)
    stone.draw()
    snake.draw()
    apple.draw()
    bad_food.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        for position_stone in stone.list_stones:
            if position_stone == snake.get_head_position:
                snake.reset()
                stone.draw()
        if bad_food.position == snake.get_head_position:
            snake.length -= 1
            if snake.length == 0:
                snake.reset()
                bad_food.position = bad_food.randomize_position
            else:
                bad_food.position = bad_food.randomize_position
                last_rect = pygame.Rect(
                    snake.positions[-1],
                    (GRID_SIZE, GRID_SIZE),
                )
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
                snake.positions.pop()
        if apple.position == snake.get_head_position:
            snake.length += 1
            apple.position = apple.randomize_position
            snake.added_body_snake()
        for position_body_snake in snake.positions[1:]:
            if snake.positions[0] == position_body_snake:
                snake.reset()
        snake.draw()
        apple.draw()
        bad_food.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
