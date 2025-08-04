#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Snake Game - Anime Edition
动漫风格贪吃蛇游戏主程序入口

作者: AI Assistant
版本: 1.0.0
描述: 具有动漫视觉风格的本地贪吃蛇游戏，支持暂停、皮肤选择与最高分记录
"""

import pygame
import sys
from ui_menu import MainMenu
from game_logic import SnakeGame
from skin_manager import SkinManager
from score_manager import ScoreManager

# 游戏常量
WIDTH = 800
HEIGHT = 600
FPS = 60
TITLE = "贪吃蛇 - Anime Edition"

class GameApp:
    """游戏主应用类"""
    
    def __init__(self):
        """初始化游戏应用"""
        pygame.init()
        
        # 设置窗口
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        
        # 设置窗口图标
        import os
        icon_path = os.path.join("assets", "icon.ico")
        try:
            if os.path.exists(icon_path) and icon_path.endswith('.ico'):
                # 对于.ico文件，我们跳过加载，因为pygame对.ico支持有限
                pass
            else:
                # 如果有其他格式的图标文件，可以在这里加载
                pass
        except Exception as e:
            print(f"无法加载图标: {e}")
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.fullscreen = False
        
        # 初始化管理器
        self.skin_manager = SkinManager()
        self.score_manager = ScoreManager()
        
        # 初始化菜单和游戏
        self.main_menu = MainMenu(self.screen, self.skin_manager, self.score_manager)
        self.snake_game = None
        
        # 导入皮肤选择菜单
        from ui_menu import SkinSelectionMenu
        self.skin_selection_menu = SkinSelectionMenu(self.screen, self.skin_manager)
        
        # 游戏状态
        self.state = "menu"  # menu, game, skin_selection
    
    def toggle_fullscreen(self):
        """切换全屏模式"""
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type in [pygame.KEYDOWN, pygame.KEYUP]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                
                # 根据当前状态处理按键
                if self.state == "menu":
                    if event.type == pygame.KEYDOWN:  # 菜单只处理按下事件
                        result = self.main_menu.handle_event(event)
                        if result == "start_game":
                            self.start_game()
                        elif result == "skin_selection":
                            self.state = "skin_selection"
                        elif result == "quit":
                            self.running = False
                elif self.state == "skin_selection":
                    if event.type == pygame.KEYDOWN:  # 皮肤选择只处理按下事件
                        result = self.skin_selection_menu.handle_event(event)
                        if result == "back_to_menu" or result == "skin_selected":
                            self.state = "menu"
                
                elif self.state == "game" and self.snake_game:
                    # 游戏状态需要处理按下和释放事件
                    result = self.snake_game.handle_event(event)
                    if result == "menu":
                        self.state = "menu"
                        self.snake_game = None
                    elif result == "toggle_fullscreen":
                        self.toggle_fullscreen()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "menu":
                    result = self.main_menu.handle_event(event)
                    if result == "start_game":
                        self.start_game()
                    elif result == "skin_selection":
                        self.state = "skin_selection"
                    elif result == "quit":
                        self.running = False
                elif self.state == "skin_selection":
                    result = self.skin_selection_menu.handle_event(event)
                    if result == "back_to_menu" or result == "skin_selected":
                        self.state = "menu"
    
    def start_game(self):
        """开始游戏"""
        self.snake_game = SnakeGame(self.screen, self.skin_manager, self.score_manager)
        self.state = "game"
    
    def update(self):
        """更新游戏状态"""
        if self.state == "game" and self.snake_game:
            result = self.snake_game.update()
            if result == "game_over" or result == "victory":
                self.state = "menu"
                self.snake_game = None
    
    def draw(self):
        """绘制游戏画面"""
        self.screen.fill((26, 26, 46))  # 深蓝色背景
        
        if self.state == "menu":
            self.main_menu.draw()
        elif self.state == "game" and self.snake_game:
            self.snake_game.draw()
        elif self.state == "skin_selection":
            # 绘制皮肤选择界面
            self.skin_selection_menu.draw()
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    """主函数"""
    app = GameApp()
    app.run()

if __name__ == "__main__":
    main()