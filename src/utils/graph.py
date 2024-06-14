import collections

from src import consts


def valid_coords(x: int, y: int, width: int, height: int) -> bool:
    """
    Проверка координат на выход за пределы списка.

    :param x: Координата столбца.
    :param y: Координата строки.
    :param width: Ширина двумерного массива.
    :param height: Высота двумерного массива.
    :return: Корректны ли координаты.
    """
    return width > x >= 0 and height > y >= 0


def get_neighbors_coords(
    x: int,
    y: int,
    rooms: list[list[consts.RoomsTypes | str]],
    *,
    ignore_secret: bool = False,
    use_diagonals: bool = False,
) -> list[tuple[int, int]]:
    """
    Получение координат клеток-соседей, в которые можно пройти.

    :param x: Координата столбца.
    :param y: Координата строки.
    :param rooms: Двумерный массив значений типов комнат.
    :param ignore_secret: Игнорировать ли секретную комнату.
    :param use_diagonals: Использовать ли диагональные пути.
    :return: Список со всеми координатами соседей, в которые можно пройти.
    """
    moves = [(0, -1), (0, 1), (1, 0), (-1, 0)]
    if use_diagonals:
        moves += [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    map_width, map_height = len(rooms[0]), len(rooms)
    ignored = [consts.RoomsTypes.EMPTY]
    if ignore_secret:
        ignored.append(consts.RoomsTypes.SECRET)
    return [
        (x + i, y + j)
        for i, j in moves
        if valid_coords(x + i, y + j, map_width, map_height)
        and rooms[y + j][x + i] not in ignored
    ]


# Попытаться сделать ход по диагонали, если соседние клетки в эту сторону свободны
# мб надо побаловаться с созданием графа
def make_path_to_cell(
    graph: dict[tuple[int, int]],
    xy_start: tuple[int, int],
    xy_end: tuple[int, int],
) -> bool | list[tuple[int, int]]:
    """
    Проверка, можно ли дойти от клетки до стартовой комнаты.

    :param graph: Графоподобный словарь клеток комнаты.
    :param xy_start: Начальная клетка.
    :param xy_end: Конечная клетка.
    :return: Список клеток пути или False.
    """
    queue = collections.deque([xy_start])
    visited: dict[tuple[int, int], tuple[int, int]] = {xy_start: None}
    while queue:
        current_cell = queue.popleft()
        if current_cell == xy_end:
            break
        next_cells = graph.get(current_cell, [])
        for next_cell in next_cells:
            if next_cell not in visited:
                queue.append(next_cell)
                visited[next_cell] = current_cell

    if xy_end not in visited:
        return False

    way: list[tuple[int, int]] = []
    path_segment = xy_end
    while path_segment and path_segment in visited:
        way.append(path_segment)
        path_segment = visited[path_segment]
    way.reverse()
    return way


def make_neighbors_graph(
    rooms: list[list[consts.RoomsTypes | str]],
    ignore_secret: bool = False,
    use_diagonals: bool = False,
) -> dict[tuple[int, int], list[tuple[int, int]]]:
    """
    Генерация графа соседей.
    Используется как для построения графа всей карты, так и для построения графа конкретной комнаты,
    для этого нужно передать массив rooms со значениями:
      consts.RoomTypes.DEFAULT, если можно ходить по клетке;
      consts.RoomTypes.EMPTY, если нельзя ходить по клетке.


    :param rooms: Двумерный массив значений типов комнат.
    :param ignore_secret: Игнорировать ли секретную комнату.
    :param use_diagonals: Использовать ли диагональные пути.
    :return: Графоподобный словарь (координаты: список координат соседей).
    """
    graph = collections.defaultdict(
        list,
    )  # dict[tuple[int, int], list[tuple[int, int]]]
    # клетка -> список соседей, в которые можно пройти
    for y, row in enumerate(rooms):
        for x, col in enumerate(row):
            if col != consts.RoomsTypes.EMPTY:
                graph[(x, y)].extend(
                    get_neighbors_coords(
                        x,
                        y,
                        rooms,
                        ignore_secret=ignore_secret,
                        use_diagonals=use_diagonals,
                    ),
                )
    return graph
