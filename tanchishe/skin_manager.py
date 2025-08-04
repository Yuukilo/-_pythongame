#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
皮肤管理器模块
处理皮肤加载与切换功能
"""

import pygame
import json
import os

class SkinManager:
    """皮肤管理器类"""
    
    def __init__(self):
        """初始化皮肤管理器"""
        self.config_file = "config.json"
        
        # 定义可用皮肤
        self.available_skins = {
            "classic": {
                "name": "经典蛇",
                "snake_head_color": (0, 255, 0),
                "snake_body_color": (0, 200, 0),
                "food_color": (255, 0, 0),
                "description": "传统的绿色贪吃蛇"
            },
            "neko": {
                "name": "猫耳蛇",
                "snake_head_color": (255, 150, 200),
                "snake_body_color": (255, 100, 150),
                "food_color": (255, 200, 100),
                "description": "可爱的粉色猫耳风格"
            },
            "dragon": {
                "name": "龙形蛇",
                "snake_head_color": (255, 215, 0),
                "snake_body_color": (255, 165, 0),
                "food_color": (255, 0, 255),
                "description": "威武的金色龙形风格"
            }
        }
        
        # 当前皮肤
        self.current_skin = "classic"
        
        # 加载配置
        self.load_config()
        
        # 皮肤资源缓存
        self.skin_cache = {}
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.current_skin = config.get('current_skin', 'classic')
                    
                    # 验证皮肤是否存在
                    if self.current_skin not in self.available_skins:
                        self.current_skin = 'classic'
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            self.current_skin = 'classic'
    
    def save_config(self):
        """保存配置文件"""
        try:
            config = {
                'current_skin': self.current_skin,
                'version': '1.0.0'
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get_current_skin(self):
        """获取当前皮肤名称"""
        return self.current_skin
    
    def get_current_skin_info(self):
        """获取当前皮肤信息"""
        skin_info = self.available_skins.get(self.current_skin, self.available_skins['classic'])
        # 返回标准化的皮肤信息格式
        return {
            'name': skin_info['name'],
            'head_color': skin_info['snake_head_color'],
            'body_color': skin_info['snake_body_color'],
            'food_color': skin_info['food_color'],
            'description': skin_info['description']
        }
    
    def set_current_skin(self, skin_name):
        """设置当前皮肤"""
        if skin_name in self.available_skins:
            self.current_skin = skin_name
            self.save_config()
            return True
        return False
    
    def get_available_skins(self):
        """获取所有可用皮肤列表"""
        return list(self.available_skins.keys())
    
    def get_skin_info(self, skin_name):
        """获取指定皮肤信息"""
        return self.available_skins.get(skin_name)
    
    def get_snake_head_color(self, skin_name=None):
        """获取蛇头颜色"""
        skin_name = skin_name or self.current_skin
        skin_info = self.available_skins.get(skin_name, self.available_skins['classic'])
        return skin_info['snake_head_color']
    
    def get_snake_body_color(self, skin_name=None):
        """获取蛇身颜色"""
        skin_name = skin_name or self.current_skin
        skin_info = self.available_skins.get(skin_name, self.available_skins['classic'])
        return skin_info['snake_body_color']
    
    def get_food_color(self, skin_name=None):
        """获取食物颜色"""
        skin_name = skin_name or self.current_skin
        skin_info = self.available_skins.get(skin_name, self.available_skins['classic'])
        return skin_info['food_color']
    
    def load_skin_sprite(self, skin_name, sprite_type):
        """加载皮肤精灵图片"""
        cache_key = f"{skin_name}_{sprite_type}"
        
        # 检查缓存
        if cache_key in self.skin_cache:
            return self.skin_cache[cache_key]
        
        # 尝试加载图片文件
        sprite_path = f"assets/sprites/{skin_name}_{sprite_type}.png"
        
        try:
            if os.path.exists(sprite_path):
                sprite = pygame.image.load(sprite_path).convert_alpha()
                self.skin_cache[cache_key] = sprite
                return sprite
        except Exception as e:
            print(f"加载皮肤图片失败 {sprite_path}: {e}")
        
        # 如果图片加载失败，返回None（使用颜色绘制）
        return None
    
    def draw_snake_segment(self, screen, rect, is_head=False, skin_name=None):
        """绘制蛇身段"""
        skin_name = skin_name or self.current_skin
        
        # 尝试加载精灵图片
        sprite_type = "head" if is_head else "body"
        sprite = self.load_skin_sprite(skin_name, sprite_type)
        
        if sprite:
            # 缩放精灵到合适大小
            scaled_sprite = pygame.transform.scale(sprite, (rect.width, rect.height))
            screen.blit(scaled_sprite, rect)
        else:
            # 使用颜色绘制
            if is_head:
                color = self.get_snake_head_color(skin_name)
            else:
                color = self.get_snake_body_color(skin_name)
            
            pygame.draw.rect(screen, color, rect)
            
            # 添加一些装饰效果
            if skin_name == "neko":
                # 猫耳蛇：添加可爱的点点
                if is_head:
                    # 绘制眼睛
                    eye_size = 3
                    left_eye = (rect.x + rect.width//3, rect.y + rect.height//3)
                    right_eye = (rect.x + 2*rect.width//3, rect.y + rect.height//3)
                    pygame.draw.circle(screen, (0, 0, 0), left_eye, eye_size)
                    pygame.draw.circle(screen, (0, 0, 0), right_eye, eye_size)
                else:
                    # 身体上的小点
                    dot_color = (255, 255, 255)
                    center = rect.center
                    pygame.draw.circle(screen, dot_color, center, 2)
            
            elif skin_name == "dragon":
                # 龙形蛇：添加鳞片效果
                scale_color = (255, 255, 0)
                if is_head:
                    # 龙头装饰
                    pygame.draw.circle(screen, scale_color, rect.center, rect.width//4)
                else:
                    # 鳞片纹理
                    for i in range(0, rect.width, 6):
                        for j in range(0, rect.height, 6):
                            if (i + j) % 12 == 0:
                                pygame.draw.circle(screen, scale_color, 
                                                 (rect.x + i, rect.y + j), 1)
        
        # 绘制边框
        pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    
    def draw_food(self, screen, rect, skin_name=None):
        """绘制食物"""
        skin_name = skin_name or self.current_skin
        
        # 尝试加载食物精灵
        sprite = self.load_skin_sprite(skin_name, "food")
        
        if sprite:
            scaled_sprite = pygame.transform.scale(sprite, (rect.width, rect.height))
            screen.blit(scaled_sprite, rect)
        else:
            # 使用颜色和形状绘制
            food_color = self.get_food_color(skin_name)
            
            if skin_name == "classic":
                # 经典：简单的方块
                pygame.draw.rect(screen, food_color, rect)
            elif skin_name == "neko":
                # 猫耳：心形食物
                center = rect.center
                radius = rect.width // 3
                # 简化的心形（两个圆加一个三角形）
                pygame.draw.circle(screen, food_color, 
                                 (center[0] - radius//2, center[1] - radius//2), radius//2)
                pygame.draw.circle(screen, food_color, 
                                 (center[0] + radius//2, center[1] - radius//2), radius//2)
                points = [(center[0], center[1] + radius//2),
                         (center[0] - radius, center[1]),
                         (center[0] + radius, center[1])]
                pygame.draw.polygon(screen, food_color, points)
            elif skin_name == "dragon":
                # 龙形：宝石形状
                center = rect.center
                size = rect.width // 2
                points = [
                    (center[0], center[1] - size),  # 上
                    (center[0] + size, center[1]),  # 右
                    (center[0], center[1] + size),  # 下
                    (center[0] - size, center[1])   # 左
                ]
                pygame.draw.polygon(screen, food_color, points)
        
        # 绘制边框
        pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    
    def get_skin_preview_color(self, skin_name):
        """获取皮肤预览颜色（用于菜单显示）"""
        skin_info = self.available_skins.get(skin_name)
        if skin_info:
            return skin_info['snake_head_color']
        return (128, 128, 128)
    
    def create_skin_preview(self, skin_name, size=(64, 64)):
        """创建皮肤预览图"""
        surface = pygame.Surface(size)
        surface.fill((50, 50, 70))  # 背景色
        
        # 绘制简化的蛇头预览
        head_rect = pygame.Rect(size[0]//4, size[1]//4, size[0]//2, size[1]//2)
        head_color = self.get_snake_head_color(skin_name)
        
        pygame.draw.rect(surface, head_color, head_rect)
        pygame.draw.rect(surface, (255, 255, 255), head_rect, 2)
        
        # 添加简单的眼睛
        eye_size = 2
        left_eye = (head_rect.x + head_rect.width//3, head_rect.y + head_rect.height//3)
        right_eye = (head_rect.x + 2*head_rect.width//3, head_rect.y + head_rect.height//3)
        pygame.draw.circle(surface, (0, 0, 0), left_eye, eye_size)
        pygame.draw.circle(surface, (0, 0, 0), right_eye, eye_size)
        
        return surface