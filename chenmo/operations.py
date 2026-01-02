"""
chenmo 操作管理器
实现所有操作的具体逻辑
"""
import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from .utils import get_work_path, is_temp_work, validate_namespace, get_storage_path, ensure_work_directories
from .storage import StorageManager
from .api import get_api_client


class OperationManager:
    """
    操作管理器，实现所有 chenmo 操作的具体逻辑
    """
    
    def __init__(self, storage_manager: StorageManager):
        self.storage = storage_manager
    
    def deploy(self, work_name: str, sub_name: str, source_from: str, toas: str):
        """
        部署操作 - 从源安装设定包到本地持久空间
        """
        # 验证命名空间
        if not validate_namespace(toas):
            raise ValueError(f"Invalid namespace: {toas}")
        
        # 检查目标是否已存在
        target_path = get_work_path(toas, is_temp=False)
        if target_path.exists():
            raise ValueError(f"Namespace collision: {toas} already exists")
        
        # 创建目标目录
        ensure_work_directories(target_path)
        
        # 模拟从源获取数据（在实际实现中，这里会从远程获取.narr包）
        # 这里我们创建一个示例结构
        manifest = {
            "name": toas,
            "version": "1.0",
            "canonical_source": source_from or f"official_repo/{work_name}"
        }
        
        # 保存清单文件
        import json
        with open(target_path / 'manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        # 创建示例内容
        if sub_name == 'novies':
            novies_data = {
                "type": "novies",
                "source_work": work_name,
                "description": f"Deployed from {work_name}",
                "deployed_from": source_from
            }
            with open(target_path / 'novies' / f'{sub_name}.json', 'w', encoding='utf-8') as f:
                json.dump(novies_data, f, ensure_ascii=False, indent=2)
        
        return f"Successfully deployed {work_name}.{sub_name} to {toas}"
    
    def update(self, work_name: str, sub_name: str, source_from: str, 
               merge_strategy: str, local_origin: str, target_path: str, toas: str):
        """
        更新操作 - 在已有持久作品上增量合并变更
        """
        # 获取当前作品路径
        current_work_path = get_work_path(work_name)
        if not current_work_path.exists():
            raise ValueError(f"Work does not exist: {work_name}")
        
        if local_origin:
            # 模式B：分支合并
            origin_work_path = Path(local_origin)
            if not origin_work_path.exists():
                raise ValueError(f"Local origin does not exist: {local_origin}")
            
            target_work_path = get_work_path(toas) if target_path is None else Path(target_path)
            
            # 检查目标是否已存在
            if target_work_path.exists():
                raise ValueError(f"Target already exists: {target_work_path}")
            
            # 复制源到目标
            shutil.copytree(origin_work_path, target_work_path)
            
            # 应用更新
            # 这里会根据merge_strategy进行合并
            if merge_strategy == 'overlay':
                # 简单覆盖
                pass
            elif merge_strategy == 'patch':
                # 补丁合并
                pass
            elif merge_strategy == 'strict':
                # 严格模式，冲突则失败
                pass
            elif merge_strategy == 'interactive':
                # 交互模式，需要用户确认
                pass
            
            return f"Successfully updated {work_name}.{sub_name} from {source_from} to {toas}"
        else:
            # 模式A：原地更新
            # 应用更新到当前作品
            return f"Successfully updated {work_name}.{sub_name} in place"
    
    def register(self, work_name: str, sub_name: str, log_works: str, 
                 log_person: List[str], log_settings: List[str], log_thing: List[str]):
        """
        注册操作 - 从零声明新作品、人物、设定或物品
        """
        # 判断是否为临时作品
        is_temp = is_temp_work(work_name)
        if is_temp and work_name.startswith('temps.'):
            actual_work_name = work_name[6:]
        else:
            actual_work_name = work_name
        
        # 检查作品是否存在，如果不存在则创建
        work_path = get_work_path(work_name, is_temp=is_temp)
        if not work_path.exists():
            ensure_work_directories(work_path)
            
            # 创建清单文件
            manifest = {
                "name": actual_work_name,
                "version": "1.0",
                "canonical_source": "local_creation"
            }
            with open(work_path / 'manifest.json', 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        # 如果log_works是None或空字符串，尝试使用AI生成
        if sub_name == 'novies' and log_works:
            # 检查是否包含AI增强指令（以"AI:"开头）
            ai_enhanced = log_works.startswith("AI:")
            if ai_enhanced:
                ai_description = log_works[3:].strip()  # 移除"AI:"前缀
                api_client = get_api_client()
                enhanced_data = api_client.generate_world_setting(ai_description)
                if enhanced_data:
                    novies_data = {
                        "type": "novies",
                        "description": ai_description,
                        "ai_enhanced": True,
                        "enhanced_data": enhanced_data,
                        "registered_at": str(Path.home() / '.chenmo')
                    }
                else:
                    # 如果AI生成失败，使用原始描述
                    novies_data = {
                        "type": "novies",
                        "description": ai_description,
                        "ai_enhanced": False,
                        "registered_at": str(Path.home() / '.chenmo')
                    }
            else:
                novies_data = {
                    "type": "novies",
                    "description": log_works,
                    "ai_enhanced": False,
                    "registered_at": str(Path.home() / '.chenmo')
                }
            
            with open(work_path / 'novies' / f'{sub_name}.json', 'w', encoding='utf-8') as f:
                json.dump(novies_data, f, ensure_ascii=False, indent=2)
        
        # 注册人物 - 尝试AI增强
        for person_name in log_person:
            ai_enhanced = person_name.startswith("AI:")
            if ai_enhanced:
                ai_description = person_name[3:].strip()
                api_client = get_api_client()
                enhanced_data = api_client.generate_character(ai_description)
                if enhanced_data:
                    person_data = {
                        "type": "persona",
                        "name": enhanced_data.get("name", ai_description),
                        "ai_enhanced": True,
                        "enhanced_data": enhanced_data,
                        "registered_from": f"{work_name}.{sub_name}"
                    }
                else:
                    # 如果AI生成失败，使用原始名称
                    person_data = {
                        "type": "persona",
                        "name": ai_description,
                        "ai_enhanced": False,
                        "registered_from": f"{work_name}.{sub_name}"
                    }
            else:
                person_data = {
                    "type": "persona",
                    "name": person_name,
                    "ai_enhanced": False,
                    "registered_from": f"{work_name}.{sub_name}"
                }
            
            with open(work_path / 'personas' / f'{person_name.split()[0] if " " in person_name else person_name}.json', 'w', encoding='utf-8') as f:
                json.dump(person_data, f, ensure_ascii=False, indent=2)
        
        # 注册设定 - 尝试AI增强
        if log_settings:
            processed_settings = []
            for setting in log_settings:
                ai_enhanced = setting.startswith("AI:")
                if ai_enhanced:
                    ai_description = setting[3:].strip()
                    api_client = get_api_client()
                    enhanced_data = api_client.generate_world_setting(ai_description)
                    if enhanced_data:
                        processed_settings.append({
                            "original": ai_description,
                            "ai_enhanced": True,
                            "enhanced_data": enhanced_data
                        })
                    else:
                        processed_settings.append({
                            "original": ai_description,
                            "ai_enhanced": False
                        })
                else:
                    processed_settings.append({
                        "original": setting,
                        "ai_enhanced": False
                    })
            
            settings_data = {
                "type": "core",
                "settings": processed_settings,
                "registered_from": f"{work_name}.{sub_name}"
            }
            with open(work_path / 'cores' / f'{sub_name}_settings.json', 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, ensure_ascii=False, indent=2)
        
        # 注册物品/科技 - 尝试AI增强
        if log_thing:
            processed_things = []
            for thing in log_thing:
                ai_enhanced = thing.startswith("AI:")
                if ai_enhanced:
                    ai_description = thing[3:].strip()
                    api_client = get_api_client()
                    # 使用通用生成方法来处理物品/科技
                    prompt = f"基于以下描述生成详细的科技/物品信息：{ai_description}"
                    enhanced_description = api_client.generate_content(prompt)
                    if enhanced_description:
                        processed_things.append({
                            "original": ai_description,
                            "ai_enhanced": True,
                            "enhanced_description": enhanced_description
                        })
                    else:
                        processed_things.append({
                            "original": ai_description,
                            "ai_enhanced": False
                        })
                else:
                    processed_things.append({
                        "original": thing,
                        "ai_enhanced": False
                    })
            
            thing_data = {
                "type": "tech",
                "items": processed_things,
                "registered_from": f"{work_name}.{sub_name}"
            }
            with open(work_path / 'tech' / f'{sub_name}_tech.json', 'w', encoding='utf-8') as f:
                json.dump(thing_data, f, ensure_ascii=False, indent=2)
        
        return f"Successfully registered {work_name}.{sub_name}"
    
    def mix(self, sources: List[tuple], weights: List[float], target_type: str, toas: str):
        """
        混合操作 - 按权重融合多源设定，生成新实体
        """
        # 验证源是否存在
        for source_work, source_sub in sources:
            work_path = get_work_path(source_work)
            if not work_path.exists():
                raise ValueError(f"Source work does not exist: {source_work}")
        
        # 创建目标作品
        target_path = get_work_path(toas, is_temp=False)
        if target_path.exists():
            raise ValueError(f"Target already exists: {toas}")
        
        ensure_work_directories(target_path)
        
        # 模拟混合过程
        mixed_data = {
            "type": target_type,
            "sources": sources,
            "weights": weights,
            "mixed_at": str(Path.home() / '.chenmo'),
            "description": f"Mixed content from {len(sources)} sources"
        }
        
        # 保存混合结果
        import json
        with open(target_path / 'novies' / f'{toas}.json', 'w', encoding='utf-8') as f:
            json.dump(mixed_data, f, ensure_ascii=False, indent=2)
        
        # 创建清单文件
        manifest = {
            "name": toas,
            "version": "1.0",
            "canonical_source": f"mixed from {sources}"
        }
        with open(target_path / 'manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        return f"Successfully mixed sources into {toas}"
    
    def fabricate(self, work_name: str, sub_name: str, setting: str):
        """
        实例化操作 - 动态生成作品实例
        """
        # 检查作品是否已存在
        work_path = get_work_path(work_name, is_temp=False)
        if work_path.exists():
            raise ValueError(f"Work already exists: {work_name}")
        
        # 创建作品目录
        ensure_work_directories(work_path)
        
        # 创建基础内容
        novies_data = {
            "type": "novies",
            "setting": setting,
            "fabricated_at": str(Path.home() / '.chenmo')
        }
        
        import json
        with open(work_path / 'novies' / f'{sub_name}.json', 'w', encoding='utf-8') as f:
            json.dump(novies_data, f, ensure_ascii=False, indent=2)
        
        # 创建清单文件
        manifest = {
            "name": work_name,
            "version": "1.0",
            "canonical_source": "fabricated"
        }
        with open(work_path / 'manifest.json', 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        return f"Successfully fabricated {work_name}.{sub_name}"
    
    def core(self, work_name: str, sub_name: str, axioms: List[str], constraints: List[str]):
        """
        内核提取操作 - 定义或提取底层法则
        """
        # 获取作品路径
        work_path = get_work_path(work_name)
        if not work_path.exists():
            raise ValueError(f"Work does not exist: {work_name}")
        
        # 确保目录存在
        ensure_work_directories(work_path)
        
        # 检查是否需要AI增强（axioms或constraints中包含"AI:"前缀）
        ai_enhanced_axioms = [a for a in axioms if a.startswith("AI:")]
        ai_enhanced_constraints = [c for c in constraints if c.startswith("AI:")]
        
        processed_axioms = []
        processed_constraints = []
        
        # 处理AI增强的公理
        for axiom in axioms:
            if axiom.startswith("AI:"):
                ai_description = axiom[3:].strip()
                api_client = get_api_client()
                enhanced_data = api_client.generate_world_setting(ai_description)
                if enhanced_data:
                    processed_axioms.append({
                        "original": ai_description,
                        "ai_enhanced": True,
                        "enhanced_data": enhanced_data,
                        "axiom_type": "generated"
                    })
                else:
                    processed_axioms.append({
                        "original": ai_description,
                        "ai_enhanced": False,
                        "axiom_type": "fallback"
                    })
            else:
                processed_axioms.append(axiom)
        
        # 处理AI增强的约束
        for constraint in constraints:
            if constraint.startswith("AI:"):
                ai_description = constraint[3:].strip()
                api_client = get_api_client()
                enhanced_data = api_client.generate_world_setting(ai_description)
                if enhanced_data:
                    processed_constraints.append({
                        "original": ai_description,
                        "ai_enhanced": True,
                        "enhanced_data": enhanced_data,
                        "constraint_type": "generated"
                    })
                else:
                    processed_constraints.append({
                        "original": ai_description,
                        "ai_enhanced": False,
                        "constraint_type": "fallback"
                    })
            else:
                processed_constraints.append(constraint)
        
        # 创建内核数据
        core_data = {
            "type": "core",
            "axioms": processed_axioms,
            "constraints": processed_constraints,
            "extracted_from": f"{work_name}.{sub_name}",
            "ai_enhanced": bool(ai_enhanced_axioms or ai_enhanced_constraints)
        }
        
        # 保存内核数据
        import json
        with open(work_path / 'cores' / f'{sub_name}.json', 'w', encoding='utf-8') as f:
            json.dump(core_data, f, ensure_ascii=False, indent=2)
        
        return f"Successfully extracted core {work_name}.{sub_name}"
    
    def persona(self, work_name: str, sub_name: str, traits: List[str], constraints: List[str]):
        """
        人物提取操作 - 定义人物本体身份
        """
        # 获取作品路径
        work_path = get_work_path(work_name)
        if not work_path.exists():
            raise ValueError(f"Work does not exist: {work_name}")
        
        # 确保目录存在
        ensure_work_directories(work_path)
        
        # 检查是否需要AI增强（traits或constraints中包含"AI:"前缀）
        ai_enhanced_traits = [t for t in traits if t.startswith("AI:")]
        ai_enhanced_constraints = [c for c in constraints if c.startswith("AI:")]
        
        processed_traits = []
        processed_constraints = []
        
        # 处理AI增强的特质
        for trait in traits:
            if trait.startswith("AI:"):
                ai_description = trait[3:].strip()
                api_client = get_api_client()
                enhanced_data = api_client.generate_character(ai_description)
                if enhanced_data:
                    processed_traits.append({
                        "original": ai_description,
                        "ai_enhanced": True,
                        "enhanced_data": enhanced_data,
                        "trait_type": "generated"
                    })
                else:
                    processed_traits.append({
                        "original": ai_description,
                        "ai_enhanced": False,
                        "trait_type": "fallback"
                    })
            else:
                processed_traits.append(trait)
        
        # 处理AI增强的约束
        for constraint in constraints:
            if constraint.startswith("AI:"):
                ai_description = constraint[3:].strip()
                api_client = get_api_client()
                enhanced_data = api_client.generate_character(ai_description)
                if enhanced_data:
                    processed_constraints.append({
                        "original": ai_description,
                        "ai_enhanced": True,
                        "enhanced_data": enhanced_data,
                        "constraint_type": "generated"
                    })
                else:
                    processed_constraints.append({
                        "original": ai_description,
                        "ai_enhanced": False,
                        "constraint_type": "fallback"
                    })
            else:
                processed_constraints.append(constraint)
        
        # 创建人物数据
        persona_data = {
            "type": "persona",
            "traits": processed_traits,
            "constraints": processed_constraints,
            "extracted_from": f"{work_name}.{sub_name}",
            "ai_enhanced": bool(ai_enhanced_traits or ai_enhanced_constraints)
        }
        
        # 保存人物数据
        import json
        with open(work_path / 'personas' / f'{sub_name}.json', 'w', encoding='utf-8') as f:
            json.dump(persona_data, f, ensure_ascii=False, indent=2)
        
        return f"Successfully extracted persona {work_name}.{sub_name}"
    
    def mirror(self, work_name: str, sub_name: str, mp: str, r: str, as_sub: str):
        """
        镜像操作 - 创建命运变体
        """
        # 获取作品路径
        work_path = get_work_path(work_name)
        if not work_path.exists():
            raise ValueError(f"Work does not exist: {work_name}")
        
        # 确保目录存在
        ensure_work_directories(work_path)
        
        # 检查源人物是否存在
        source_persona_path = work_path / 'personas' / f'{mp}.json'
        if not source_persona_path.exists():
            raise ValueError(f"Source persona does not exist: {mp}")
        
        # 读取源人物数据
        import json
        with open(source_persona_path, 'r', encoding='utf-8') as f:
            source_data = json.load(f)
        
        # 创建镜像人物数据
        mirror_data = {
            "type": "persona",
            "mirror_of": mp,
            "fate_change": r,
            "variant_name": as_sub,
            "base_data": source_data,
            "mirrored_from": f"{work_name}.{sub_name}"
        }
        
        # 保存镜像人物数据
        with open(work_path / 'personas' / f'{as_sub}.json', 'w', encoding='utf-8') as f:
            json.dump(mirror_data, f, ensure_ascii=False, indent=2)
        
        return f"Successfully created mirror {work_name}.{as_sub} from {mp}"
    
    def transmute(self, work_name: str, sub_name: str, toas: str, rcd: str):
        """
        转义操作 - 派生新作品，保留血缘
        """
        # 获取源作品路径
        source_path = get_work_path(work_name)
        if not source_path.exists():
            raise ValueError(f"Source work does not exist: {work_name}")
        
        # 获取目标作品路径
        target_path = get_work_path(toas, is_temp=False)
        if target_path.exists():
            raise ValueError(f"Target work already exists: {toas}")
        
        # 复制整个作品目录
        shutil.copytree(source_path, target_path)
        
        # 更新清单文件，添加血缘信息
        manifest_path = target_path / 'manifest.json'
        import json
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        manifest['name'] = toas
        manifest['transmuted_from'] = work_name
        manifest['lineage_desc'] = rcd
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        
        return f"Successfully transmuted {work_name}.{sub_name} to {toas}"
    
    def run(self, work_name: str, sub_name: str, when: Any, then: str, outcome: Dict[str, Any]):
        """
        推演操作 - 原生情节发展
        """
        # 获取作品路径
        work_path = get_work_path(work_name)
        if not work_path.exists():
            raise ValueError(f"Work does not exist: {work_name}")
        
        # 检查是否需要AI增强（then以"AI:"开头）
        ai_enhanced = then.startswith("AI:")
        if ai_enhanced:
            ai_context = then[3:].strip()  # 移除"AI:"前缀
            api_client = get_api_client()
            
            # 获取作品上下文
            context_info = self._get_work_context(work_name, sub_name)
            
            # 生成情节事件
            enhanced_event = api_client.generate_plot_event(context_info, ai_context)
            if enhanced_event:
                run_data = {
                    "type": "run",
                    "when_condition": str(when) if when else "always",
                    "then_event": ai_context,
                    "ai_enhanced": True,
                    "enhanced_event": enhanced_event,
                    "outcome": outcome,
                    "executed_in": f"{work_name}.{sub_name}",
                    "executed_at": str(Path.home() / '.chenmo')
                }
            else:
                # 如果AI生成失败，使用原始事件
                run_data = {
                    "type": "run",
                    "when_condition": str(when) if when else "always",
                    "then_event": ai_context,
                    "ai_enhanced": False,
                    "outcome": outcome,
                    "executed_in": f"{work_name}.{sub_name}",
                    "executed_at": str(Path.home() / '.chenmo')
                }
        else:
            # 非AI增强模式
            run_data = {
                "type": "run",
                "when_condition": str(when) if when else "always",
                "then_event": then,
                "ai_enhanced": False,
                "outcome": outcome,
                "executed_in": f"{work_name}.{sub_name}",
                "executed_at": str(Path.home() / '.chenmo')
            }
        
        # 确保目录存在
        ensure_work_directories(work_path)
        
        # 保存推演结果
        import json
        run_file_path = work_path / 'novies' / f'{sub_name}_run.json'
        with open(run_file_path, 'w', encoding='utf-8') as f:
            json.dump(run_data, f, ensure_ascii=False, indent=2)
        
        return f"Successfully ran scenario {then} in {work_name}.{sub_name}"
    
    def _get_work_context(self, work_name: str, sub_name: str) -> str:
        """
        获取作品上下文信息，用于AI生成
        """
        work_path = get_work_path(work_name)
        context_parts = []
        
        # 添加作品描述（如果存在）
        novies_path = work_path / 'novies' / f'{sub_name}.json'
        if novies_path.exists():
            with open(novies_path, 'r', encoding='utf-8') as f:
                import json
                novies_data = json.load(f)
                if 'description' in novies_data:
                    context_parts.append(f"作品描述: {novies_data['description']}")
                if 'enhanced_data' in novies_data:
                    context_parts.append(f"AI增强数据: {novies_data['enhanced_data']}")
        
        # 添加人物信息（如果存在）
        personas_dir = work_path / 'personas'
        if personas_dir.exists():
            for persona_file in personas_dir.glob('*.json'):
                with open(persona_file, 'r', encoding='utf-8') as f:
                    persona_data = json.load(f)
                    if 'name' in persona_data:
                        context_parts.append(f"人物: {persona_data['name']}")
        
        # 添加内核信息（如果存在）
        cores_dir = work_path / 'cores'
        if cores_dir.exists():
            for core_file in cores_dir.glob('*.json'):
                with open(core_file, 'r', encoding='utf-8') as f:
                    core_data = json.load(f)
                    if 'axioms' in core_data:
                        context_parts.append(f"公理: {core_data['axioms']}")
                    if 'constraints' in core_data:
                        context_parts.append(f"约束: {core_data['constraints']}")
        
        return " | ".join(context_parts) if context_parts else f"作品: {work_name}, 子模块: {sub_name}"
    
    def inspect(self, work_name: str, sub_name: str, target: str):
        """
        查看操作 - 返回指定实体的结构化元数据
        """
        # 获取作品路径
        work_path = get_work_path(work_name)
        if not work_path.exists():
            raise ValueError(f"Work does not exist: {work_name}")
        
        # 根据目标类型获取文件路径
        file_path = get_storage_path(work_name, sub_name, target)
        
        # 读取并返回数据
        import json
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        else:
            return {"error": f"Entity {work_name}.{sub_name} with target '{target}' not found"}