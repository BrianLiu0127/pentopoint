import time

import numpy as np
import heapq

from PIL import Image
import math


class Node:
    def __init__(self, x, y, direction, g=0, h=0, parent=None):
        self.x = x
        self.y = y
        self.direction = direction
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f


def calu_h(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class TspSolver:
    def __init__(self, _shelves_position=0, _end_point=(150, 5)):
        self.node = None
        self.maze = np.array([])
        self.get_map()
        self.pos_array = np.array([])
        self.name_array = np.array([])
        self.dist_map = np.array([])
        self.shelves_position = _shelves_position
        self.path_map = []
        self.end_point = 150, 5
        self.route = []
        self.ref_index = np.array([])
        self.end_dist = np.array([])
        self.start_dist = np.array([])
        self.shelves_index = get_shelves_index()
        self.index_inv = ["茶", "啤酒", "米", "醬", "雞精", "衛生紙", "牛奶", "巧克力", "堅果", "飲料", "酒類",
                          "南北貨",
                          "調味料", "營養品", "清潔用品", "冷藏/凍食品", "休閒食品"]

        self.translate = {}  # tuple(int,int) 對應到 int
        st = time.time()
        if self.shelves_position:
            self.re_calcu(self.shelves_position)
        self.shelves_position = get_shelves_maze()
        self.dist_map = np.load("distance_array_2d.npy")
        self.end_dist = np.load("end_array_2d.npy")

    def get_map(self):
        img = Image.open("map0316.jpg")
        new_width = 160
        new_height = 160
        img = img.resize((new_width, new_height))
        img_grayscale = img.convert("L")
        threshold = 200
        # 將像素值大於閾值的設置為1,小於等於閾值的設置為0
        maze = np.array(img_grayscale)

        self.maze = (maze < threshold)

    def re_calcu(self, _shelves_position: dict):
        self.node = [(19, 40), (27, 94), (50, 32), (8, 126), (50, 120), (91, 73), (132, 45), (137, 134), (143, 127),
                     (18, 30), (17, 81), (82, 32), (18, 132), (81, 81), (81, 133), (138, 62), (138, 125)]
        for key in _shelves_position:
            # self.node.append(_shelves_position[key])
            print(_shelves_position[key], ",", end="")
        n = len(self.node)
        self.dist_map = np.zeros((n, n))
        self.path_map = [[[] for _ in range(n)] for _ in range(n)]
        self.end_dist = np.zeros(n)
        for i in range(n):
            for j in range(i, n):
                self.dist_map[i, j], path = self.A_star(self.node[i], self.node[j])
                self.path_map[i][j] = path
                self.dist_map[j, i] = self.dist_map[i, j]
                # print(path)
        for i in range(n):
            self.end_dist[i], _ = self.A_star(self.node[i], self.end_point)

        np.save("distance_array_2d", self.dist_map)
        np.save("end_array_2d", self.end_dist)
        return

    def get_sorted_list(self, cur_pos: tuple[int, int], name_list: tuple[str]) -> list[str]:
        self.name_array = np.array(name_list)
        r = np.array([self.shelves_index[n] for n in self.name_array])
        # calculate_dist from cur_pos to all node
        self.start_dist = np.array([calu_h(cur_pos[0] * 5, 160 - 5 * cur_pos[1], self.shelves_position[key][0], \
                                           self.shelves_position[key][1]) for key in self.shelves_position])
        d, r = self.tsp_sa(r)
        sorted_list = [self.index_inv[idx] for idx in r]
        print(sorted_list)
        # use SA to sort route
        return sorted_list

    def get_path(self, cur: tuple[int, int], target: str) -> list[tuple[int, int]]:
        new_cur = (cur[0] * 5, (160 - cur[1]* 5))
        d, path = self.A_star(new_cur, self.shelves_position[target])
        return path

    def A_star(self, start, end) -> {int, list[int, int]}:
        rows, cols = len(self.maze), len(self.maze[0])
        start_direction = (0, 0)
        start_node = Node(start[0], start[1], start_direction, h=calu_h(start[0], start[1], end[0], end[1]))
        end_node = Node(end[0], end[1], None)
        open_set = []
        heapq.heappush(open_set, start_node)
        came_from = {}
        g_scores = {start: float('inf') for _ in range(rows) for _ in range(cols)}
        g_scores[start] = 0
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        while open_set:
            current = heapq.heappop(open_set)

            if (current.x, current.y) == (end_node.x, end_node.y):
                path = []
                d = 0
                prev_x, prev_y = -1, -1
                while current:
                    if current.parent is None or (current.parent.x != prev_x and current.parent.y != prev_y):
                        path.append((current.x / 5, (160 - current.y) / 5))
                        prev_x = current.x
                        prev_y = current.y
                    current = current.parent
                    d += 1
                return d, path[::-1]  # Return reversed path

            for dx, dy in directions:
                nx, ny = current.x + dx, current.y + dy
                new_direction = (dx, dy)

                if rows > nx >= 0 and 0 <= ny < cols and self.maze[ny][nx] == 0:
                    new_g_score = current.g + 1 + (new_direction != current.direction) / 2

                    if new_g_score < g_scores.get((nx, ny), float('inf')):
                        neighbor = Node(nx, ny, new_direction, g=new_g_score, h=calu_h(nx, ny, end[0], end[1]))
                        neighbor.parent = current
                        g_scores[(nx, ny)] = new_g_score
                        neighbor.f = new_g_score + neighbor.h
                        heapq.heappush(open_set, neighbor)
                        came_from[(nx, ny)] = current

        print(f"No path found between {start} and {end}")
        return 10000, None  # No path found

    def calculate_dist(self, route: np.array):
        n = len(route)
        return sum(self.dist_map[route[i], route[(i + 1)]] for i in range(n - 1)) + self.end_dist[route[n - 1]] + \
            self.start_dist[route[0]]

    def tsp_sa(self, r, t0=500, t_min=0.1, k=40, cool_down=0.99):
        t = t0

        n = len(r)
        route = r
        current_distance = self.calculate_dist(route)
        print(f' distance :{current_distance}')

        while t >= t_min:
            t *= cool_down
            for _ in range(k):
                i, j = np.random.randint(0, n, size=2)
                new_route = route.copy()
                new_route[i], new_route[j] = new_route[j], new_route[i]
                new_distance = self.calculate_dist(new_route)
                if new_distance < current_distance or np.random.random() < math.exp(
                        (current_distance - new_distance) / t):
                    route = new_route
                    current_distance = new_distance

        print(f' distance :{current_distance}')
        print(f' route : {route}')
        return current_distance, route


def get_shelves_index():
    shelves_index = {
        "茶": 0,
        "啤酒": 1,
        "米": 2,
        "醬": 3,
        "雞精": 4,
        "衛生紙": 5,
        "牛奶": 6,
        "巧克力": 7,
        "堅果": 8,
        "飲料": 9,
        "酒類": 10,
        "南北貨": 11,
        "調味料": 12,
        "營養品": 13,
        "清潔用品": 14,
        "冷藏/凍食品": 15,
        "休閒食品": 16
    }
    return shelves_index


def get_shelves_maze():
    shelves_position = {
        "茶": (19, 40),
        "啤酒": (27, 94),
        "米": (50, 32),
        "醬": (8, 126),
        "雞精": (50, 120),
        "衛生紙": (91, 73),
        "牛奶": (132, 45),
        "巧克力": (137, 134),
        "堅果": (143, 127),
        "飲料": (18, 30),
        "酒類": (17, 81),
        "南北貨": (82, 32),
        "調味料": (18, 132),
        "營養品": (81, 81),
        "清潔用品": (81, 133),
        "冷藏/凍食品": (138, 62),
        "休閒食品": (138, 125)
    }
    return shelves_position


# tsp_solver = TspSolver()
# sl = tsp_solver.get_sorted_list((10, 10), ("衛生紙", "南北貨", "茶", "米", "雞精", "飲料", "酒類", "調味料"))
# print(tsp_solver.get_path((0, 0), "牛奶"))
