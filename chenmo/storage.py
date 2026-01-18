"""
存储管理模块
处理数据持久化和文件操作
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import shutil
import zipfile


class StorageManager:
    """存储管理器"""
    
    def __init__(self):
        self.engine = None  # 会在初始化时设置
    
    def initialize_with_engine(self, engine):
        """使用引擎初始化"""
        self.engine = engine
    
    def save_work_data(self, work_name: str, sub_name: str, entity_type: str, data: Dict[str, Any], merge_strategy: str = "strict"):
        """保存作品数据"""
        if not self.engine:
            from .core import ChenmoEngine
            self.engine = ChenmoEngine()
        
        work_path = self.engine.get_work_path(work_name)
        
        # 确定保存目录
        if entity_type == 'c':  # core
            target_dir = work_path / 'cores'
        elif entity_type == 'p':  # persona
            target_dir = work_path / 'personas'
        elif entity_type == 't':  # tech
            target_dir = work_path / 'tech'
        elif entity_type == 'novies':  # novies
            target_dir = work_path / 'novies'
        else:
            target_dir = work_path / 'novies'  # 默认
        
        target_dir.mkdir(exist_ok=True)
        
        # 检查目标文件是否存在
        file_path = target_dir / f"{sub_name}.json"
        if file_path.exists() and merge_strategy != "overlay":
            if merge_strategy == "strict":
                raise ValueError(f"File exists: {file_path}")
            elif merge_strategy == "patch":
                # 加载现有数据并合并
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                # 递归合并字典
                merged_data = self._recursive_merge(existing_data, data)
                
                # 保存合并后的数据
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(merged_data, f, ensure_ascii=False, indent=2)
                
                return file_path
        
        # 直接保存数据
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return file_path
    
    def _recursive_merge(self, base: dict, update: dict) -> dict:
        """递归合并字典"""
        result = base.copy()
        
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._recursive_merge(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def load_work_data(self, work_name: str, sub_name: str, entity_type: str) -> Optional[Dict[str, Any]]:
        """加载作品数据"""
        if not self.engine:
            from .core import ChenmoEngine
            self.engine = ChenmoEngine()
        
        return self.engine.load_entity(work_name, sub_name, entity_type)
    
    def export_work_as_package(self, work_name: str, package_path: str) -> bool:
        """导出作品为包文件(.narr)"""
        if not self.engine:
            from .core import ChenmoEngine
            self.engine = ChenmoEngine()
        
        work_path = self.engine.get_work_path(work_name)
        if not work_path.exists():
            return False
        
        # 创建临时目录用于打包
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(work_path):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(work_path.parent)
                    zipf.write(file_path, arcname)
        
        return True
    
    def import_package(self, package_path: str, work_name: str) -> bool:
        """导入包文件(.narr)"""
        if not self.engine:
            from .core import ChenmoEngine
            self.engine = ChenmoEngine()
        
        work_path = self.engine.get_work_path(work_name)
        
        # 检查是否已存在
        if work_path.exists():
            raise ValueError(f"Namespace collision: {work_name} already exists")
        
        # 解压包文件
        with zipfile.ZipFile(package_path, 'r') as zipf:
            zipf.extractall(work_path)
        
        return True
    
    def validate_package(self, package_path: str) -> bool:
        """验证包文件完整性"""
        try:
            with zipfile.ZipFile(package_path, 'r') as zipf:
                # 检查必要文件
                namelist = zipf.namelist()
                
                # 检查是否有manifest.json
                if 'manifest.json' not in namelist:
                    return False
                
                # 检查是否有必要的目录结构
                required_dirs = ['novies/', 'cores/', 'personas/', 'tech/']
                for req_dir in required_dirs:
                    if not any(name.startswith(req_dir) for name in namelist):
                        return False
                
                return True
        except:
            return False