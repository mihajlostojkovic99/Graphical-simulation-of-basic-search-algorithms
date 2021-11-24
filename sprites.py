import pygame
import os
import config
import statistics
import time


class BaseSprite(pygame.sprite.Sprite):
    images = dict()

    def __init__(self, row, col, file_name, transparent_color=None):
        pygame.sprite.Sprite.__init__(self)
        if file_name in BaseSprite.images:
            self.image = BaseSprite.images[file_name]
        else:
            self.image = pygame.image.load(os.path.join(config.IMG_FOLDER, file_name)).convert()
            self.image = pygame.transform.scale(self.image, (config.TILE_SIZE, config.TILE_SIZE))
            BaseSprite.images[file_name] = self.image
        # making the image transparent (if needed)
        if transparent_color:
            self.image.set_colorkey(transparent_color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * config.TILE_SIZE, row * config.TILE_SIZE)
        self.row = row
        self.col = col


class Agent(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Agent, self).__init__(row, col, file_name, config.DARK_GREEN)

    def move_towards(self, row, col):
        row = row - self.row
        col = col - self.col
        self.rect.x += col
        self.rect.y += row

    def place_to(self, row, col):
        self.row = row
        self.col = col
        self.rect.x = col * config.TILE_SIZE
        self.rect.y = row * config.TILE_SIZE

    # game_map - list of lists of elements of type Tile
    # goal - (row, col)
    # return value - list of elements of type Tile
    def get_agent_path(self, game_map, goal):
        pass


class ExampleAgent(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map, goal):
        path = [game_map[self.row][self.col]]

        row = self.row
        col = self.col
        while True:
            if row != goal[0]:
                row = row + 1 if row < goal[0] else row - 1
            elif col != goal[1]:
                col = col + 1 if col < goal[1] else col - 1
            else:
                break
            path.append(game_map[row][col])
        return path


class Tile(BaseSprite):
    def __init__(self, row, col, file_name):
        super(Tile, self).__init__(row, col, file_name)

    def position(self):
        return self.row, self.col

    def cost(self):
        pass

    def kind(self):
        pass


class Stone(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'stone.png')

    def cost(self):
        return 1000

    def kind(self):
        return 's'


class Water(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'water.png')

    def cost(self):
        return 500

    def kind(self):
        return 'w'


class Road(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'road.png')

    def cost(self):
        return 2

    def kind(self):
        return 'r'


class Grass(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'grass.png')

    def cost(self):
        return 3

    def kind(self):
        return 'g'


class Mud(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'mud.png')

    def cost(self):
        return 5

    def kind(self):
        return 'm'


class Dune(Tile):
    def __init__(self, row, col):
        super().__init__(row, col, 'dune.png')

    def cost(self):
        return 7

    def kind(self):
        return 's'


class Goal(BaseSprite):
    def __init__(self, row, col):
        super().__init__(row, col, 'x.png', config.DARK_GREEN)


class Trail(BaseSprite):
    def __init__(self, row, col, num):
        super().__init__(row, col, 'trail.png', config.DARK_GREEN)
        self.num = num

    def draw(self, screen):
        text = config.GAME_FONT.render(f'{self.num}', True, config.WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)


def get_next_nodes_Aki(row, col, path: list[Tile], game_map):
    next_tiles: list[list[int]] = []

    if row - 1 >= 0:  # north tile
        next_tiles.append([row - 1, col])
    if col + 1 < len(game_map[row]):  # east tile
        next_tiles.append([row, col + 1])
    if row + 1 < len(game_map):  # south tile
        next_tiles.append([row + 1, col])
    if col - 1 >= 0:  # west tile
        next_tiles.append([row, col - 1])

    final = []

    for i in next_tiles:
        if game_map[i[0]][i[1]] not in path:
            final.append(i)
    final.reverse()
    final = sort_nodes_Aki(final, game_map)
    return final


def sort_nodes_Aki(nodes: list[list[int]], game_map: list[list[Tile]]):
    return sorted(nodes, key=lambda elem: game_map[elem[0]][elem[1]].cost(), reverse=True)


def neighbors(tile1, tile2):
    if tile1[0] in [tile2[0] - 1, tile2[0] + 1] and tile1[1] == tile2[1]:
        return True
    if tile1[1] in [tile2[1] - 1, tile2[1] + 1] and tile1[0] == tile2[0]:
        return True
    return False


def recalculate_path(path, next_tile):
    while True:
        tile = path.pop()
        tmp = tile.position()
        if neighbors(tmp, next_tile):
            path.append(tile)
            return path


class Aki(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map: list[list[Tile]], goal):
        path = []
        stack: list[list[int]] = [[self.row, self.col]]

        while True:
            cur_tile = stack.pop()

            if cur_tile[0] == goal[0] and cur_tile[1] == goal[1]:
                path.append(game_map[cur_tile[0]][cur_tile[1]])
                return path

            next_tiles: list[list[int]] = get_next_nodes_Aki(cur_tile[0], cur_tile[1], path, game_map)
            # dohvati sledece korake na kojima igrac nije prethodno bio i sortira ih

            if len(next_tiles) == 0:
                path = recalculate_path(path, stack[len(stack) - 1])  # ako je zaglavio po dubini, ovim se backtrackuje
                continue

            for tile in next_tiles:
                stack.append(tile)
            path.append(game_map[cur_tile[0]][cur_tile[1]])


def get_next_nodes_Jocke(row, col, cur_tile, game_map, visited):
    next_tiles: list[list[int]] = []

    if row - 1 >= 0:  # north tile
        tmp = [row - 1, col]
        tmp.extend(cur_tile)
        next_tiles.append(tmp)
    if col + 1 < len(game_map[row]):  # east tile
        tmp = [row, col + 1]
        tmp.extend(cur_tile)
        next_tiles.append(tmp)
    if row + 1 < len(game_map):  # south tile
        tmp = [row + 1, col]
        tmp.extend(cur_tile)
        next_tiles.append(tmp)
    if col - 1 >= 0:  # west tile
        tmp = [row, col - 1]
        tmp.extend(cur_tile)
        next_tiles.append(tmp)

    parent_list = []
    cnt = 0
    while True:
        row = cur_tile[cnt]
        cnt += 1
        col = cur_tile[cnt]
        cnt += 1
        parent_list.append([row, col])
        if row == -1:
            break
    final = [x for x in next_tiles if [x[0], x[1]] not in parent_list and [x[0], x[1]] not in visited]
    # sklanjam tile iz kog smo dosli u ovaj
    return final


def get_neighbors_for_sort(row, col, parent_row, parent_col, game_map):
    neigh: list[list[int]] = []
    if row - 1 >= 0:  # north tile
        tmp = [row - 1, col]
        neigh.append(tmp)
    if col + 1 < len(game_map[row]):  # east tile
        tmp = [row, col + 1]
        neigh.append(tmp)
    if row + 1 < len(game_map):  # south tile
        tmp = [row + 1, col]
        neigh.append(tmp)
    if col - 1 >= 0:  # west tile
        tmp = [row, col - 1]
        neigh.append(tmp)

    final = [elem for elem in neigh if elem[0] != parent_row or elem[1] != parent_col]
    return final


def sort_nodes_Jocke(nodes: list[list[int]], game_map: list[list[Tile]]):
    return sorted(nodes, key=lambda elem: statistics.mean(
        [game_map[x[0]][x[1]].cost() for x in get_neighbors_for_sort(elem[0], elem[1],
                                                                     elem[2], elem[3],
                                                                     game_map)]))


def generate_path(tile, game_map: list[list[Tile]], start_time: float = -1):
    path: list[Tile] = []
    while True:
        row = tile.pop(0)
        col = tile.pop(0)
        if row == -1:
            break
        path.append(game_map[row][col])
    path.reverse()
    if start_time != -1:
        print("Igrac je pronasao put za " + str(time.perf_counter() - start_time) + "ms!")
    return path


class Jocke(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map: list[list[Tile]], goal):
        queue: list[list[int]] = [[self.row, self.col, -1, -1]]
        visited: list[list[int]] = []
        start = time.perf_counter()

        while True:
            cur_tile = queue.pop(0)
            if [cur_tile[0], cur_tile[1]] in visited:
                continue
            visited.append([cur_tile[0], cur_tile[1]])

            next_tiles: list[list[int]] = get_next_nodes_Jocke(cur_tile[0], cur_tile[1], cur_tile, game_map, visited)

            next_tiles = sort_nodes_Jocke(next_tiles, game_map)

            for tile in next_tiles:
                if game_map[tile[0]][tile[1]] == game_map[goal[0]][goal[1]]:
                    # nasli smo put do cilja, treba krenuti unazad i oformiti path
                    path = generate_path(tile, game_map, start)
                    return path

            for tile in next_tiles:
                queue.append(tile)


def get_next_nodes_Draza(row, col, cur_tile, game_map, visited, paths):
    next_tiles: list[list[int]] = []

    if row - 1 >= 0:  # north tile
        tmp = [row - 1, col]
        tmp.extend(cur_tile)
        next_tiles.append(tmp)
    if col + 1 < len(game_map[row]):  # east tile
        tmp = [row, col + 1]
        tmp.extend(cur_tile)
        next_tiles.append(tmp)
    if row + 1 < len(game_map):  # south tile
        tmp = [row + 1, col]
        tmp.extend(cur_tile)
        next_tiles.append(tmp)
    if col - 1 >= 0:  # west tile
        tmp = [row, col - 1]
        tmp.extend(cur_tile)
        next_tiles.append(tmp)

    tmp = [elem for elem in next_tiles if elem[0] != cur_tile[2] or elem[1] != cur_tile[3]]  # skloni prethodni tile
    final = [x for x in tmp if [x[0], x[1]] not in visited] # skloni tile ako si ga vec posetio
    return final


def calc_cost(node: list[int], game_map: list[list[Tile]]):
    sum = 0
    cnt = 0
    while True:
        row = node[cnt]
        cnt += 1
        col = node[cnt]
        cnt += 1
        if row == -1:
            break
        sum += game_map[row][col].cost()
    return sum


def sort_nodes_Draza(nodes: list[list[int]], game_map: list[list[Tile]]):
    return sorted(nodes, key=lambda elem: (calc_cost(elem, game_map), len(elem)))


class Draza(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map: list[list[Tile]], goal):
        paths: list[list[int]] = [[self.row, self.col, -1, -1]]
        visited: list[list[int]] = []
        start = time.perf_counter()

        while True:
            cur_tile = paths.pop(0)
            if [cur_tile[0], cur_tile[1]] in visited:
                continue
            visited.append([cur_tile[0], cur_tile[1]])

            if game_map[cur_tile[0]][cur_tile[1]] == game_map[goal[0]][goal[1]]:
                path = generate_path(cur_tile, game_map, start)
                return path

            next_tiles: list[list[int]] = get_next_nodes_Draza(cur_tile[0], cur_tile[1], cur_tile, game_map, visited,
                                                               paths)

            for tile in next_tiles:
                paths.append(tile)
            paths = sort_nodes_Draza(paths, game_map)


def calc_cost_Bole(node: list[int], game_map: list[list[Tile]], goal, min_cost):
    sum = 0
    cnt = 2
    while True:
        row = node[cnt]
        cnt += 1
        col = node[cnt]
        cnt += 1
        if row == -1:
            break
        sum += game_map[row][col].cost()
    dx = abs(node[0] - goal[0])
    dy = abs(node[1] - goal[1])
    sum += game_map[node[0]][node[1]].cost()
    sum += min_cost * (dx + dy)
    return sum


def sort_nodes_Bole(nodes: list[list[int]], game_map: list[list[Tile]], goal, min_cost):
    return sorted(nodes, key=lambda elem: (calc_cost_Bole(elem, game_map, goal, min_cost), len(elem)))


class Bole(Agent):
    def __init__(self, row, col, file_name):
        super().__init__(row, col, file_name)

    def get_agent_path(self, game_map: list[list[Tile]], goal):
        paths: list[list[int]] = [[self.row, self.col, -1, -1]]
        visited: list[list[int]] = []
        start = time.perf_counter()

        min_cost = game_map[0][0].cost()
        for x in game_map:
            for y in x:
                if y.cost() < min_cost:
                    min_cost = y.cost()

        while True:
            cur_tile = paths.pop(0)
            if [cur_tile[0], cur_tile[1]] in visited:
                continue
            visited.append([cur_tile[0], cur_tile[1]])

            if game_map[cur_tile[0]][cur_tile[1]] == game_map[goal[0]][goal[1]]:
                path = generate_path(cur_tile, game_map, start)
                return path

            next_tiles: list[list[int]] = get_next_nodes_Draza(cur_tile[0], cur_tile[1], cur_tile, game_map, visited, paths)

            for tile in next_tiles:
                paths.append(tile)
            paths = sort_nodes_Bole(paths, game_map, goal, min_cost)
