"""
chenmo 存储管理器
"""
import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from .utils import get_work_path, ensure_work_directories, load_json_file, save_json_file, create_manifest


class StorageManager:
    """
    存储管理器，负责文件的读写操作
    """
    
    def __init__(self):
        self.base_path = Path.home() / '.chenmo'
    
    def create_work(self, work_name: str, is_temp: bool = False, description: str = ""):
        """
        创建新的作品目录结构
        """
        work_path = get_work_path(work_name, is_temp=is_temp)
        
        # 确保作品目录不存在
        if work_path.exists():
            raise ValueError(f"Work already exists: {work_path}")
        
        # 创建目录结构
        ensure_work_directories(work_path)
        
        # 创建清单文件
        manifest = create_manifest(work_name)
        save_json_file(work_path / 'manifest.json', manifest)
        
        return work_path
    
    def save_entity(self, work_name: str, sub_name: str, entity_type: str, data: Dict[str, Any]):
        """
        保存实体数据
        """
        from .utils import get_storage_path
        file_path = get_storage_path(work_name, sub_name, entity_type)
        save_json_file(file_path, data)
    
    def load_entity(self, work_name: str, sub_name: str, entity_type: str) -> Optional[Dict[str, Any]]:
        """
        加载实体数据
        """
        from .utils import get_storage_path
        file_path = get_storage_path(work_name, sub_name, entity_type)
        
        if file_path.exists():
            return load_json_file(file_path)
        return None
    
    def list_entities(self, work_name: str, entity_type: str) -> list:
        """
        列出指定类型的所有实体
        """
        work_path = get_work_path(work_name)
        
        if entity_type == 'c':  # 内核
            dir_path = work_path / 'cores'
        elif entity_type == 'p':  # 人物
            dir_path = work_path / 'personas'
        elif entity_type == 't':  # 科技
            dir_path = work_path / 'tech'
        elif entity_type == 'novies':  # 主叙事
            dir_path = work_path / 'novies'
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        if not dir_path.exists():
            return []
        
        entities = []
        for file_path in dir_path.glob('*.json'):
            entities.append(file_path.stem)
        
        return entities
    
    def work_exists(self, work_name: str, is_temp: bool = None) -> bool:
        """
        检查作品是否存在
        """
        work_path = get_work_path(work_name, is_temp)
        return work_path.exists()
    
    def copy_work(self, source_work: str, target_work: str, is_temp: bool = False):
        """
        复制整个作品
        """
        source_path = get_work_path(source_work)
        target_path = get_work_path(target_work, is_temp)
        
        if not source_path.exists():
            raise ValueError(f"Source work does not exist: {source_path}")
        
        if target_path.exists():
            raise ValueError(f"Target work already exists: {target_path}")
        
        # 复制整个目录
        shutil.copytree(source_path, target_path)
        
        # 更新清单文件中的作品名
        manifest_path = target_path / 'manifest.json'
        if manifest_path.exists():
            manifest = load_json_file(manifest_path)
            manifest['name'] = target_work
            save_json_file(manifest_path, manifest)
    
    def delete_work(self, work_name: str, is_temp: bool = False):
        """
        删除作品
        """
        work_path = get_work_path(work_name, is_temp)
        
        if work_path.exists():
            shutil.rmtree(work_path)
    
    def get_work_manifest(self, work_name: str, is_temp: bool = False) -> Optional[Dict[str, Any]]:
        """
        获取作品清单
        """
        work_path = get_work_path(work_name, is_temp)
        manifest_path = work_path / 'manifest.json'
        
        if manifest_path.exists():
            return load_json_file(manifest_path)
        return None