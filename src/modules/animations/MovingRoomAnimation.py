import pygame as pg


from src import consts
from src.modules.levels.Room import Room


class MovingRoomAnimation:
    # Чтобы время туда-сюда в разные направления было одинаковым, умножаю на отношение длины к высоте
    vy_speed = consts.CELL_SIZE * -15
    vx_speed = vy_speed * consts.ROOM_WIDTH / consts.ROOM_HEIGHT

    def __init__(self, from_room: Room, to_room: Room, direction: consts.Moves):
        self.from_room = from_room
        self.to_room = to_room
        self.direction = direction
        self.is_over = False

        self.from_x, self.from_y = 0, 0
        if direction == consts.Moves.UP:
            self.to_x, self.to_y = 0, -consts.GAME_HEIGHT
        elif direction == consts.Moves.DOWN:
            self.to_x, self.to_y = 0, consts.GAME_HEIGHT
        elif direction == consts.Moves.RIGHT:
            self.to_x, self.to_y = consts.GAME_WIDTH, 0
        elif direction == consts.Moves.LEFT:
            self.to_x, self.to_y = -consts.GAME_WIDTH, 0
        else:
            raise ValueError("Неправильный директион...")
        self.vx, self.vy = self.vx_speed * direction.value[0], self.vy_speed * direction.value[1]

        self.screen = pg.Surface((consts.WIDTH, consts.HEIGHT))

    def render(self, screen: pg.Surface):
        time_screen = pg.Surface((consts.GAME_WIDTH, consts.GAME_HEIGHT))

        self.from_room.render(time_screen)
        self.screen.blit(time_screen, (self.from_x, self.from_y))

        self.to_room.render(time_screen)
        self.screen.blit(time_screen, (self.to_x, self.to_y))

        screen.blit(self.screen, (0, 0))

    def update(self, delta_t: float):
        self.from_x += self.vx * delta_t
        self.from_y += self.vy * delta_t
        self.to_x += self.vx * delta_t
        self.to_y += self.vy * delta_t

        # Способ рабочий, но если мало фепеес, то может сломаться)
        # if abs(self.to_x) < 10 and abs(self.to_y) < 10:
        #   self.is_over = True

        if self.direction == consts.Moves.UP:
            self.is_over = self.to_y >= 0
        elif self.direction == consts.Moves.DOWN:
            self.is_over = self.to_y <= 0
        elif self.direction == consts.Moves.RIGHT:
            self.is_over = self.to_x <= 0
        elif self.direction == consts.Moves.LEFT:
            self.is_over = self.to_x >= 0
        else:
            raise ValueError("Оно выдаёт ошибку за неверный direction ещё в ините, поэтому зачем ты что-то меняешь? А?")
