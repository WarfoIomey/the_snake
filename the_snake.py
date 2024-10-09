from random import randrange
from typing import Optional

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центр по оси х.
CENTER_X = SCREEN_WIDTH // 2
# Центр по оси y.
CENTER_Y = SCREEN_HEIGHT // 2

# Константы расположения кнопок главного меню.
X_BUTTON_MENU = CENTER_X - 100
Y_START_BUTTON = CENTER_Y - 90
Y_SETTING_BUTTON = CENTER_Y + 10
Y_QUIT_BUTTON = CENTER_Y + 110

# Константы текста меню.
DRAW_MENU_X = CENTER_X - 100
DRAW_MENU_Y = CENTER_Y - 190

# Константы расположения кнопок настройках.
X_SAVE_BUTTON = CENTER_X - 100
X_BACK_BUTTON = CENTER_X + 100
Y_BUTTON_SETTINGS = CENTER_Y + 185

# Константы расположения окон ввода.
SNAKE_BOX_X = CENTER_X - 90
SNAKE_BOX_Y = CENTER_Y - 190

APPLE_BOX_X = CENTER_X - 80
APPLE_BOX_Y = CENTER_Y - 90

SPEED_BOX_X = CENTER_X
SPEED_BOX_Y = CENTER_Y + 10

STONE_BOX_X = CENTER_X + 100
STONE_BOX_Y = CENTER_Y + 110

# Константы расположения текста в настройках.
DRAW_X = CENTER_X - 300

DRAW_SNAKE_Y = CENTER_Y - 190

DRAW_SPEED_Y = CENTER_Y + 10

DRAW_APPLE_Y = CENTER_Y - 90

DRAW_STONE_Y = CENTER_Y + 110

# Константы размеров объектов главного меню.
LONG_RECT = 200
HEIGHT_RECT = 50

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Центр поля.
CENTER = (CENTER_X, CENTER_Y)

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

# Цвет окна ввода.
COLOR_INPUT_BOX = '#90ee90'

# Цвет активного окна ввода
COLOR_ACTIVE_BOX = '#a6caf0'

# Размер текста
SIZE_TEXT = 50

# Цвет камня.
STONE_COLOR = (169, 169, 169)

# Длинна змеи со старта игры.
LENGTH_HEAD_SNAKE = 1

# Ширина линии змеи.
WIDTH_LINE_ONE = 1

# Ширина линии кнопок.
WIDTH_LINE_BUTTON = 2

# Минимальная шиирина окна ввода.
MIN_WIDTH_BOX = 50

# Число камней.
STONE_COUNT = 3

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class InputBox():
    """Класс для ввода параметров для изменения скорости змеи,
    цвета змеи, цвета яблок и количество камней.

    Атрибуты:
        color (str): Код цвета активного поля и неактивного.
        text_user (str): Текст который пользователь ввёл.
        is_active (bool): Статус окна ввода.
    """

    def __init__(
        self,
        color: str = COLOR_INPUT_BOX,
        text_user=f'{BOARD_BACKGROUND_COLOR}',
        is_active=False
    ) -> None:
        self.color = color
        self.is_active = is_active
        self.text_user = text_user

    def update_color(self) -> None:
        """Метод для измения цвета окна ввода"""
        self.color = COLOR_ACTIVE_BOX if self.is_active else COLOR_INPUT_BOX


class GameObject():
    """Родительский класс для создания яблок и змей.

    Атрибуты:
        position (tuple): Позиция объекта на игровом поле.
        body_color (tuple): Цвет объекта.
    """

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


class Apple(GameObject):
    """Дочерний класс GameObject, предназначен для создания еды для змеи.

    Атрибуты:
        body_color (tuple): Цвет еды.
        position (tuple): Расположение еды в случайном месте.
        list_apple (list): Список расположений яблок на игровом поле.
        occupied_cells (list): Список всех занятых ячеек на игровом поле.
    """

    def __init__(
            self,
            body_color=APPLE_COLOR,
            occupied_cells: list = [],
    ) -> None:
        self.body_color = body_color
        self.list_apple: list = []
        self.occupied_cells = occupied_cells
        self.position = self.randomize_position

    def draw(self) -> None:
        """Метод для отрисовки еды на игровом поле.

        Аргументы:
            rect: Объект с расположением и размерами еды.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, WIDTH_LINE_ONE)

    @property
    def randomize_position(self) -> tuple:
        """Метод для генерации случайного расположения еды.

        Возвращает:
            tuple: Расположение по x и y на игровом поле.
        """
        self.list_apple.clear()
        result = (
            randrange(0, SCREEN_WIDTH, GRID_SIZE),
            randrange(0, SCREEN_HEIGHT, GRID_SIZE),
        )
        for occupied in self.occupied_cells:
            if result == occupied:
                new_result = (
                    randrange(0, SCREEN_WIDTH, GRID_SIZE),
                    randrange(0, SCREEN_HEIGHT, GRID_SIZE)
                )
                self.list_apple.append(new_result)
                return new_result
            self.list_apple.append(result)
        return result


class Stone(Apple):
    """Дочерний класс Apple, предназначен для создания препятствия для змеи.

    Атрибуты:
        body_color (tuple): Цвет камня.
        list_stone (list): Список камней с их расположением.
        count (int): Количество камней на игровом поле.
        occupied_cells (list): Список всех занятых ячеек на игровом поле.
        list_stones (list): Список координат всех ячеек где находится камень.
    """

    def __init__(
            self,
            body_color=STONE_COLOR,
            occupied_cells: list = [],
            count=STONE_COUNT
    ) -> None:
        self.count = count
        self.body_color = body_color
        self.occupied_cells = occupied_cells
        self.list_stones: list = []
        self.randomize_position_stone()

    def draw(self) -> None:
        """Метод для отрисовки камня на игровом поле.

        Аргументы:
            rect: Объект с расположением и размерами камня.
        """
        for stone in self.list_stones:
            rect = pygame.Rect(stone, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, WIDTH_LINE_ONE)

    def randomize_position_stone(self) -> None:
        """Метод для генерации случайного расположения камня."""
        self.list_stones.clear()
        for _ in range(1, self.count + 1):
            result = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE),
            )
            for occupied in self.occupied_cells:
                if occupied == result:
                    new_result = (
                        randrange(0, SCREEN_WIDTH, GRID_SIZE),
                        randrange(0, SCREEN_HEIGHT, GRID_SIZE),
                    )
                    self.list_stones.append(new_result)
                else:
                    self.list_stones.append(result)


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

    def __init__(
            self,
            position=CENTER,
            positions=[CENTER],
            body_color=SNAKE_COLOR,
            length: int = LENGTH_HEAD_SNAKE,
            last: tuple = CENTER,
            direction: tuple = RIGHT,
            next_direction: Optional[tuple] = None) -> None:
        super().__init__(position, body_color)
        self.positions = positions
        self.length = length
        self.last = last
        self.direction = direction
        self.next_direction = next_direction

    def update_direction(self) -> None:
        """Обновление движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Метод передвижения змеи по сетке игрового поле,
        с переходом из одной границы поля в другю.
        """
        coordinate_x, coordinate_y = self.get_head_position
        new_x = (coordinate_x + (self.direction[0] * GRID_SIZE))
        new_y = (coordinate_y + (self.direction[1] * GRID_SIZE))
        self.positions.insert(
            0,
            (
                new_x % SCREEN_WIDTH,
                new_y % SCREEN_HEIGHT,
            )
        )
        self.last = self.positions[-1]
        self.positions.pop()

    def draw(self) -> None:
        """Отрисовка змеи."""
        head_rect = pygame.Rect(self.get_head_position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, WIDTH_LINE_ONE)

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
            if self.length == LENGTH_HEAD_SNAKE:
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
        self.length = LENGTH_HEAD_SNAKE


def draw_text(surface, text, font, color, x, y):
    """Отрисовка текста в главном меню"""
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))


def draw_button(surface, text, font, color, rect, border_color):
    """Отрисовка кнопок в главном меню"""
    pygame.draw.rect(surface, border_color, rect, WIDTH_LINE_BUTTON)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def draw_input_box(surface, text, font, color, rect, text_color):
    """Отрисовка полей ввода значений в главном меню"""
    pygame.draw.rect(surface, color, rect)
    text_surface = font.render(text, True, text_color)
    surface.blit(text_surface, (rect.x, rect.y))
    rect.w = max(MIN_WIDTH_BOX, text_surface.get_width())


def choice_box(rect, box, x, y):
    """Выбор окна ввода параметров"""
    if rect.collidepoint(x, y):
        box.is_active = not box.is_active
        box.update_color()


def proccesing_box(box, event):
    """Функция для удаления последнего элемента или ввода элемента"""
    if event.key == pygame.K_BACKSPACE:
        if box.is_active:
            box.text_user = box.text_user[:-1]
    elif box.is_active:
        box.text_user += event.unicode


def parse_str(box):
    """Функция обработки строки"""
    item = box.text_user[1:-1].replace(' ', '')
    result = {
        'R': int(item.split(',')[0]),
        'G': int(item.split(',')[1]),
        'B': int(item.split(',')[2]),
    }
    return result


def hangle_mouse(
        back_button,
        save_button,
        snake_box,
        speed_box,
        apple_box,
        stone_box,
        color_snake_rect,
        speed_snake_rect,
        color_apple_rect,
        stone_rect,
        params
):
    """Функция для обработки мышки, клавиатуры
    и кнопок для сохранения параметров игры.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if back_button.collidepoint(mouse_x, mouse_y):
                # Возвращение в главное меню.
                return False
            if save_button.collidepoint(mouse_x, mouse_y):
                # Кнопка применения настроек.
                snake = parse_str(snake_box)
                apple = parse_str(apple_box)
                params['count_stone'] = int(stone_box.text_user)
                params['speed'] = int(speed_box.text_user)
                params['color_apple'] = (apple['R'], apple['G'], apple['B'])
                params['color_snake'] = (snake['R'], snake['G'], snake['B'])
            choice_box(color_snake_rect, snake_box, mouse_x, mouse_y)
            choice_box(speed_snake_rect, speed_box, mouse_x, mouse_y)
            choice_box(color_apple_rect, apple_box, mouse_x, mouse_y)
            choice_box(stone_rect, stone_box, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            proccesing_box(snake_box, event)
            proccesing_box(speed_box, event)
            proccesing_box(apple_box, event)
            proccesing_box(stone_box, event)
    return True


def handle_keys(game_object):
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
            elif event.key == pygame.K_ESCAPE:
                return False
    return True


def show_setting(setting, params, font):
    """Функция для отображения настроек"""
    save_button = pygame.Rect(
        X_SAVE_BUTTON,
        Y_BUTTON_SETTINGS,
        LONG_RECT,
        HEIGHT_RECT,
    )

    back_button = pygame.Rect(
        X_BACK_BUTTON,
        Y_BUTTON_SETTINGS,
        LONG_RECT,
        HEIGHT_RECT,
    )
    color_snake_rect = pygame.Rect(
        SNAKE_BOX_X,
        SNAKE_BOX_Y,
        LONG_RECT,
        HEIGHT_RECT,
    )
    color_apple_rect = pygame.Rect(
        APPLE_BOX_X,
        APPLE_BOX_Y,
        LONG_RECT,
        HEIGHT_RECT,
    )
    speed_snake_rect = pygame.Rect(
        SPEED_BOX_X,
        SPEED_BOX_Y,
        LONG_RECT,
        HEIGHT_RECT,
    )
    stone_rect = pygame.Rect(
        STONE_BOX_X,
        STONE_BOX_Y,
        LONG_RECT,
        HEIGHT_RECT,
    )
    snake_box = InputBox(text_user=f'{params["color_snake"]}')
    speed_box = InputBox(text_user=f'{params["speed"]}')
    apple_box = InputBox(text_user=f'{params["color_apple"]}')
    stone_box = InputBox(text_user=f'{params["count_stone"]}')
    while setting:
        setting = hangle_mouse(
            back_button=back_button,
            save_button=save_button,
            snake_box=snake_box,
            speed_box=speed_box,
            apple_box=apple_box,
            stone_box=stone_box,
            color_snake_rect=color_snake_rect,
            speed_snake_rect=speed_snake_rect,
            color_apple_rect=color_apple_rect,
            stone_rect=stone_rect,
            params=params
        )
        screen.fill(BOARD_BACKGROUND_COLOR)
        draw_text(
            screen,
            'Цвет змеи:',
            font,
            SNAKE_COLOR,
            DRAW_X,
            DRAW_SNAKE_Y,
        )
        draw_input_box(
            screen,
            snake_box.text_user,
            font,
            snake_box.color,
            color_snake_rect,
            BOARD_BACKGROUND_COLOR,
        )
        draw_text(
            screen,
            'Цвет яблок:',
            font,
            SNAKE_COLOR,
            DRAW_X,
            DRAW_APPLE_Y,
        )
        draw_input_box(
            screen,
            apple_box.text_user,
            font,
            apple_box.color,
            color_apple_rect,
            BOARD_BACKGROUND_COLOR,
        )
        draw_text(
            screen,
            'Скорость змеи:',
            font,
            SNAKE_COLOR,
            DRAW_X,
            DRAW_SPEED_Y,
        )
        draw_input_box(
            screen,
            speed_box.text_user,
            font,
            speed_box.color,
            speed_snake_rect,
            BOARD_BACKGROUND_COLOR
        )
        draw_text(
            screen,
            'Количество камней:',
            font,
            SNAKE_COLOR,
            DRAW_X,
            DRAW_STONE_Y,
        )
        draw_input_box(
            screen,
            stone_box.text_user,
            font,
            stone_box.color,
            stone_rect,
            BOARD_BACKGROUND_COLOR
        )
        draw_button(
            screen,
            'Сохранить',
            font,
            SNAKE_COLOR,
            save_button,
            BOARD_BACKGROUND_COLOR,
        )
        draw_button(
            screen,
            'Назад',
            font,
            SNAKE_COLOR,
            back_button,
            BOARD_BACKGROUND_COLOR,
        )
        pygame.display.update()


def show_menu(params, font):
    """Функция для отображения главного меню"""
    menu = True
    setting = False
    start_button = pygame.Rect(
        X_BUTTON_MENU,
        Y_START_BUTTON,
        LONG_RECT,
        HEIGHT_RECT
    )
    settings_button = pygame.Rect(
        X_BUTTON_MENU,
        Y_SETTING_BUTTON,
        LONG_RECT,
        HEIGHT_RECT
    )
    quit_button = pygame.Rect(
        X_BUTTON_MENU,
        Y_QUIT_BUTTON,
        LONG_RECT,
        HEIGHT_RECT
    )
    while menu:
        clock.tick(params['speed'])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if start_button.collidepoint(mouse_x, mouse_y):
                    menu = False
                elif settings_button.collidepoint(mouse_x, mouse_y):
                    setting = True
                    show_setting(setting, params, font)
                elif quit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    raise SystemExit
        screen.fill(BOARD_BACKGROUND_COLOR)
        draw_text(
            screen,
            'Меню игры',
            font,
            SNAKE_COLOR,
            DRAW_MENU_X,
            DRAW_MENU_Y,
        )
        draw_button(
            screen,
            'Начать игру',
            font,
            SNAKE_COLOR,
            start_button,
            BOARD_BACKGROUND_COLOR,
        )
        draw_button(
            screen,
            'Настройки',
            font,
            SNAKE_COLOR,
            settings_button,
            BOARD_BACKGROUND_COLOR,
        )
        draw_button(
            screen,
            'Выйти',
            font,
            SNAKE_COLOR,
            quit_button,
            BOARD_BACKGROUND_COLOR
        )
        pygame.display.update()


def main():
    """Функция игры"""
    pygame.init()
    pygame.font.init()
    FONT = pygame.font.Font(None, SIZE_TEXT)
    # Параметры игры по умолчанию.
    params = {
        'speed': SPEED,
        'color_snake': SNAKE_COLOR,
        'color_apple': APPLE_COLOR,
        'count_stone': STONE_COUNT,
    }
    while True:
        show_menu(params, FONT)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake = Snake(body_color=params['color_snake'])
        stone = Stone(
            count=params['count_stone'],
            occupied_cells=snake.positions
        )
        apple = Apple(
            body_color=params['color_apple'],
            occupied_cells=snake.positions + stone.list_stones,
        )
        occupied_cells = snake.positions + stone.list_stones + apple.list_apple
        bad_food = Apple(
            body_color=BAD_FOOD_COLOR,
            occupied_cells=occupied_cells,
        )
        game = True
        while game:
            clock.tick(params['speed'])
            game = handle_keys(snake)
            snake.update_direction()
            snake.move()
            for position_stone in stone.list_stones:
                if position_stone == snake.get_head_position:
                    snake.reset()
                    stone.draw()
            if bad_food.position == snake.get_head_position:
                snake.length -= LENGTH_HEAD_SNAKE
                if snake.length < LENGTH_HEAD_SNAKE:
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
                snake.length += LENGTH_HEAD_SNAKE
                snake.added_body_snake()
                occupied = snake.positions + stone.list_stones
                apple.occupied_cells = occupied + bad_food.list_apple
                apple.position = apple.randomize_position
            for position_body_snake in snake.positions[1:]:
                if snake.get_head_position == position_body_snake:
                    snake.reset()
            snake.draw()
            stone.draw()
            apple.draw()
            bad_food.draw()
            pygame.display.update()


if __name__ == '__main__':
    main()
