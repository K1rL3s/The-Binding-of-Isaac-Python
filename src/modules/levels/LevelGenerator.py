"""
Генератор этажа.
Вызывать generate_level(width, height, rooms) для получения карты уровня.
"""

import random
import math
import collections

from src.utils.graph import make_neighbors_graph
from src.consts import RoomsTypes, Moves


# Оптимизировать это, проложив путь от старта до всех возможных точек и проверить, что все точки задействованы.
def all_rooms_have_path_to_start(rooms: list[list[RoomsTypes | str]], *, ignore_secret: bool = True) -> bool:
    """
    Проверка, все ли комнаты имеют путь до стартовой комнаты.

    :param rooms: Двумерный массив значений типов комнат.
    :param ignore_secret: Игнорировать ли секретную комнату.
    :return: Все ли комнаты имеют путь до стартовой комнаты.
    """
    graph = make_neighbors_graph(rooms, ignore_secret=ignore_secret)
    ignored = (RoomsTypes.EMPTY, RoomsTypes.SECRET)
    for y, row in enumerate(rooms):
        for x, col in enumerate(row):
            if rooms[y][x] not in ignored:
                if not has_path_to_start((x, y), rooms, ignore_secret=ignore_secret, graph=graph):
                    return False
    return True


def has_path_to_start(start_pos: tuple[int, int], rooms: list[list[RoomsTypes | str]],
                      *,
                      ignore_secret: bool = True, graph: dict[tuple[int, int], list[tuple[int, int]]] = None) -> bool:
    """
    Проверка, можно ли дойти от клетки до стартовой комнаты.

    :param start_pos: Позиция клетки, из которой начинается путь.
    :param rooms: Двумерный массив значений типов комнат.
    :param ignore_secret: Игнорировать ли секретную комнату.
    :param graph: Графоподобный словарь (передаётся для того, чтобы не пересоздавать его на проверку каждой комнаты).
    :return: Все ли комнаты имеют путь до стартовой комнаты.
    """
    map_width, map_height = len(rooms[0]), len(rooms)
    end_pos = math.ceil(map_width / 2) - 1, math.ceil(map_height / 2) - 1,
    if graph is None:
        graph = make_neighbors_graph(rooms, ignore_secret=ignore_secret)
    queue = collections.deque([start_pos])
    visited: dict[tuple[int, int], tuple[int, int]] = {start_pos: None}
    while queue:
        current_cell = queue.popleft()
        if current_cell == end_pos:
            break
        next_cells = graph.get(current_cell, [])
        for next_cell in next_cells:
            if next_cell not in visited.keys():
                queue.append(next_cell)
                visited[next_cell] = current_cell
    return end_pos in visited.keys()


def set_secret_room(rooms: list[list[RoomsTypes | str]]) -> bool:
    """
    Установка секретной комнаты.

    :param rooms: Двумерный массив значений типов комнат.
    :return: Успешно ли поставлена секретная комната.
    """
    graph = make_neighbors_graph(rooms)
    is_okay = False
    # Сначала ставит секретку там, где 4 соседа, потом там, где 3, потом там, где 2.
    # Теперь работает медленнее :)
    for neighbors_rooms in range(4, 1, -1):
        secrets = [room for room in graph if len(graph[room]) >= neighbors_rooms
                   and rooms[room[1]][room[0]] == RoomsTypes.DEFAULT]
        random.shuffle(secrets)
        for x, y in secrets:
            rooms[y][x] = RoomsTypes.SECRET
            if all_rooms_have_path_to_start(rooms):
                is_okay = True
                break
            else:
                rooms[y][x] = RoomsTypes.DEFAULT
        if is_okay:
            break
    return is_okay


def set_special_rooms(rooms: list[list[RoomsTypes | str]]) -> bool:
    """
    Расстановка специальных комнат (сокровищница, магазин, босс).

    :param rooms: Двумерный массив значений типов комнат.
    :return: Успешно ли поставлены все специальные комнаты.
    """
    # Поиск комнат с одним соседом для установки сокровищницы, магазина и комнаты с боссом
    graph = make_neighbors_graph(rooms, ignore_secret=True)
    solo = [room for room in graph if len(graph[room]) == 1 and rooms[room[1]][room[0]] == RoomsTypes.DEFAULT]
    if len(solo) < 3:
        return False

    # Установка комнаты с боссом как можно дальше от места спавна
    map_width, map_height = len(rooms[0]), len(rooms)
    spawn_x, spawn_y = math.ceil(map_width / 2) - 1, math.ceil(map_height / 2) - 1
    boss_x, boss_y = max(solo, key=lambda c: math.sqrt((spawn_x - c[0]) ** 2 + (spawn_y - c[1]) ** 2))
    rooms[boss_y][boss_x] = RoomsTypes.BOSS
    solo.remove((boss_x, boss_y))

    # Случайная установка магазина и сокровищницы
    random.shuffle(solo)
    for coords, room_type in zip(solo, (RoomsTypes.SHOP, RoomsTypes.TREASURE)):
        x, y = coords
        rooms[y][x] = room_type

    return True


def set_other_rooms(rooms: list[list[RoomsTypes | str]]) -> bool:
    """
    Расстановка комнат, отличных от спавна и дефолтных.

    :param rooms: Двумерный массив значений типов комнат.
    :return: Успешно ли поставлены все комнаты.
    """
    # Установка секретной комнаты
    if not set_secret_room(rooms):
        return False

    # Установка специальных комнат
    if not set_special_rooms(rooms):
        return False

    return True


def set_default_rooms(rooms: list[list[RoomsTypes | str]], room_numbers: int) -> None:
    """
    Расстановка RoomsTypes.DEFAULT и RoomsTypes.SPAWN на пустой карте.

    :param rooms: Двумерный массив значений типов комнат (в этом случае - RoomsTypes.EMPTY).
    :param room_numbers: Сколько комнат заполнить значением дефолтной комнаты.
    :return: None
    """

    map_width, map_height = len(rooms[0]), len(rooms)
    cur_x, cur_y = math.ceil(map_width / 2) - 1, math.ceil(map_height / 2) - 1
    room_numbers -= 1
    rooms[cur_y][cur_x] = RoomsTypes.SPAWN
    moves = [move.value for move in Moves]
    # Попытка сделать алгоритм "бегающей собаки" из какого-то видоса про генерацию уровней в Айзеке
    while room_numbers > 0:
        step_x, step_y = random.choice(moves)
        cur_x = max(0, min(map_width - 1, cur_x + step_x))
        cur_y = max(0, min(map_height - 1, cur_y + step_y))
        if rooms[cur_y][cur_x] == RoomsTypes.EMPTY:
            room_numbers -= 1
            rooms[cur_y][cur_x] = RoomsTypes.DEFAULT


def generate_level(map_width: int, map_height: int, room_numbers: int) -> list[list[RoomsTypes | str]]:
    """
    Генератор этажа (уровня).

    :param map_width: ширина этажа.
    :param map_height: высота этажа.
    :param room_numbers: - количество комнат с учетом спавна, магазина, босса итд итп.
    """
    assert 3 <= map_width <= 10                        # Проверка размера карты
    assert 3 <= map_height <= 10                       # Проверка размера карты
    assert room_numbers >= 5                           # Спавн, магазин, сокровищница, босс, секретная комната
    assert room_numbers < map_width * map_height - 3   # Возможно сгенерировать все комнаты

    rooms = []
    successful_generation = False
    while not successful_generation:
        # Генерация уровня, пока не появится подходящая планировка
        rooms = [[RoomsTypes.EMPTY] * map_width for _ in range(map_height)]
        set_default_rooms(rooms, room_numbers)
        successful_generation = set_other_rooms(rooms)
    assert rooms
    return rooms


def print_map(rooms: list[list[RoomsTypes | str]]) -> None:
    """
    Вывод карты в консоль.

    :param rooms: Двумерный массив значений типов комнат.
    :return: None.
    """
    for row in rooms:
        for col in row:
            print(col.value.center(8, ' '), end=' ')
        print()


def main():
    mapa = generate_level(10, 10, 50)
    print_map(mapa)


if __name__ == '__main__':
    main()
