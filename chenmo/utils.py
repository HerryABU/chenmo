"""
工具模块
提供各种辅助功能
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional


def print_content(content: str, to: Optional[str] = None, format: str = "narrative", merge: str = "strict"):
    """
    智能输出与更新接口
    """
    if format == "narrative":
        # 叙事格式：直接输出文本
        if to is None:
            # 输出到控制台
            print(content)
        else:
            # 输出到文件
            with open(to, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Narrative content written to {to}")
    elif format == "world":
        # 世界构建格式：解析JSON并写入结构化文件
        try:
            # 解析内容为JSON
            parsed_data = json.loads(content)
            
            # 验证必需字段
            if 'type' not in parsed_data or 'name' not in parsed_data:
                raise ValueError("World format requires 'type' and 'name' fields")
            
            entity_type = parsed_data['type']
            entity_name = parsed_data['name']
            
            if to is None:
                # 如果没有指定目标，输出到控制台
                print(json.dumps(parsed_data, ensure_ascii=False, indent=2))
            else:
                # 根据目标路径和实体类型确定保存位置
                target_path = Path(to)
                
                if target_path.is_dir():
                    # 如果目标是目录，则根据实体类型创建相应子目录
                    if entity_type == 'work':
                        # 对于作品，创建作品目录结构
                        work_path = target_path / entity_name
                        work_path.mkdir(exist_ok=True)
                        
                        # 创建完整的目录结构
                        (work_path / 'novies').mkdir(exist_ok=True)
                        (work_path / 'cores').mkdir(exist_ok=True)
                        (work_path / 'personas').mkdir(exist_ok=True)
                        (work_path / 'tech').mkdir(exist_ok=True)
                        
                        # 保存作品数据
                        output_file = work_path / 'manifest.json'
                        
                        if output_file.exists() and merge != "overlay":
                            if merge == "strict":
                                raise ValueError(f"File exists: {output_file}")
                            elif merge == "patch":
                                # 加载现有数据并合并
                                with open(output_file, 'r', encoding='utf-8') as f:
                                    existing_data = json.load(f)
                                
                                # 递归合并
                                merged_data = _recursive_merge(existing_data, parsed_data)
                                
                                with open(output_file, 'w', encoding='utf-8') as f:
                                    json.dump(merged_data, f, ensure_ascii=False, indent=2)
                            else:
                                raise ValueError(f"Unknown merge strategy: {merge}")
                        else:
                            with open(output_file, 'w', encoding='utf-8') as f:
                                json.dump(parsed_data, f, ensure_ascii=False, indent=2)
                    
                    else:
                        # 对于其他类型，根据entity_type确定目录
                        if entity_type == 'core':
                            target_dir = target_path / 'cores'
                        elif entity_type == 'persona':
                            target_dir = target_path / 'personas'
                        elif entity_type == 'tech':
                            target_dir = target_path / 'tech'
                        else:
                            target_dir = target_path / 'novies'  # 默认
                        
                        target_dir.mkdir(exist_ok=True)
                        
                        # 保存文件
                        output_file = target_dir / f"{entity_name}.json"
                        
                        if output_file.exists() and merge != "overlay":
                            if merge == "strict":
                                raise ValueError(f"File exists: {output_file}")
                            elif merge == "patch":
                                # 加载现有数据并合并
                                with open(output_file, 'r', encoding='utf-8') as f:
                                    existing_data = json.load(f)
                                
                                # 递归合并
                                merged_data = _recursive_merge(existing_data, parsed_data)
                                
                                with open(output_file, 'w', encoding='utf-8') as f:
                                    json.dump(merged_data, f, ensure_ascii=False, indent=2)
                            else:
                                raise ValueError(f"Unknown merge strategy: {merge}")
                        else:
                            with open(output_file, 'w', encoding='utf-8') as f:
                                json.dump(parsed_data, f, ensure_ascii=False, indent=2)
                
                else:
                    # 如果目标是具体文件
                    if target_path.exists() and merge != "overlay":
                        if merge == "strict":
                            raise ValueError(f"File exists: {target_path}")
                        elif merge == "patch":
                            # 加载现有数据并合并
                            with open(target_path, 'r', encoding='utf-8') as f:
                                existing_data = json.load(f)
                            
                            # 递归合并
                            merged_data = _recursive_merge(existing_data, parsed_data)
                            
                            with open(target_path, 'w', encoding='utf-8') as f:
                                json.dump(merged_data, f, ensure_ascii=False, indent=2)
                        else:
                            raise ValueError(f"Unknown merge strategy: {merge}")
                    else:
                        with open(target_path, 'w', encoding='utf-8') as f:
                            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
                
                print(f"World data written to {target_path}")
        
        except json.JSONDecodeError:
            raise ValueError("Content is not valid JSON for world format")


def _recursive_merge(base: dict, update: dict) -> dict:
    """递归合并字典"""
    result = base.copy()
    
    for key, value in update.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _recursive_merge(result[key], value)
        else:
            result[key] = value
    
    return result


def validate_world_data(data: Dict[str, Any]) -> bool:
    """验证世界数据格式"""
    required_fields = ['type', 'name', 'metadata', 'data']
    
    for field in required_fields:
        if field not in data:
            return False
    
    # 验证type字段的值
    valid_types = ['work', 'persona', 'core', 'tech']
    if data['type'] not in valid_types:
        return False
    
    # 验证metadata必须包含description
    if 'description' not in data['metadata']:
        return False
    
    return True


def clean_temp_files():
    """清理临时文件"""
    home_dir = Path.home() / '.chenmo'
    temps_dir = home_dir / 'temps'
    
    if temps_dir.exists():
        import shutil
        shutil.rmtree(temps_dir)
        temps_dir.mkdir(parents=True, exist_ok=True)


def list_all_works():
    """列出所有作品"""
    home_dir = Path.home() / '.chenmo'
    works_dir = home_dir / 'works'
    temps_dir = home_dir / 'temps' / 'works'
    
    works = []
    
    # 列出持久作品
    if works_dir.exists():
        for work_path in works_dir.iterdir():
            if work_path.is_dir():
                works.append(('persistent', work_path.name))
    
    # 列出临时作品
    if temps_dir.exists():
        for work_path in temps_dir.iterdir():
            if work_path.is_dir():
                works.append(('temporary', f'temps.{work_path.name}'))
    
    return works