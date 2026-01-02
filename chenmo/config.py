import os
import json
from pathlib import Path

def get_config_path():
    """获取配置文件路径"""
    home_dir = Path.home()
    return home_dir / '.chenmo' / 'config.json'

def ensure_config_dir():
    """确保配置目录存在"""
    config_path = get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    return config_path

def load_config():
    """加载配置，如果不存在则提示用户设置"""
    config_path = ensure_config_dir()
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # 配置不存在，提示用户设置
        print("欢迎使用 chenmo 可编程元叙事引擎！")
        print("首次使用需要配置AI服务信息：")
        api_url = input("请输入API URL (例如: https://api.openai.com/v1/chat/completions): ").strip()
        api_key = input("请输入API Key: ").strip()
        model = input("请输入模型名称 (例如: gpt-4, gpt-3.5-turbo): ").strip()
        
        config = {
            "api_url": api_url,
            "api_key": api_key,
            "model": model
        }
        
        # 保存配置
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"配置已保存到 {config_path}")
        return config

def get_api_config():
    """获取API配置，优先从环境变量读取，然后从配置文件读取"""
    # 优先从环境变量读取
    api_key = os.getenv('CHENMO_API_KEY')
    api_url = os.getenv('CHENMO_API_URL', 'https://api.openai.com/v1/chat/completions')
    model = os.getenv('CHENMO_MODEL', 'gpt-3.5-turbo')
    
    if api_key:
        return {
            'api_key': api_key,
            'api_url': api_url,
            'model': model
        }
    
    # 如果环境变量未设置，从配置文件读取
    try:
        config = load_config()
        return config
    except Exception as e:
        print(f"配置加载失败: {e}")
        print("请设置环境变量 CHENMO_API_KEY, CHENMO_API_URL, CHENMO_MODEL 或确保配置文件存在")
        return None