"""
可编程元叙事引擎核心模块
"""
import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import requests
import tempfile


class ChenmoEngine:
    """可编程元叙事引擎核心类"""
    
    def __init__(self):
        self.home_dir = Path.home() / '.chenmo'
        self.works_dir = self.home_dir / 'works'
        self.temps_dir = self.home_dir / 'temps' / 'works'
        
        # 确保目录存在
        self.works_dir.mkdir(parents=True, exist_ok=True)
        self.temps_dir.mkdir(parents=True, exist_ok=True)
        
        # 当前工作标识符
        self.current_work = None
        
        # 缓存已加载的作品
        self.loaded_works = {}
        
    def set_current_work(self, identifier):
        """设置当前工作标识符"""
        self.current_work = identifier
    
    def import_entity(self, entity, as_alias=None):
        """导入实体"""
        # 如果实体不存在，尝试自动拉取
        if not self.entity_exists(entity):
            self.auto_deploy_entity(entity)
        
        # 返回实体引用
        alias = as_alias or entity
        self.loaded_works[alias] = entity
        return f"Imported {entity} as {alias}"
    
    def entity_exists(self, entity):
        """检查实体是否存在"""
        # 检查是否在本地存在
        parts = entity.split('.')
        if len(parts) >= 2:
            work_name = parts[0]
            # 检查 works 目录
            work_path = self.works_dir / work_name
            if work_path.exists():
                return True
            # 检查 temps 目录
            temp_work_path = self.temps_dir / work_name
            if temp_work_path.exists():
                return True
        return False
    
    def auto_deploy_entity(self, entity):
        """自动部署实体"""
        # 这里可以实现自动从官方仓库拉取
        parts = entity.split('.')
        if len(parts) >= 2:
            work_name = parts[0]
            # 尝试从官方仓库下载
            self.download_package(work_name)
    
    def download_package(self, package_id):
        """下载包"""
        # 这里应该连接到官方仓库
        # 暂时使用模拟实现
        pass
    
    def get_work_path(self, work_name: str) -> Path:
        """获取作品路径"""
        if work_name.startswith('temps.'):
            temp_name = work_name.replace('temps.', '', 1)
            return self.temps_dir / temp_name
        else:
            return self.works_dir / work_name
    
    def create_work_structure(self, work_name: str) -> Path:
        """创建作品结构"""
        work_path = self.get_work_path(work_name)
        
        # 检查是否已存在
        if work_path.exists():
            raise ValueError(f"Namespace collision: {work_name} already exists")
        
        # 创建目录结构
        work_path.mkdir(parents=True, exist_ok=True)
        (work_path / 'novies').mkdir(exist_ok=True)
        (work_path / 'cores').mkdir(exist_ok=True)
        (work_path / 'personas').mkdir(exist_ok=True)
        (work_path / 'tech').mkdir(exist_ok=True)
        
        # 创建 manifest.json
        manifest = {
            "name": work_name,
            "version": "1.0",
            "canonical_source": work_name
        }
        with open(work_path / 'manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        return work_path
    
    def save_entity(self, work_name: str, sub_name: str, entity_type: str, data: Dict[str, Any]):
        """保存实体"""
        work_path = self.get_work_path(work_name)
        
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
        
        # 保存文件
        file_path = target_dir / f"{sub_name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return file_path
    
    def load_entity(self, work_name: str, sub_name: str, entity_type: str) -> Optional[Dict[str, Any]]:
        """加载实体"""
        work_path = self.get_work_path(work_name)
        
        # 确定加载目录
        if entity_type == 'c':  # core
            target_dir = work_path / 'cores'
        elif entity_type == 'p':  # persona
            target_dir = work_path / 'personas'
        elif entity_type == 't':  # tech
            target_dir = work_path / 'tech'
        elif entity_type == 'm':  # mirror
            target_dir = work_path / 'personas'  # 镜像也存储在personas中
        else:
            target_dir = work_path / 'novies'  # 默认
        
        file_path = target_dir / f"{sub_name}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    def search_entities(self, keyword: str, work_filter: Optional[str] = None, type_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """搜索实体"""
        results = []
        
        # 搜索 works 目录
        for work_path in self.works_dir.iterdir():
            if work_path.is_dir():
                work_name = work_path.name
                if work_filter and work_name != work_filter:
                    continue
                
                # 搜索不同类型的实体
                for entity_type in ['novies', 'cores', 'personas', 'tech']:
                    entity_dir = work_path / entity_type
                    if entity_dir.exists():
                        for entity_file in entity_dir.iterdir():
                            if entity_file.suffix == '.json':
                                entity_name = entity_file.stem
                                if keyword.lower() in entity_name.lower() or keyword.lower() in work_name.lower():
                                    if not type_filter or type_filter == entity_type[0] or type_filter == 'all':
                                        with open(entity_file, 'r', encoding='utf-8') as f:
                                            try:
                                                data = json.load(f)
                                                results.append({
                                                    'work': work_name,
                                                    'name': entity_name,
                                                    'type': entity_type[0],
                                                    'path': str(entity_file),
                                                    'data': data
                                                })
                                            except:
                                                # 如果JSON解析失败，仍然记录基本信息
                                                results.append({
                                                    'work': work_name,
                                                    'name': entity_name,
                                                    'type': entity_type[0],
                                                    'path': str(entity_file),
                                                    'data': {}
                                                })
        
        # 搜索 temps 目录
        for work_path in self.temps_dir.iterdir():
            if work_path.is_dir():
                work_name = work_path.name
                if work_filter and work_name != work_filter:
                    continue
                
                # 搜索不同类型的实体
                for entity_type in ['novies', 'cores', 'personas', 'tech']:
                    entity_dir = work_path / entity_type
                    if entity_dir.exists():
                        for entity_file in entity_dir.iterdir():
                            if entity_file.suffix == '.json':
                                entity_name = entity_file.stem
                                if keyword.lower() in entity_name.lower() or keyword.lower() in work_name.lower():
                                    if not type_filter or type_filter == entity_type[0] or type_filter == 'all':
                                        with open(entity_file, 'r', encoding='utf-8') as f:
                                            try:
                                                data = json.load(f)
                                                results.append({
                                                    'work': f'temps.{work_name}',
                                                    'name': entity_name,
                                                    'type': entity_type[0],
                                                    'path': str(entity_file),
                                                    'data': data
                                                })
                                            except:
                                                # 如果JSON解析失败，仍然记录基本信息
                                                results.append({
                                                    'work': f'temps.{work_name}',
                                                    'name': entity_name,
                                                    'type': entity_type[0],
                                                    'path': str(entity_file),
                                                    'data': {}
                                                })
        
        return results