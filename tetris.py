import pygame
import random
import os

# 初始化 Pygame
pygame.init()
pygame.font.init()

# 设置游戏窗口
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
BLOCK_SIZE = 30

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('俄罗斯方块')

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
COLORS = [
    (0, 0, 0),
    (255, 0, 0),    # 红色
    (0, 255, 0),    # 绿色
    (0, 0, 255),    # 蓝色
    (255, 255, 0),  # 黄色
    (255, 165, 0),  # 橙色
    (0, 255, 255),  # 青色
    (255, 0, 255)   # 紫色
]

# 游戏区域的大小（以方块数量计）
GRID_WIDTH = 10
GRID_HEIGHT = 20

# 计算游戏区域的实际像素大小
GAME_WIDTH = GRID_WIDTH * BLOCK_SIZE
GAME_HEIGHT = GRID_HEIGHT * BLOCK_SIZE

# 计算游戏区域的起始位置（居中显示）
GAME_X = (WINDOW_WIDTH - GAME_WIDTH) // 2
GAME_Y = (WINDOW_HEIGHT - GAME_HEIGHT) // 2

# 创建游戏网格
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

class Tetromino:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.randint(1, len(COLORS)-1)
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        
    def draw(self):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    pygame.draw.rect(screen, COLORS[self.color],
                                   (GAME_X + (self.x + j) * BLOCK_SIZE,
                                    GAME_Y + (self.y + i) * BLOCK_SIZE,
                                    BLOCK_SIZE - 1, BLOCK_SIZE - 1))

    def check_collision(self, grid):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    if (self.y + i >= GRID_HEIGHT or  # 触底
                        self.x + j < 0 or  # 触左边界
                        self.x + j >= GRID_WIDTH or  # 触右边界
                        grid[self.y + i][self.x + j]):  # 碰到其他方块
                        return True
        return False

    def lock(self, grid):
        for i in range(len(self.shape)):
            for j in range(len(self.shape[0])):
                if self.shape[i][j]:
                    grid[self.y + i][self.x + j] = self.color

    def rotate(self):
        # 保存原始形状以便检测碰撞
        old_shape = self.shape
        # 获取矩阵的行数和列数
        rows = len(self.shape)
        cols = len(self.shape[0])
        # 创建新的旋转后的形状
        rotated = [[self.shape[rows-1-j][i] for j in range(rows)] for i in range(cols)]
        self.shape = rotated
        # 如果旋转后发生碰撞，则恢复原来的形状
        if self.check_collision(grid):
            self.shape = old_shape

def draw_grid():
    # 绘制游戏区域边框
    pygame.draw.rect(screen, WHITE, (GAME_X-2, GAME_Y-2, GAME_WIDTH+4, GAME_HEIGHT+4), 2)
    
    # 绘制网格线
    for x in range(GRID_WIDTH + 1):
        pygame.draw.line(screen, GRAY, 
                        (GAME_X + x * BLOCK_SIZE, GAME_Y),
                        (GAME_X + x * BLOCK_SIZE, GAME_Y + GAME_HEIGHT))
    
    for y in range(GRID_HEIGHT + 1):
        pygame.draw.line(screen, GRAY,
                        (GAME_X, GAME_Y + y * BLOCK_SIZE),
                        (GAME_X + GAME_WIDTH, GAME_Y + y * BLOCK_SIZE))

def remove_full_lines(grid):
    global score
    full_lines = 0
    for i in range(GRID_HEIGHT):
        if all(grid[i]):
            full_lines += 1
            for y in range(i, 0, -1):
                grid[y] = grid[y-1][:]
            grid[0] = [0] * GRID_WIDTH
    
    # 根据消除的行数计算得分
    if full_lines == 1:
        score += 100
    elif full_lines == 2:
        score += 300
    elif full_lines == 3:
        score += 500
    elif full_lines == 4:
        score += 800
    
    return full_lines

def draw_blocks(grid):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if grid[i][j]:
                pygame.draw.rect(screen, COLORS[grid[i][j]],
                               (GAME_X + j * BLOCK_SIZE,
                                GAME_Y + i * BLOCK_SIZE,
                                BLOCK_SIZE - 1, BLOCK_SIZE - 1))

# 在游戏主循环前添加
current_piece = Tetromino()
fall_time = 0
fall_speed = 1000  # 每秒移动一格
last_fall_time = pygame.time.get_ticks()

# 在颜色定义后添加
try:
    # 尝试使用系统默认字体
    FONT = pygame.font.SysFont('Arial', 36)
except:
    # 如果失败，使用默认字体
    FONT = pygame.font.Font(None, 36)
score = 0

# 添加分数显示函数
def draw_score():
    # 1. 首先画一个醒目的红色背景框
    score_box_rect = pygame.draw.rect(screen, RED, 
                                    (GAME_X + GAME_WIDTH + 20, # x坐标
                                     GAME_Y, # y坐标
                                     150, # 宽度
                                     50), # 高度
                                    0)  # 填充矩形
    
    # 2. 直接在屏幕上绘制分数数字
    score_str = str(score)
    # 使用更大的字体
    font = pygame.font.Font(None, 48)
    text = font.render(score_str, True, WHITE)
    # 将分数放在红色框中间
    text_rect = text.get_rect(center=score_box_rect.center)
    screen.blit(text, text_rect)

# 修改游戏主循环
running = True
while running:
    current_time = pygame.time.get_ticks()
    delta_time = current_time - last_fall_time
    
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                current_piece.x -= 1
                if current_piece.check_collision(grid):
                    current_piece.x += 1
            elif event.key == pygame.K_RIGHT:
                current_piece.x += 1
                if current_piece.check_collision(grid):
                    current_piece.x -= 1
            elif event.key == pygame.K_DOWN:
                current_piece.y += 1
                if current_piece.check_collision(grid):
                    current_piece.y -= 1
            elif event.key == pygame.K_UP:
                current_piece.rotate()
    
    # 自动下落
    if delta_time > fall_speed:
        current_piece.y += 1
        if current_piece.check_collision(grid):
            current_piece.y -= 1
            current_piece.lock(grid)
            remove_full_lines(grid)
            current_piece = Tetromino()
        last_fall_time = current_time
    
    # 填充背景色
    screen.fill(BLACK)
    
    # 绘制网格
    draw_grid()
    
    # 绘制已固定的方块
    draw_blocks(grid)
    
    # 绘制当前方块
    current_piece.draw()
    
    # 确保在最后绘制分数
    draw_score()
    
    # 更新显示
    pygame.display.flip()

# 退出游戏
pygame.quit()
