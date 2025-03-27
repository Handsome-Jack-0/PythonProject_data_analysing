import random
import pygame
from collections import deque


class MazeGenerator:
    def __init__(self, width, height, difficulty='medium'):
        self.width = width
        self.height = height
        # 调整迷宫数组维度为 (2h+1) x (2w+1)
        self.maze = [[1] * (2 * width + 1) for _ in range(2 * height + 1)]
        self.visited = [[False] * width for _ in range(height)]
        self.difficulty = difficulty
        self.entrance = None
        self.exit = None

    def set_difficulty(self):
        difficulty_settings = {
            'easy': 0.2,
            'medium': 0.5,
            'hard': 0.8
        }
        self.wall_probability = difficulty_settings.get(self.difficulty, 0.5)

    def generate_maze(self):
        self.set_difficulty()
        # 初始化随机起点
        start_x = random.randint(0, self.width - 1)
        start_y = random.randint(0, self.height - 1)

        # 使用DFS生成迷宫基础结构
        stack = [(start_x, start_y)]
        self.visited[start_y][start_x] = True
        self.maze[2 * start_y + 1][2 * start_x + 1] = 0

        while stack:
            x, y = stack[-1]
            neighbors = self._get_unvisited_neighbors(x, y)

            if neighbors:
                nx, ny = random.choice(neighbors)
                # 打通当前单元格与邻居之间的墙
                self.maze[2 * y + 1 + (ny - y)][2 * x + 1 + (nx - x)] = 0
                self.maze[2 * ny + 1][2 * nx + 1] = 0
                self.visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        # 设置入口和出口（关键修改）
        mid_y = 2 * self.height // 2  # 垂直方向中间位置（因为数组长度是2h+1）
        self.entrance = (0, mid_y)  # 左边界中间
        self.exit = (2 * self.width, mid_y)  # 右边界中间

        # 确保入口出口是通路
        self.maze[mid_y][0] = 0
        self.maze[mid_y][2 * self.width] = 0

        # 根据难度添加随机墙壁
        self._add_random_walls()

        return self.maze

    def _get_unvisited_neighbors(self, x, y):
        """获取未访问的相邻单元格"""
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if not self.visited[ny][nx]:
                    neighbors.append((nx, ny))
        return neighbors

    def _add_random_walls(self):
        """根据难度添加额外墙壁"""
        for y in range(1, 2 * self.height, 2):
            for x in range(1, 2 * self.width, 2):
                if random.random() < self.wall_probability:
                    candidates = []
                    # 检查上下左右可能的墙壁位置
                    if y > 1 and self.maze[y - 1][x] == 0:
                        candidates.append((y - 1, x))
                    if y < 2 * self.height - 1 and self.maze[y + 1][x] == 0:
                        candidates.append((y + 1, x))
                    if x > 1 and self.maze[y][x - 1] == 0:
                        candidates.append((y, x - 1))
                    if x < 2 * self.width - 1 and self.maze[y][x + 1] == 0:
                        candidates.append((y, x + 1))

                    for candidate in candidates:
                        wy, wx = candidate
                        # 临时添加墙壁
                        temp_maze = [row[:] for row in self.maze]
                        temp_maze[wy][wx] = 1
                        # 检查添加墙壁后是否仍然连通
                        if self._is_connected(temp_maze, self.entrance, self.exit):
                            self.maze[wy][wx] = 1

    def _is_connected(self, maze, start, end):
        """检查从起点到终点是否连通"""
        queue = deque([start])
        visited = set()
        visited.add(start)

        while queue:
            x, y = queue.popleft()
            if (x, y) == end:
                return True
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 0 and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited.add((nx, ny))
        return False


def play_maze(maze, entrance, exit):
    pygame.init()
    CELL_SIZE = 20
    WINDOW_SIZE = (len(maze[0]) * CELL_SIZE, len(maze) * CELL_SIZE)

    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Maze Game")

    # 初始化玩家位置（入口坐标转换）
    player_pos = [entrance[0], entrance[1]]

    clock = pygame.time.Clock()
    running = True
    game_won = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 处理键盘输入
        keys = pygame.key.get_pressed()
        new_pos = player_pos.copy()
        if keys[pygame.K_UP]:
            new_pos[1] -= 1
        if keys[pygame.K_DOWN]:
            new_pos[1] += 1
        if keys[pygame.K_LEFT]:
            new_pos[0] -= 1
        if keys[pygame.K_RIGHT]:
            new_pos[0] += 1

        # 验证移动有效性
        if 0 <= new_pos[0] < len(maze[0]) and 0 <= new_pos[1] < len(maze):
            if maze[new_pos[1]][new_pos[0]] == 0:
                player_pos = new_pos

        # 检查胜利条件
        if (player_pos[0], player_pos[1]) == exit:
            game_won = True
            running = False

        # 绘制界面
        screen.fill((255, 255, 255))

        # 绘制迷宫
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # 绘制入口（绿色）和出口（红色）
        pygame.draw.rect(screen, (0, 255, 0),
                         (entrance[0] * CELL_SIZE, entrance[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, (255, 0, 0),
                         (exit[0] * CELL_SIZE, exit[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        # 绘制玩家（蓝色）
        pygame.draw.rect(screen, (0, 0, 255),
                         (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    if game_won:
        print("Congratulations! You've escaped the maze!")


if __name__ == "__main__":
    WIDTH = 10
    HEIGHT = 10
    DIFFICULTY = 'medium'

    generator = MazeGenerator(WIDTH, HEIGHT, DIFFICULTY)
    maze = generator.generate_maze()

    # 验证入口出口坐标有效性
    print(f"Entrance: {generator.entrance}")
    print(f"Exit: {generator.exit}")

    play_maze(maze, generator.entrance, generator.exit)
