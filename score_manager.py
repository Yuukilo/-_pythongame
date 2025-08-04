#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分数管理器模块
处理最高分记录的读写和管理
"""

import json
import os
from datetime import datetime

class ScoreManager:
    """分数管理器类"""
    
    def __init__(self, config_file="config.json"):
        """初始化分数管理器"""
        self.config_file = config_file
        self.high_score = 0
        self.score_history = []
        self.load_scores()
    
    def load_scores(self):
        """从配置文件加载分数数据"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.high_score = config.get('high_score', 0)
                    self.score_history = config.get('score_history', [])
                    
                    # 确保分数历史不超过100条记录
                    if len(self.score_history) > 100:
                        self.score_history = self.score_history[-100:]
            else:
                # 如果配置文件不存在，创建默认配置
                self.create_default_config()
        except Exception as e:
            print(f"加载分数数据失败: {e}")
            self.high_score = 0
            self.score_history = []
            self.create_default_config()
    
    def create_default_config(self):
        """创建默认配置文件"""
        default_config = {
            'high_score': 0,
            'score_history': [],
            'current_skin': 'classic',
            'version': '1.0.0',
            'settings': {
                'sound_enabled': True,
                'fullscreen': False,
                'difficulty': 'normal'
            }
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"创建默认配置文件失败: {e}")
    
    def save_scores(self):
        """保存分数数据到配置文件"""
        try:
            # 读取现有配置
            config = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # 更新分数相关数据
            config['high_score'] = self.high_score
            config['score_history'] = self.score_history
            config['last_updated'] = datetime.now().isoformat()
            
            # 保存配置
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"保存分数数据失败: {e}")
    
    def get_high_score(self):
        """获取最高分"""
        return self.high_score
    
    def update_high_score(self, new_score):
        """更新最高分"""
        is_new_record = False
        
        if new_score > self.high_score:
            self.high_score = new_score
            is_new_record = True
        
        # 添加到历史记录
        score_entry = {
            'score': new_score,
            'timestamp': datetime.now().isoformat(),
            'is_record': is_new_record
        }
        
        self.score_history.append(score_entry)
        
        # 保持历史记录在合理范围内
        if len(self.score_history) > 100:
            self.score_history = self.score_history[-100:]
        
        # 保存数据
        self.save_scores()
        
        return is_new_record
    
    def get_score_history(self, limit=10):
        """获取分数历史记录"""
        # 返回最近的记录，按时间倒序
        return sorted(self.score_history, 
                     key=lambda x: x['timestamp'], 
                     reverse=True)[:limit]
    
    def get_average_score(self):
        """获取平均分"""
        if not self.score_history:
            return 0
        
        total_score = sum(entry['score'] for entry in self.score_history)
        return total_score / len(self.score_history)
    
    def get_total_games(self):
        """获取总游戏次数"""
        return len(self.score_history)
    
    def get_records_count(self):
        """获取破纪录次数"""
        return sum(1 for entry in self.score_history if entry.get('is_record', False))
    
    def reset_scores(self):
        """重置所有分数数据"""
        self.high_score = 0
        self.score_history = []
        self.save_scores()
    
    def export_scores(self, filename="score_export.json"):
        """导出分数数据"""
        try:
            export_data = {
                'high_score': self.high_score,
                'score_history': self.score_history,
                'export_date': datetime.now().isoformat(),
                'total_games': self.get_total_games(),
                'average_score': self.get_average_score(),
                'records_count': self.get_records_count()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"导出分数数据失败: {e}")
            return False
    
    def import_scores(self, filename):
        """导入分数数据"""
        try:
            if not os.path.exists(filename):
                return False
            
            with open(filename, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            # 验证数据格式
            if 'high_score' in import_data and 'score_history' in import_data:
                self.high_score = max(self.high_score, import_data['high_score'])
                
                # 合并历史记录
                imported_history = import_data['score_history']
                self.score_history.extend(imported_history)
                
                # 去重并排序
                seen = set()
                unique_history = []
                for entry in self.score_history:
                    entry_key = (entry['score'], entry['timestamp'])
                    if entry_key not in seen:
                        seen.add(entry_key)
                        unique_history.append(entry)
                
                self.score_history = sorted(unique_history, 
                                           key=lambda x: x['timestamp'])
                
                # 保持记录数量限制
                if len(self.score_history) > 100:
                    self.score_history = self.score_history[-100:]
                
                self.save_scores()
                return True
            
        except Exception as e:
            print(f"导入分数数据失败: {e}")
        
        return False
    
    def get_statistics(self):
        """获取统计信息"""
        if not self.score_history:
            return {
                'total_games': 0,
                'high_score': 0,
                'average_score': 0,
                'records_count': 0,
                'last_played': None
            }
        
        # 计算统计数据
        scores = [entry['score'] for entry in self.score_history]
        last_entry = max(self.score_history, key=lambda x: x['timestamp'])
        
        return {
            'total_games': len(self.score_history),
            'high_score': self.high_score,
            'average_score': round(sum(scores) / len(scores), 1),
            'lowest_score': min(scores),
            'records_count': self.get_records_count(),
            'last_played': last_entry['timestamp'],
            'score_range': max(scores) - min(scores) if scores else 0
        }
    
    def is_high_score(self, score):
        """检查是否为最高分"""
        return score > self.high_score
    
    def get_score_rank(self, score):
        """获取分数排名（在历史记录中的位置）"""
        if not self.score_history:
            return 1
        
        scores = [entry['score'] for entry in self.score_history]
        scores.append(score)
        scores.sort(reverse=True)
        
        return scores.index(score) + 1
    
    def get_recent_improvement(self, limit=5):
        """获取最近的进步情况"""
        if len(self.score_history) < 2:
            return None
        
        recent_scores = [entry['score'] for entry in self.score_history[-limit:]]
        
        if len(recent_scores) < 2:
            return None
        
        improvement = recent_scores[-1] - recent_scores[0]
        average_recent = sum(recent_scores) / len(recent_scores)
        
        return {
            'improvement': improvement,
            'average_recent': round(average_recent, 1),
            'trend': 'improving' if improvement > 0 else 'declining' if improvement < 0 else 'stable'
        }