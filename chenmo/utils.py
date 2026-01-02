"""
chenmo 工具函数
"""
import os
import re
from pathlib import Path
from typing import Union


def ensure_chenmo_dir(base_path: Path):
    """
    确保 .chenmo 目录结构存在
    """
    (base_path / 'works').mkdir(parents=True, exist_ok=True)
    (base_path / 'temps' / 'works').mkdir(parents=True, exist_ok=True)


def is_temp_work(work_name: str) -> bool:
    """
    判断是否为临时作品
    """
    return work_name.startswith('temps.')


def get_work_path(work_name: str, is_temp: bool = None) -> Path:
    """
    获取作品存储路径
    """
    base_path = Path.home() / '.chenmo'
    
    if is_temp is None:
        is_temp = is_temp_work(work_name)
    
    if is_temp:
        # 临时作品路径
        if work_name.startswith('temps.'):
            work_dir = work_name[6:]  # 移除 'temps.' 前缀
        else:
            work_dir = work_name
        return base_path / 'temps' / 'works' / work_dir
    else:
        # 持久作品路径
        return base_path / 'works' / work_name


def validate_namespace(namespace: str) -> bool:
    """
    验证命名空间是否有效
    """
    # 基本格式验证：只能包含字母、数字、下划线、点和连字符
    if not re.match(r'^[a-zA-Z0-9_.-]+$', namespace):
        return False
    
    # 检查是否包含保留关键字
    reserved = ['d', 'u', 'l', 'x', 'f', 'c', 'p', 'm', 't', 'r', 'i', 'novies', 'mxd', 'in']
    if namespace in reserved:
        return False
        
    return True


def get_storage_path(work_name: str, sub_name: str, target_type: str) -> Path:
    """
    根据目标类型获取存储路径
    """
    work_path = get_work_path(work_name)
    
    if target_type == 'c':  # 内核
        return work_path / 'cores' / f'{sub_name}.json'
    elif target_type == 'p':  # 人物
        return work_path / 'personas' / f'{sub_name}.json'
    elif target_type == 'm':  # 镜像
        return work_path / 'personas' / f'{sub_name}.json'
    elif target_type == 't':  # 科技
        return work_path / 'tech' / f'{sub_name}.json'
    elif target_type == 'novies':  # 主叙事
        return work_path / 'novies' / f'{sub_name}.json'
    else:
        raise ValueError(f"Unknown target type: {target_type}")


def ensure_work_directories(work_path: Path):
    """
    确保作品目录结构存在
    """
    (work_path / 'novies').mkdir(parents=True, exist_ok=True)
    (work_path / 'cores').mkdir(parents=True, exist_ok=True)
    (work_path / 'personas').mkdir(parents=True, exist_ok=True)
    (work_path / 'tech').mkdir(parents=True, exist_ok=True)


def load_json_file(file_path: Path) -> dict:
    """
    安全加载 JSON 文件
    """
    if file_path.exists():
        with open(file_path, 'r', encoding='utf-8') as f:
            return dict(file_path=file_path, **(load_json(f.read()) if f.read().strip() else {}))
    return {}


def save_json_file(file_path: Path, data: dict):
    """
    安全保存 JSON 文件
    """
    # 确保父目录存在
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        import json
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_json(json_str: str) -> dict:
    """
    解析 JSON 字符串
    """
    import json
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def create_manifest(work_name: str, version: str = "1.0", canonical_source: str = None) -> dict:
    """
    创建作品清单文件
    """
    manifest = {
        "name": work_name,
        "version": version,
        "canonical_source": canonical_source or "",
        "created_at": str(Path.home() / '.chenmo' / 'works' / work_name)
    }
    return manifest