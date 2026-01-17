"""
LLM 接口模块
提供与大语言模型的交互功能
"""
import json
import os
from typing import Dict, Any, Optional
from pathlib import Path


class LLMInterface:
    """LLM 接口类"""
    
    def __init__(self, **kwargs):
        self.type = kwargs.get('type', 'openai')
        self.model = kwargs.get('model', 'gpt-4o')
        self.apiurl = kwargs.get('apiurl', None)
        self.apikey = kwargs.get('apikey', os.getenv('OPENAI_API_KEY'))
        self.mode = kwargs.get('mode', 'narrative')
        
        # 根据类型初始化相应的客户端
        if self.type == 'openai':
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.apikey, base_url=self.apiurl)
            except ImportError:
                raise ImportError("Please install openai: pip install openai")
        elif self.type == 'ollama':
            try:
                import ollama
                self.client = ollama
            except ImportError:
                raise ImportError("Please install ollama: pip install ollama")
        else:
            # 自定义类型，需要用户提供客户端
            self.client = None
    
    def generate(self, prompt: str) -> str:
        """生成内容"""
        if self.type == 'openai':
            return self._generate_openai(prompt)
        elif self.type == 'ollama':
            return self._generate_ollama(prompt)
        else:
            raise ValueError(f"Unsupported LLM type: {self.type}")
    
    def _generate_openai(self, prompt: str) -> str:
        """使用OpenAI生成内容"""
        if self.mode == 'narrative':
            # 叙事模式：生成自然语言文本
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return response.choices[0].message.content
        elif self.mode == 'world':
            # 世界构建模式：生成符合chenmo规范的JSON
            system_prompt = """
            你是一个结构化的虚构世界构建助手。请按照chenmo库的规范生成JSON格式的世界数据。
            输出必须是有效的JSON，包含以下字段：
            {
              "type": "work" | "persona" | "core" | "tech",
              "name": "实体名",
              "metadata": {
                "description": "自然语言描述",
                "source_prompt": "用户原始提示",
                "generated_by": "模型名"
              },
              "data": {
                // 结构化字段
              }
            }
            """
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            content = response.choices[0].message.content
            
            # 尝试解析为JSON
            try:
                # 移除可能的markdown包装
                if content.startswith('```json'):
                    content = content[7:content.rfind('```')]
                elif content.startswith('```'):
                    content = content[3:content.rfind('```')]
                
                json.loads(content)  # 验证是否为有效JSON
                return content
            except json.JSONDecodeError:
                # 如果不是有效JSON，尝试修复
                return self._fix_json_output(content)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")
    
    def _generate_ollama(self, prompt: str) -> str:
        """使用Ollama生成内容"""
        if self.mode == 'narrative':
            # 叙事模式：生成自然语言文本
            response = self.client.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
            return response['message']['content']
        elif self.mode == 'world':
            # 世界构建模式：生成符合chenmo规范的JSON
            system_prompt = """
            你是一个结构化的虚构世界构建助手。请按照chenmo库的规范生成JSON格式的世界数据。
            输出必须是有效的JSON，包含以下字段：
            {
              "type": "work" | "persona" | "core" | "tech",
              "name": "实体名",
              "metadata": {
                "description": "自然语言描述",
                "source_prompt": "用户原始提示",
                "generated_by": "模型名"
              },
              "data": {
                // 结构化字段
              }
            }
            """
            response = self.client.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            content = response['message']['content']
            
            # 尝试解析为JSON
            try:
                # 移除可能的markdown包装
                if content.startswith('```json'):
                    content = content[7:content.rfind('```')]
                elif content.startswith('```'):
                    content = content[3:content.rfind('```')]
                
                json.loads(content)  # 验证是否为有效JSON
                return content
            except json.JSONDecodeError:
                # 如果不是有效JSON，尝试修复
                return self._fix_json_output(content)
        else:
            raise ValueError(f"Unsupported mode: {self.mode}")
    
    def _fix_json_output(self, content: str) -> str:
        """尝试修复JSON输出"""
        # 简单的JSON修复逻辑
        # 找到第一个{和最后一个}
        start = content.find('{')
        end = content.rfind('}')
        
        if start != -1 and end != -1 and start < end:
            json_str = content[start:end+1]
            try:
                json.loads(json_str)
                return json_str
            except json.JSONDecodeError:
                pass
        
        # 如果无法修复，返回原始内容
        return content


def create_llm(**kwargs):
    """创建LLM接口实例的便捷函数"""
    return LLMInterface(**kwargs)