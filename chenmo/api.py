"""
chenmo API 客户端
处理与AI服务的交互，用于增强生成内容
"""

import requests
import json
from typing import Dict, Any, Optional
from pathlib import Path

from .config import get_api_config


class APIClient:
    """
    API客户端，用于与AI服务交互
    """
    
    def __init__(self, api_url: str = None, api_key: str = None, model: str = None):
        """
        初始化API客户端
        :param api_url: API端点URL
        :param api_key: API密钥
        :param model: 使用的模型名称
        """
        # 如果提供了参数，则使用参数；否则从配置获取
        if api_url and api_key and model:
            self.api_url = api_url
            self.api_key = api_key
            self.model = model
        else:
            # 获取配置
            config = get_api_config()
            if config:
                self.api_url = config.get('api_url', 'https://api.openai.com/v1/chat/completions')
                self.api_key = config.get('api_key', '')
                self.model = config.get('model', 'gpt-3.5-turbo')
            else:
                # 如果配置获取失败，使用默认值
                self.api_url = 'https://api.openai.com/v1/chat/completions'
                self.api_key = ''
                self.model = 'gpt-3.5-turbo'
        
        # 设置请求头
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}' if self.api_key else ''
        }
        
        # 验证配置
        if not self.api_key:
            print("警告: 未设置API密钥，AI增强功能将不可用")
    
    def generate_content(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Optional[str]:
        """
        生成内容
        :param prompt: 提示词
        :param max_tokens: 最大生成token数
        :param temperature: 生成温度
        :return: 生成的内容
        """
        if not self.api_key:
            return None
            
        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
            
        except requests.exceptions.RequestException as e:
            print(f"API请求错误: {e}")
            return None
        except (KeyError, IndexError) as e:
            print(f"API响应解析错误: {e}")
            return None
        except Exception as e:
            print(f"未知错误: {e}")
            return None
    
    def generate_character(self, description: str) -> Optional[Dict[str, Any]]:
        """
        生成角色信息
        :param description: 角色描述
        :return: 角色信息字典
        """
        prompt = f"""
        基于以下描述生成一个详细的角色信息：
        {description}
        
        请返回JSON格式，包含以下字段：
        - name: 角色名
        - traits: 特质列表
        - background: 背景故事
        - motivations: 动机
        - constraints: 行为限制
        """
        
        response = self.generate_content(prompt, max_tokens=800)
        if response:
            try:
                # 尝试提取JSON部分
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = response[start:end]
                    return json.loads(json_str)
            except json.JSONDecodeError:
                print("无法解析AI响应为JSON格式")
                return None
        return None
    
    def generate_world_setting(self, description: str) -> Optional[Dict[str, Any]]:
        """
        生成世界设定
        :param description: 世界描述
        :return: 世界设定信息字典
        """
        prompt = f"""
        基于以下描述生成一个详细的世界设定：
        {description}
        
        请返回JSON格式，包含以下字段：
        - name: 世界名
        - axioms: 基本公理列表
        - laws: 法则
        - constraints: 约束条件
        - technologies: 科技水平
        - social_structure: 社会结构
        """
        
        response = self.generate_content(prompt, max_tokens=1000)
        if response:
            try:
                # 尝试提取JSON部分
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = response[start:end]
                    return json.loads(json_str)
            except json.JSONDecodeError:
                print("无法解析AI响应为JSON格式")
                return None
        return None
    
    def generate_plot_event(self, context: str, condition: str) -> Optional[Dict[str, Any]]:
        """
        基于上下文和条件生成情节事件
        :param context: 上下文
        :param condition: 触发条件
        :return: 情节事件信息字典
        """
        prompt = f"""
        基于以下上下文和条件生成一个情节事件：
        上下文: {context}
        条件: {condition}
        
        请返回JSON格式，包含以下字段：
        - event_name: 事件名
        - description: 事件描述
        - characters_involved: 涉及角色
        - consequences: 后果
        - story_impact: 对故事的影响
        """
        
        response = self.generate_content(prompt, max_tokens=600)
        if response:
            try:
                # 尝试提取JSON部分
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = response[start:end]
                    return json.loads(json_str)
            except json.JSONDecodeError:
                print("无法解析AI响应为JSON格式")
                return None
        return None


# 全局API客户端实例
_api_client = None


def get_api_client() -> APIClient:
    """
    获取API客户端实例
    """
    global _api_client
    if _api_client is None:
        _api_client = APIClient()
    return _api_client