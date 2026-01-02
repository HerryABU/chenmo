"""
chenmo - 可编程元叙事引擎
Deploy, Register, Mix, Inspect, and Reason with Structured Fictional Universes
"""
import os
import json
import shutil
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import tempfile


class Chenmo:
    """
    `chenmo` 是一个面向高设定密度虚构世界的 Python DSL 库。
    它允许用精确的类 Python 语句操控虚构宇宙的全生命周期。
    """
    
    def __init__(self):
        # 设置基础路径
        self.base_path = Path.home() / '.chenmo'
        self.works_path = self.base_path / 'works'
        self.temps_path = self.base_path / 'temps' / 'works'
        
        # 创建必要的目录
        self.works_path.mkdir(parents=True, exist_ok=True)
        self.temps_path.mkdir(parents=True, exist_ok=True)
    
    def _get_work_path(self, work_name: str):
        """获取作品路径，区分持久和临时作品"""
        if work_name.startswith('temps.'):
            # 临时作品路径
            actual_name = work_name.split('.', 1)[1]  # 移除 'temps.' 前缀
            return self.temps_path / actual_name
        else:
            # 持久作品路径
            return self.works_path / work_name
    
    def _ensure_work_dirs(self, work_path: Path):
        """确保作品目录结构存在"""
        (work_path / 'novies').mkdir(parents=True, exist_ok=True)
        (work_path / 'cores').mkdir(parents=True, exist_ok=True)
        (work_path / 'personas').mkdir(parents=True, exist_ok=True)
        (work_path / 'tech').mkdir(parents=True, exist_ok=True)
        
        # 创建 manifest.json 如果不存在
        manifest_path = work_path / 'manifest.json'
        if not manifest_path.exists():
            manifest = {
                "name": work_path.name,
                "version": "1.0",
                "canonical_source": ""
            }
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    def d(self, source_work: str, sub_name: str = 'novies'):
        """
        部署（Deploy） - 从源安装设定包到本地持久空间
        d.[源作品名].[源下名](from="源路径", toas="本地命名")
        """
        class DeployOperation:
            def __init__(self, chenmo_instance, source_work, sub_name):
                self.chenmo_instance = chenmo_instance
                self.source_work = source_work
                self.sub_name = sub_name
            
            def __call__(self, from_path: str = None, toas: str = None, **kwargs):
                # 如果没有指定 toas，默认使用源作品名
                if toas is None:
                    toas = self.source_work
                
                work_path = self.chenmo_instance.works_path / toas
                
                # 检查命名空间冲突
                if work_path.exists():
                    raise ValueError(f"Namespace collision: {toas} already exists")
                
                # 创建作品目录
                self.chenmo_instance._ensure_work_dirs(work_path)
                
                # 模拟从源路径部署（这里简化处理，实际应从 from_path 下载/复制）
                print(f"Deploying {self.source_work}.{self.sub_name} to {work_path}")
                
                return work_path
        
        return DeployOperation(self, source_work, sub_name)
    
    def u(self, work_name: str, sub_name: str = 'novies'):
        """
        更新（Update） - 在已有持久作品上增量合并变更
        u.[本地作品名].[本地下名](from="源路径", merge="策略")
        """
        class UpdateOperation:
            def __init__(self, chenmo_instance, work_name, sub_name):
                self.chenmo_instance = chenmo_instance
                self.work_name = work_name
                self.sub_name = sub_name
            
            def __call__(self, from_path: str, merge: str = "overlay", lo: str = None, to: str = None, toas: str = None, **kwargs):
                if lo is None:
                    # 模式 A：原地更新
                    work_path = self.chenmo_instance._get_work_path(self.work_name)
                    if not work_path.exists():
                        raise ValueError(f"Work {self.work_name} does not exist")
                    
                    print(f"Updating {self.work_name}.{self.sub_name} from {from_path} with merge strategy {merge}")
                else:
                    # 模式 B：分支合并
                    if to is None or toas is None:
                        raise ValueError("Both 'to' and 'toas' must be provided for branch merge")
                    
                    source_path = Path(lo)
                    target_path = Path(to)
                    
                    if target_path.exists():
                        raise ValueError(f"Target path {target_path} already exists")
                    
                    print(f"Merging {self.work_name}.{self.sub_name} from {from_path} to {target_path} with strategy {merge}")
                
                return True
        
        return UpdateOperation(self, work_name, sub_name)
    
    def l(self, work_name: str, sub_name: str = 'novies'):
        """
        注册（Log / Register） - 从零声明新作品、人物、设定或物品
        l.[作品名].[下名](log_works="作品描述", log_person=["人物描述", ...], ...)
        """
        class LogOperation:
            def __init__(self, chenmo_instance, work_name, sub_name):
                self.chenmo_instance = chenmo_instance
                self.work_name = work_name
                self.sub_name = sub_name
            
            def __call__(self, log_works: str = None, log_person: List[str] = None, 
                        log_settings: List[str] = None, log_thing: List[str] = None, **kwargs):
                work_path = self.chenmo_instance._get_work_path(self.work_name)
                
                # 检查命名空间冲突（仅对持久作品）
                if not self.work_name.startswith('temps.') and work_path.exists():
                    raise ValueError(f"Namespace exists: {self.work_name}")
                
                # 创建作品目录
                self.chenmo_instance._ensure_work_dirs(work_path)
                
                # 处理作品描述
                if log_works:
                    novies_path = work_path / 'novies' / f'{self.sub_name}.json'
                    data = {"description": log_works}
                    with open(novies_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                
                # 处理人物
                if log_person:
                    for i, person_desc in enumerate(log_person):
                        person_path = work_path / 'personas' / f'{person_desc.replace(" ", "_").lower()}.json'
                        data = {"description": person_desc}
                        with open(person_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                
                # 处理设定
                if log_settings:
                    for i, setting_desc in enumerate(log_settings):
                        setting_path = work_path / 'cores' / f'{self.sub_name}_{i}.json'
                        data = {"description": setting_desc}
                        with open(setting_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                
                # 处理物品/科技
                if log_thing:
                    for i, thing_desc in enumerate(log_thing):
                        thing_path = work_path / 'tech' / f'{thing_desc.replace(" ", "_").lower()}.json'
                        data = {"description": thing_desc}
                        with open(thing_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"Registered {self.work_name}.{self.sub_name}")
                return work_path
        
        return LogOperation(self, work_name, sub_name)
    
    def x(self, dummy: str):
        """
        混合（Mix） - 按权重融合多源设定，生成新实体
        x.mxd.in(sources=[("作品1", "下名1"), ("作品2", "下名2")], weights=[0.6, 0.4], toas="新实体名")
        """
        class MixOperation:
            def __init__(self, chenmo_instance):
                self.chenmo_instance = chenmo_instance
            
            class MixInOperation:
                def __init__(self, chenmo_instance):
                    self.chenmo_instance = chenmo_instance
                
                def __call__(self, sources: List[tuple], weights: List[float], 
                           target_type: str, toas: str, **kwargs):
                    # 检查源是否存在
                    for source_work, source_sub in sources:
                        source_path = self.chenmo_instance._get_work_path(source_work)
                        if not source_path.exists():
                            raise ValueError(f"Source work {source_work} does not exist")
                    
                    # 检查 toas 是否已存在
                    target_path = self.chenmo_instance.works_path / toas
                    if target_path.exists():
                        raise ValueError(f"Target namespace {toas} already exists")
                    
                    # 创建目标作品
                    self.chenmo_instance._ensure_work_dirs(target_path)
                    
                    # 模拟混合过程
                    mixed_data = {
                        "sources": sources,
                        "weights": weights,
                        "target_type": target_type,
                        "mixed_at": "now"
                    }
                    
                    # 根据目标类型存储
                    if target_type == 'c':
                        target_dir = target_path / 'cores'
                    elif target_type == 'p':
                        target_dir = target_path / 'personas'
                    elif target_type == 't':
                        target_dir = target_path / 'tech'
                    else:
                        raise ValueError(f"Invalid target_type: {target_type}")
                    
                    target_file = target_dir / f'{toas}.json'
                    with open(target_file, 'w', encoding='utf-8') as f:
                        json.dump(mixed_data, f, ensure_ascii=False, indent=2)
                    
                    print(f"Mixed sources into new entity: {toas}")
                    return target_path
            
            def in_(self):
                return self.MixInOperation(self.chenmo_instance)
        
        return MixOperation(self)
    
    def f(self, work_name: str, sub_name: str = 'novies'):
        """
        实例化（Fabricate） - 动态生成作品实例
        f.[作品名].[下名](setting="描述字符串")
        """
        class FabricateOperation:
            def __init__(self, chenmo_instance, work_name, sub_name):
                self.chenmo_instance = chenmo_instance
                self.work_name = work_name
                self.sub_name = sub_name
            
            def __call__(self, setting: str, **kwargs):
                work_path = self.chenmo_instance.works_path / self.work_name
                
                # 检查命名空间冲突
                if work_path.exists():
                    raise ValueError(f"Work {self.work_name} already exists")
                
                # 创建作品目录
                self.chenmo_instance._ensure_work_dirs(work_path)
                
                # 创建基础设定
                novies_path = work_path / 'novies' / f'{self.sub_name}.json'
                data = {"setting": setting}
                with open(novies_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"Fabricated work: {self.work_name} with setting: {setting}")
                return work_path
        
        return FabricateOperation(self, work_name, sub_name)
    
    def c(self, work_name: str, sub_name: str = 'novies'):
        """
        内核提取（Core） - 定义或提取底层法则
        c.[作品名].[下名](axioms=["公理1", "公理2"], constraints=["约束1", "约束2"])
        """
        class CoreOperation:
            def __init__(self, chenmo_instance, work_name, sub_name):
                self.chenmo_instance = chenmo_instance
                self.work_name = work_name
                self.sub_name = sub_name
            
            def __call__(self, axioms: List[str] = None, constraints: List[str] = None, **kwargs):
                work_path = self.chenmo_instance._get_work_path(self.work_name)
                
                # 确保作品存在
                self.chenmo_instance._ensure_work_dirs(work_path)
                
                # 创建内核数据
                core_data = {
                    "axioms": axioms or [],
                    "constraints": constraints or []
                }
                
                core_path = work_path / 'cores' / f'{self.sub_name}.json'
                with open(core_path, 'w', encoding='utf-8') as f:
                    json.dump(core_data, f, ensure_ascii=False, indent=2)
                
                print(f"Created core {self.work_name}.{self.sub_name}")
                return core_path
        
        return CoreOperation(self, work_name, sub_name)
    
    def p(self, work_name: str, sub_name: str = 'novies'):
        """
        人物提取（Persona） - 定义人物本体身份
        p.[作品名].[下名](traits=["特质1", "特质2"], constraints=["不可为行为1", "不可为行为2"])
        """
        class PersonaOperation:
            def __init__(self, chenmo_instance, work_name, sub_name):
                self.chenmo_instance = chenmo_instance
                self.work_name = work_name
                self.sub_name = sub_name
            
            def __call__(self, traits: List[str] = None, constraints: List[str] = None, **kwargs):
                work_path = self.chenmo_instance._get_work_path(self.work_name)
                
                # 确保作品存在
                self.chenmo_instance._ensure_work_dirs(work_path)
                
                # 创建人物数据
                persona_data = {
                    "traits": traits or [],
                    "constraints": constraints or []
                }
                
                persona_path = work_path / 'personas' / f'{self.sub_name}.json'
                with open(persona_path, 'w', encoding='utf-8') as f:
                    json.dump(persona_data, f, ensure_ascii=False, indent=2)
                
                print(f"Created persona {self.work_name}.{self.sub_name}")
                return persona_path
        
        return PersonaOperation(self, work_name, sub_name)
    
    def m(self, work_name: str, sub_name: str = 'novies'):
        """
        镜像（Mirror） - 创建命运变体
        m.[作品名].[下名](mp="源人物名", r="命运变更描述", as_sub="新镜像名")
        """
        class MirrorOperation:
            def __init__(self, chenmo_instance, work_name, sub_name):
                self.chenmo_instance = chenmo_instance
                self.work_name = work_name
                self.sub_name = sub_name
            
            def __call__(self, mp: str, r: str, as_sub: str, **kwargs):
                work_path = self.chenmo_instance._get_work_path(self.work_name)
                
                # 检查源人物是否存在
                source_path = work_path / 'personas' / f'{mp}.json'
                if not source_path.exists():
                    raise ValueError(f"Source persona {mp} does not exist in {self.work_name}")
                
                # 创建镜像数据（基于源人物）
                with open(source_path, 'r', encoding='utf-8') as f:
                    source_data = json.load(f)
                
                mirror_data = {
                    **source_data,
                    "mirror_of": mp,
                    "fate_change": r,
                    "variant_name": as_sub
                }
                
                mirror_path = work_path / 'personas' / f'{as_sub}.json'
                with open(mirror_path, 'w', encoding='utf-8') as f:
                    json.dump(mirror_data, f, ensure_ascii=False, indent=2)
                
                print(f"Created mirror {as_sub} from {mp} in {self.work_name}")
                return mirror_path
        
        return MirrorOperation(self, work_name, sub_name)
    
    def t(self, source_work: str, source_sub: str = 'novies'):
        """
        转义（Transmute） - 派生新作品，保留血缘
        t.[源作品名].[源下名](toas="新作品名", rcd="血缘描述")
        """
        class TransmuteOperation:
            def __init__(self, chenmo_instance, source_work, source_sub):
                self.chenmo_instance = chenmo_instance
                self.source_work = source_work
                self.source_sub = source_sub
            
            def __call__(self, toas: str, rcd: str, **kwargs):
                source_path = self.chenmo_instance._get_work_path(self.source_work)
                if not source_path.exists():
                    raise ValueError(f"Source work {self.source_work} does not exist")
                
                target_path = self.chenmo_instance.works_path / toas
                if target_path.exists():
                    raise ValueError(f"Target work {toas} already exists")
                
                # 复制整个作品目录
                shutil.copytree(source_path, target_path)
                
                # 更新 manifest.json 以包含血缘信息
                manifest_path = target_path / 'manifest.json'
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    manifest = json.load(f)
                
                manifest['bloodline'] = rcd
                manifest['derived_from'] = self.source_work
                
                with open(manifest_path, 'w', encoding='utf-8') as f:
                    json.dump(manifest, f, ensure_ascii=False, indent=2)
                
                print(f"Transmuted {self.source_work} to {toas} with bloodline {rcd}")
                return target_path
        
        return TransmuteOperation(self, source_work, source_sub)
    
    def r(self, work_name: str, sub_name: str = 'novies'):
        """
        推演（Run） - 仅用于原生情节发展
        r.[作品名].[下名](when=<条件表达式>, then="情节事件ID", outcome={...})
        """
        class RunOperation:
            def __init__(self, chenmo_instance, work_name, sub_name):
                self.chenmo_instance = chenmo_instance
                self.work_name = work_name
                self.sub_name = sub_name
            
            def __call__(self, when=None, then: str = None, outcome: dict = None, **kwargs):
                work_path = self.chenmo_instance._get_work_path(self.work_name)
                if not work_path.exists():
                    raise ValueError(f"Work {self.work_name} does not exist")
                
                # 模拟推演过程
                print(f"Running narrative evolution for {self.work_name}.{self.sub_name}")
                print(f"  Condition: {when}")
                print(f"  Event: {then}")
                if outcome:
                    print(f"  Outcome: {outcome}")
                
                # 记录推演事件
                narrative_log_path = work_path / 'novies' / 'narrative_log.json'
                log_entry = {
                    "event": then,
                    "condition": str(when),
                    "outcome": outcome or {},
                    "timestamp": "now"
                }
                
                # 读取现有日志或创建新日志
                if narrative_log_path.exists():
                    with open(narrative_log_path, 'r', encoding='utf-8') as f:
                        log = json.load(f)
                else:
                    log = []
                
                log.append(log_entry)
                
                with open(narrative_log_path, 'w', encoding='utf-8') as f:
                    json.dump(log, f, ensure_ascii=False, indent=2)
                
                return log_entry
        
        return RunOperation(self, work_name, sub_name)
    
    def i(self, work_name: str, sub_name: str = 'novies'):
        """
        查看（Inspect） - 返回指定实体的结构化元数据
        i.[作品名].[下名](target='c' | 'p' | 'm')
        """
        class InspectOperation:
            def __init__(self, chenmo_instance, work_name, sub_name):
                self.chenmo_instance = chenmo_instance
                self.work_name = work_name
                self.sub_name = sub_name
            
            def __call__(self, target: str = 'p', **kwargs):
                work_path = self.chenmo_instance._get_work_path(self.work_name)
                if not work_path.exists():
                    raise ValueError(f"Work {self.work_name} does not exist")
                
                # 根据目标类型查找文件
                if target == 'c':
                    target_dir = work_path / 'cores'
                    target_file = target_dir / f'{self.sub_name}.json'
                elif target == 'p':
                    target_dir = work_path / 'personas'
                    target_file = target_dir / f'{self.sub_name}.json'
                elif target == 'm':
                    # 镜像也是人物的一种，所以仍在 personas 目录
                    target_dir = work_path / 'personas'
                    target_file = target_dir / f'{self.sub_name}.json'
                else:
                    raise ValueError(f"Invalid target type: {target}")
                
                if not target_file.exists():
                    raise ValueError(f"Entity {self.work_name}.{self.sub_name} ({target}) does not exist")
                
                with open(target_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"Inspected {self.work_name}.{self.sub_name} ({target}): {data}")
                return data
        
        return InspectOperation(self, work_name, sub_name)


# 创建全局实例
chenmo = Chenmo()

class ChenmoOperation:
    """
    支持链式调用的操作类，如 l.temps.cyber_noir.novies
    """
    def __init__(self, chenmo_instance, operation_func):
        self.chenmo_instance = chenmo_instance
        self.operation_func = operation_func
        self.path_parts = []

    def __getattr__(self, name):
        self.path_parts.append(name)
        return self

    def __call__(self, *args, **kwargs):
        if len(self.path_parts) < 2:
            raise ValueError("Path must have at least work_name and sub_name")
        
        # 最后一部分是 sub_name，前面的是 work_name（可能包含 temps. 前缀）
        sub_name = self.path_parts[-1]
        work_name = '.'.join(self.path_parts[:-1])
        
        op_func = self.operation_func(work_name, sub_name)
        return op_func(*args, **kwargs)


# 为方便使用，创建操作别名，支持链式调用
d = lambda: ChenmoOperation(chenmo, chenmo.d)
u = lambda: ChenmoOperation(chenmo, chenmo.u)
l = lambda: ChenmoOperation(chenmo, chenmo.l)
x = lambda: ChenmoOperation(chenmo, chenmo.x)
f = lambda: ChenmoOperation(chenmo, chenmo.f)
c = lambda: ChenmoOperation(chenmo, chenmo.c)
p = lambda: ChenmoOperation(chenmo, chenmo.p)
m = lambda: ChenmoOperation(chenmo, chenmo.m)
t = lambda: ChenmoOperation(chenmo, chenmo.t)
r = lambda: ChenmoOperation(chenmo, chenmo.r)
i = lambda: ChenmoOperation(chenmo, chenmo.i)

# 创建实例以便使用
d = d()
u = u()
l = l()
x = x()
f = f()
c = c()
p = p()
m = m()
t = t()
r = r()
i = i()