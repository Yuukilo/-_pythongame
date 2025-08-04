#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UI菜单模块
处理主菜单和暂停菜单界面
"""

import pygame

class Button:
    """按钮类"""
    
    def __init__(self, x, y, width, height, text, font, color=(100, 100, 100), hover_color=(150, 150, 150), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def draw(self, screen):
        """绘制按钮"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # 绘制文字
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class MainMenu:
    """主菜单类"""
    
    def __init__(self, screen, skin_manager, score_manager):
        self.screen = screen
        self.skin_manager = skin_manager
        self.score_manager = score_manager
        
        # 字体 - 使用系统中文字体
        self.title_font = self._get_chinese_font(48)
        self.button_font = self._get_chinese_font(24)
        self.info_font = self._get_chinese_font(20)
        
        # 按钮设置 - 响应式布局
        self.buttons = {}  # 初始化空字典
        self.update_button_layout()
        
        # 背景颜色
        self.bg_color = (26, 26, 46)
    
    def update_button_layout(self):
        """更新按钮布局以适应不同屏幕尺寸"""
        button_width = 200
        button_height = 50
        button_spacing = 20
        
        # 根据屏幕高度调整起始位置
        screen_height = self.screen.get_height()
        start_y = max(300, screen_height // 2 - 50)
        center_x = self.screen.get_width() // 2 - button_width // 2
        
        # 创建按钮
        self.buttons = {
            "start": Button(center_x, start_y, button_width, button_height, 
                           "开始游戏", self.button_font, 
                           (233, 69, 96), (255, 100, 120)),
            "skin": Button(center_x, start_y + button_height + button_spacing, 
                          button_width, button_height, 
                          "选择皮肤", self.button_font,
                          (15, 52, 96), (30, 70, 120)),
            "quit": Button(center_x, start_y + 2 * (button_height + button_spacing), 
                          button_width, button_height, 
                          "退出游戏", self.button_font,
                          (100, 100, 100), (150, 150, 150))
        }
    
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
    
    def handle_event(self, event):
        """处理事件"""
        for button_name, button in self.buttons.items():
            if button.handle_event(event):
                if button_name == "start":
                    return "start_game"
                elif button_name == "skin":
                    return "skin_selection"
                elif button_name == "quit":
                    return "quit"
        
        # 处理键盘事件
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return "start_game"
            elif event.key == pygame.K_s:
                return "skin_selection"
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                return "quit"
        
        return None
    
    def draw_background(self):
        """绘制背景"""
        # 渐变背景
        for y in range(self.screen.get_height()):
            ratio = y / self.screen.get_height()
            r = int(26 + (22 - 26) * ratio)
            g = int(26 + (22 - 26) * ratio)
            b = int(46 + (62 - 46) * ratio)
            color = (r, g, b)
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))
    
    def draw_title(self):
        """绘制标题"""
        title_text = "贪吃蛇 - Anime Edition"
        title_surface = self.title_font.render(title_text, True, (255, 215, 0))  # 金黄色
        title_rect = title_surface.get_rect(center=(self.screen.get_width()//2, 150))
        
        # 添加阴影效果
        shadow_surface = self.title_font.render(title_text, True, (50, 50, 50))
        shadow_rect = shadow_surface.get_rect(center=(self.screen.get_width()//2 + 2, 152))
        self.screen.blit(shadow_surface, shadow_rect)
        self.screen.blit(title_surface, title_rect)
    
    def draw_info(self):
        """绘制信息"""
        # 最高分
        high_score = self.score_manager.get_high_score()
        high_score_text = f"最高分: {high_score}"
        high_score_surface = self.info_font.render(high_score_text, True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(self.screen.get_width()//2, 220))
        self.screen.blit(high_score_surface, high_score_rect)
        
        # 当前皮肤
        current_skin = self.skin_manager.get_current_skin()
        skin_text = f"当前皮肤: {current_skin}"
        skin_surface = self.info_font.render(skin_text, True, (200, 200, 200))
        skin_rect = skin_surface.get_rect(center=(self.screen.get_width()//2, 245))
        self.screen.blit(skin_surface, skin_rect)
        
        # 控制说明
        controls = [
            "控制: 方向键 或 WASD",
            "暂停: ESC 或 P",
            "全屏: F11",
            "目标: 蛇长度达到300获胜"
        ]
        
        start_y = self.screen.get_height() - 120
        for i, control in enumerate(controls):
            control_surface = self.info_font.render(control, True, (150, 150, 150))
            control_rect = control_surface.get_rect(center=(self.screen.get_width()//2, start_y + i * 20))
            self.screen.blit(control_surface, control_rect)
    
    def draw(self):
        """绘制主菜单"""
        # 更新按钮布局以适应当前屏幕尺寸
        self.update_button_layout()
        
        self.draw_background()
        self.draw_title()
        self.draw_info()
        
        # 绘制按钮
        for button in self.buttons.values():
            button.draw(self.screen)

class PauseMenu:
    """暂停菜单类"""
    
    def __init__(self, screen):
        self.screen = screen
        self.font = self._get_chinese_font(36)
        self.button_font = self._get_chinese_font(24)
        
        # 按钮设置
        button_width = 180
        button_height = 40
        button_spacing = 15
        start_y = 320
        center_x = screen.get_width() // 2 - button_width // 2
        
        # 创建按钮
        self.buttons = {
            "continue": Button(center_x, start_y, button_width, button_height,
                              "继续游戏", self.button_font,
                              (0, 150, 0), (0, 200, 0)),
            "fullscreen": Button(center_x, start_y + button_height + button_spacing,
                                button_width, button_height,
                                "切换全屏", self.button_font,
                                (100, 100, 150), (120, 120, 180)),
            "menu": Button(center_x, start_y + 2 * (button_height + button_spacing),
                          button_width, button_height,
                          "返回主菜单", self.button_font,
                          (150, 100, 0), (180, 120, 0)),
            "quit": Button(center_x, start_y + 3 * (button_height + button_spacing),
                          button_width, button_height,
                          "退出游戏", self.button_font,
                          (150, 0, 0), (200, 0, 0))
        }
    
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
    
    def handle_event(self, event):
        """处理事件"""
        for button_name, button in self.buttons.items():
            if button.handle_event(event):
                return button_name
        
        return None
    
    def draw(self):
        """绘制暂停菜单"""
        # 半透明遮罩
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # 暂停标题
        pause_text = self.font.render("游戏暂停", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.screen.get_width()//2, 250))
        self.screen.blit(pause_text, pause_rect)
        
        # 绘制按钮
        for button in self.buttons.values():
            button.draw(self.screen)

class SkinSelectionMenu:
    """皮肤选择菜单类"""
    
    def __init__(self, screen, skin_manager):
        self.screen = screen
        self.skin_manager = skin_manager
        self.font = self._get_chinese_font(36)
        self.info_font = self._get_chinese_font(20)
        
        # 皮肤信息
        self.skins = [
            {"name": "classic", "display_name": "经典蛇", "color": (0, 255, 0)},
            {"name": "neko", "display_name": "猫耳蛇", "color": (255, 100, 150)},
            {"name": "dragon", "display_name": "龙形蛇", "color": (255, 215, 0)}
        ]
        
        self.selected_skin = 0
    
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
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.selected_skin = (self.selected_skin - 1) % len(self.skins)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.selected_skin = (self.selected_skin + 1) % len(self.skins)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # 应用选择的皮肤
                selected_skin_name = self.skins[self.selected_skin]["name"]
                self.skin_manager.set_current_skin(selected_skin_name)
                return "skin_selected"
            elif event.key == pygame.K_ESCAPE:
                return "back_to_menu"
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检查点击的皮肤卡片
            mouse_x, mouse_y = event.pos
            card_width = 150
            card_height = 200
            spacing = 50
            start_x = (self.screen.get_width() - (len(self.skins) * card_width + (len(self.skins) - 1) * spacing)) // 2
            
            for i, skin in enumerate(self.skins):
                card_x = start_x + i * (card_width + spacing)
                card_y = 250
                card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
                
                if card_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_skin = i
                    selected_skin_name = self.skins[self.selected_skin]["name"]
                    self.skin_manager.set_current_skin(selected_skin_name)
                    return "skin_selected"
        
        return None
    
    def draw(self):
        """绘制皮肤选择菜单"""
        # 背景
        self.screen.fill((26, 26, 46))
        
        # 标题
        title_text = self.font.render("选择皮肤", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width()//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # 皮肤卡片
        card_width = 150
        card_height = 200
        spacing = 50
        start_x = (self.screen.get_width() - (len(self.skins) * card_width + (len(self.skins) - 1) * spacing)) // 2
        
        current_skin = self.skin_manager.get_current_skin()
        
        for i, skin in enumerate(self.skins):
            card_x = start_x + i * (card_width + spacing)
            card_y = 250
            
            # 卡片背景
            card_rect = pygame.Rect(card_x, card_y, card_width, card_height)
            
            # 选中状态或当前使用的皮肤 - 增强边框效果
            if i == self.selected_skin:
                # 选中状态 - 金色发光边框
                pygame.draw.rect(self.screen, (255, 215, 0), card_rect, 5)  # 更粗的金色边框
                # 添加内层边框增强效果
                inner_rect = pygame.Rect(card_x + 3, card_y + 3, card_width - 6, card_height - 6)
                pygame.draw.rect(self.screen, (255, 255, 100), inner_rect, 2)
            elif skin["name"] == current_skin:
                pygame.draw.rect(self.screen, (0, 255, 0), card_rect, 3)  # 绿色边框表示当前使用
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), card_rect, 1)
            
            pygame.draw.rect(self.screen, (50, 50, 70), card_rect)
            
            # 皮肤预览（简单的颜色块）
            preview_size = 80
            preview_x = card_x + (card_width - preview_size) // 2
            preview_y = card_y + 30
            preview_rect = pygame.Rect(preview_x, preview_y, preview_size, preview_size)
            pygame.draw.rect(self.screen, skin["color"], preview_rect)
            pygame.draw.rect(self.screen, (255, 255, 255), preview_rect, 2)
            
            # 皮肤名称
            name_surface = self.info_font.render(skin["display_name"], True, (255, 255, 255))
            name_rect = name_surface.get_rect(center=(card_x + card_width//2, card_y + 140))
            self.screen.blit(name_surface, name_rect)
            
            # 状态文字
            if skin["name"] == current_skin:
                status_surface = self.info_font.render("当前使用", True, (0, 255, 0))
                status_rect = status_surface.get_rect(center=(card_x + card_width//2, card_y + 165))
                self.screen.blit(status_surface, status_rect)
        
        # 操作提示
        hint_text = "使用方向键选择，回车确认，ESC返回"
        hint_surface = self.info_font.render(hint_text, True, (200, 200, 200))
        hint_rect = hint_surface.get_rect(center=(self.screen.get_width()//2, 500))
        self.screen.blit(hint_surface, hint_rect)