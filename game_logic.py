#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
游戏核心逻辑模块
处理蛇体移动、碰撞检测、食物生成和胜利判定
"""

import pygame
import random
from enum import Enum

class Direction(Enum):
    """方向枚举"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class GameState(Enum):
    """游戏状态枚举"""
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    VICTORY = "victory"

class SnakeGame:
    """贪吃蛇游戏核心类"""
    
    def __init__(self, screen, skin_manager, score_manager):
        """初始化游戏"""
        self.screen = screen
        self.skin_manager = skin_manager
        self.score_manager = score_manager
        
        # 游戏区域设置
        self.grid_width = 20
        self.grid_height = 15
        self.cell_size = 30
        self.game_area_width = self.grid_width * self.cell_size
        self.game_area_height = self.grid_height * self.cell_size
        
        # 计算游戏区域在屏幕中的位置（居中）
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        self.game_area_x = (screen_width - self.game_area_width) // 2
        self.game_area_y = (screen_height - self.game_area_height) // 2 + 30  # 留出顶部状态栏空间
        
        # 初始化游戏状态
        self.reset_game()
        
        # 字体 - 使用系统中文字体
        self.font = self._get_chinese_font(24)
        self.big_font = self._get_chinese_font(48)
        
        # 游戏计时
        self.last_move_time = 0
        self.base_move_delay = 300  # 基础移动延迟（毫秒）- 减慢速度
        self.fast_move_delay = 100  # 加速时的移动延迟
        self.move_delay = self.base_move_delay
        
        # 按键状态跟踪
        self.keys_pressed = set()
    
    def _get_chinese_font(self, size):
        """获取支持中文的字体"""
        # 尝试加载系统中文字体，按优先级排序
        font_names = [
            'Microsoft YaHei',  # 微软雅黑
            'SimHei',           # 黑体
            'SimSun',           # 宋体
            'KaiTi',            # 楷体
            'FangSong',         # 仿宋
            'Arial Unicode MS', # Arial Unicode
            'DejaVu Sans',      # Linux常用字体
            'Noto Sans CJK SC'  # Google Noto字体
        ]
        
        for font_name in font_names:
            try:
                font = pygame.font.SysFont(font_name, size)
                # 测试字体是否支持中文
                test_surface = font.render('测试', True, (255, 255, 255))
                if test_surface.get_width() > 0:
                    return font
            except:
                continue
        
        # 如果所有字体都失败，使用默认字体
        return pygame.font.Font(None, size)
    
    def reset_game(self):
        """重置游戏状态"""
        # 蛇的初始位置（网格坐标）
        self.snake = [(self.grid_width // 2, self.grid_height // 2)]
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        
        # 食物位置列表（支持多个食物）
        self.foods = []
        self.max_foods = 20
        
        # 为本局游戏选择食物颜色
        self.select_food_color()
        
        self.generate_initial_foods()
        
        # 游戏状态
        self.state = GameState.PLAYING
        self.score = 0
        self.start_time = pygame.time.get_ticks()
    
    def generate_food(self):
        """生成单个食物位置"""
        while True:
            food_pos = (random.randint(0, self.grid_width - 1), 
                       random.randint(0, self.grid_height - 1))
            if food_pos not in self.snake and food_pos not in self.foods:
                return food_pos
    
    def generate_initial_foods(self):
        """生成初始食物（3-5个）"""
        self.foods = []
        initial_count = random.randint(3, 5)
        for _ in range(initial_count):
            self.foods.append(self.generate_food())
    
    def maintain_foods(self):
        """维持食物数量（确保场上有足够的食物）"""
        # 计算需要生成的食物数量
        target_count = min(self.max_foods, max(5, len(self.snake) // 10 + 3))
        
        while len(self.foods) < target_count:
            self.foods.append(self.generate_food())
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            # 添加按键到按下状态集合
            self.keys_pressed.add(event.key)
            
            if event.key in [pygame.K_ESCAPE, pygame.K_p]:
                if self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
                return None
            
            elif event.key == pygame.K_F11:
                return "toggle_fullscreen"
            
            # 方向控制
            elif self.state == GameState.PLAYING:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    if self.direction != Direction.DOWN:
                        self.next_direction = Direction.UP
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    if self.direction != Direction.UP:
                        self.next_direction = Direction.DOWN
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    if self.direction != Direction.RIGHT:
                        self.next_direction = Direction.LEFT
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    if self.direction != Direction.LEFT:
                        self.next_direction = Direction.RIGHT
            
            # 暂停菜单选项
            elif self.state == GameState.PAUSED:
                if event.key == pygame.K_RETURN:  # 继续游戏
                    self.state = GameState.PLAYING
                elif event.key == pygame.K_m:  # 返回主菜单
                    return "menu"
            
            # 游戏结束后的选项
            elif self.state in [GameState.GAME_OVER, GameState.VICTORY]:
                if event.key == pygame.K_RETURN:  # 重新开始
                    self.reset_game()
                elif event.key == pygame.K_m:  # 返回主菜单
                    return "menu"
        
        elif event.type == pygame.KEYUP:
            # 从按下状态集合中移除按键
            self.keys_pressed.discard(event.key)
        
        return None
    
    def update(self):
        """更新游戏状态"""
        if self.state != GameState.PLAYING:
            return None
        
        # 检查是否有方向键被按下（加速功能）
        direction_keys = {
            pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s,
            pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d
        }
        
        is_accelerating = bool(self.keys_pressed & direction_keys)
        self.move_delay = self.fast_move_delay if is_accelerating else self.base_move_delay
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            self.last_move_time = current_time
            
            # 更新方向
            self.direction = self.next_direction
            
            # 移动蛇头
            head_x, head_y = self.snake[0]
            dx, dy = self.direction.value
            new_head = (head_x + dx, head_y + dy)
            
            # 检查碰撞
            if self.check_collision(new_head):
                self.state = GameState.GAME_OVER
                self.score_manager.update_high_score(self.score)
                return "game_over"
            
            # 移动蛇
            self.snake.insert(0, new_head)
            
            # 检查是否吃到食物
            food_eaten = False
            for food_pos in self.foods[:]:
                if new_head == food_pos:
                    self.score += 10
                    self.foods.remove(food_pos)
                    food_eaten = True
                    break
            
            if food_eaten:
                # 维持食物数量
                self.maintain_foods()
                
                # 检查胜利条件（蛇长度达到300）
                if len(self.snake) >= 300:
                    self.state = GameState.VICTORY
                    self.score_manager.update_high_score(self.score)
                    return "victory"
            else:
                # 没吃到食物，移除尾部
                self.snake.pop()
        
        return None
    
    def check_collision(self, pos):
        """检查碰撞"""
        x, y = pos
        
        # 检查边界碰撞
        if x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height:
            return True
        
        # 检查自身碰撞
        if pos in self.snake:
            return True
        
        return False
    
    def grid_to_screen(self, grid_pos):
        """将网格坐标转换为屏幕坐标"""
        x, y = grid_pos
        screen_x = self.game_area_x + x * self.cell_size
        screen_y = self.game_area_y + y * self.cell_size
        return (screen_x, screen_y)
    
    def draw_game_area(self):
        """绘制游戏区域"""
        # 绘制游戏区域背景
        game_rect = pygame.Rect(self.game_area_x, self.game_area_y, 
                               self.game_area_width, self.game_area_height)
        pygame.draw.rect(self.screen, (15, 52, 96), game_rect)  # 深蓝色背景
        pygame.draw.rect(self.screen, (233, 69, 96), game_rect, 2)  # 金黄色边框
    
    def draw_snake(self):
        """绘制蛇"""
        current_skin = self.skin_manager.get_current_skin_info()
        
        for i, segment in enumerate(self.snake):
            screen_pos = self.grid_to_screen(segment)
            rect = pygame.Rect(screen_pos[0], screen_pos[1], self.cell_size, self.cell_size)
            
            if i == 0:  # 蛇头
                pygame.draw.rect(self.screen, current_skin['head_color'], rect)
            else:  # 蛇身
                pygame.draw.rect(self.screen, current_skin['body_color'], rect)
            
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # 边框
    
    def select_food_color(self):
        """为本局游戏选择食物颜色"""
        # 获取当前蛇皮肤颜色
        current_skin = self.skin_manager.get_current_skin_info()
        snake_colors = [current_skin['head_color'], current_skin['body_color']]
        
        # 背景颜色
        background_color = (15, 52, 96)  # 深蓝色背景
        
        # 候选食物颜色（鲜明且对比度高的颜色）
        candidate_colors = [
            (255, 69, 0),    # 橙红色
            (255, 20, 147),  # 深粉色
            (255, 215, 0),   # 金色
            (50, 205, 50),   # 酸橙绿
            (0, 191, 255),   # 深天蓝
            (138, 43, 226),  # 蓝紫色
            (255, 105, 180), # 热粉色
            (255, 140, 0),   # 深橙色
            (124, 252, 0),   # 草绿色
            (255, 0, 255),   # 洋红色
            (0, 255, 127),   # 春绿色
            (255, 99, 71),   # 番茄色
        ]
        
        # 过滤掉与蛇皮肤和背景相似的颜色
        valid_colors = []
        for color in candidate_colors:
            is_valid = True
            
            # 检查与蛇皮肤颜色的差异
            for snake_color in snake_colors:
                if self._color_similarity(color, snake_color) > 0.7:
                    is_valid = False
                    break
            
            # 检查与背景颜色的差异
            if is_valid and self._color_similarity(color, background_color) > 0.6:
                is_valid = False
            
            if is_valid:
                valid_colors.append(color)
        
        # 如果没有有效颜色，使用默认的高对比度颜色
        if not valid_colors:
            valid_colors = [(255, 69, 0), (255, 215, 0), (50, 205, 50)]
        
        # 随机选择一种颜色作为本局的食物颜色
        self.food_color = random.choice(valid_colors)
    
    def _color_similarity(self, color1, color2):
        """计算两个颜色的相似度（0-1，1表示完全相同）"""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        # 计算欧几里得距离
        distance = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        max_distance = (255 ** 2 * 3) ** 0.5  # 最大可能距离
        
        # 转换为相似度（距离越小，相似度越高）
        similarity = 1 - (distance / max_distance)
        return similarity
    
    def draw_food(self):
        """绘制所有食物（统一颜色）"""
        for food_pos in self.foods:
            screen_pos = self.grid_to_screen(food_pos)
            rect = pygame.Rect(screen_pos[0], screen_pos[1], self.cell_size, self.cell_size)
            
            # 使用本局选定的统一食物颜色
            pygame.draw.rect(self.screen, self.food_color, rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)  # 边框
    
    def draw_ui(self):
        """绘制用户界面"""
        # 状态栏背景
        status_rect = pygame.Rect(0, 0, self.screen.get_width(), 30)
        pygame.draw.rect(self.screen, (22, 22, 46), status_rect)
        
        # 分数
        score_text = self.font.render(f"分数: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 5))
        
        # 蛇长度
        length_text = self.font.render(f"长度: {len(self.snake)}/300", True, (255, 255, 255))
        self.screen.blit(length_text, (150, 5))
        
        # 食物数量
        food_count_text = self.font.render(f"食物: {len(self.foods)}", True, (255, 255, 255))
        self.screen.blit(food_count_text, (280, 5))
        
        # 进度条
        progress = len(self.snake) / 300
        progress_width = 180
        progress_rect = pygame.Rect(360, 8, progress_width, 14)
        pygame.draw.rect(self.screen, (60, 60, 60), progress_rect)
        if progress > 0:
            fill_rect = pygame.Rect(360, 8, int(progress_width * progress), 14)
            pygame.draw.rect(self.screen, (233, 69, 96), fill_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), progress_rect, 1)
        
        # 最高分
        high_score = self.score_manager.get_high_score()
        high_score_text = self.font.render(f"最高分: {high_score}", True, (255, 255, 255))
        self.screen.blit(high_score_text, (560, 5))
        
        # 速度指示器
        direction_keys = {
            pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s,
            pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d
        }
        is_accelerating = bool(self.keys_pressed & direction_keys)
        speed_text = "加速中" if is_accelerating else "正常速度"
        speed_color = (255, 100, 100) if is_accelerating else (100, 255, 100)
        speed_surface = self.font.render(speed_text, True, speed_color)
        self.screen.blit(speed_surface, (700, 5))
    
    def draw_pause_menu(self):
        """绘制暂停菜单"""
        # 半透明遮罩
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 暂停文字
        pause_text = self.big_font.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 50))
        self.screen.blit(pause_text, pause_rect)
        
        # 提示文字
        hint_text = self.font.render("按ESC继续 | 按M返回主菜单 | 按F11切换全屏", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 20))
        self.screen.blit(hint_text, hint_rect)
        
        # 加速提示
        speed_hint = self.font.render("长按方向键加速移动", True, (200, 200, 200))
        speed_rect = speed_hint.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 50))
        self.screen.blit(speed_hint, speed_rect)
    
    def draw_game_over(self):
        """绘制游戏结束界面"""
        # 半透明遮罩
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 游戏结束文字
        game_over_text = self.big_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        # 最终分数
        final_score_text = self.font.render(f"最终分数: {self.score}", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(final_score_text, final_score_rect)
        
        # 提示文字
        hint_text = self.font.render("按回车重新开始 | 按M返回主菜单", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 30))
        self.screen.blit(hint_text, hint_rect)
    
    def draw_victory(self):
        """绘制胜利界面"""
        # 彩色渐变背景
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(200)
        overlay.fill((50, 0, 100))
        self.screen.blit(overlay, (0, 0))
        
        # 胜利文字（带发光效果）
        victory_text = self.big_font.render("VICTORY!", True, (255, 215, 0))
        victory_rect = victory_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 50))
        self.screen.blit(victory_text, victory_rect)
        
        # 最终分数
        final_score_text = self.font.render(f"最终分数: {self.score}", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
        self.screen.blit(final_score_text, final_score_rect)
        
        # 游戏时间
        game_time = (pygame.time.get_ticks() - self.start_time) // 1000
        time_text = self.font.render(f"用时: {game_time}秒", True, (255, 255, 255))
        time_rect = time_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 25))
        self.screen.blit(time_text, time_rect)
        
        # 提示文字
        hint_text = self.font.render("按回车重新开始 | 按M返回主菜单", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 + 55))
        self.screen.blit(hint_text, hint_rect)
    
    def draw(self):
        """绘制游戏画面"""
        # 绘制游戏区域
        self.draw_game_area()
        
        # 绘制游戏元素
        if self.state != GameState.GAME_OVER:
            self.draw_food()  # 先绘制食物
            self.draw_snake()  # 后绘制蛇（确保蛇在食物上方）
        
        # 绘制UI
        self.draw_ui()
        
        # 根据游戏状态绘制覆盖层
        if self.state == GameState.PAUSED:
            self.draw_pause_menu()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.VICTORY:
            self.draw_victory()