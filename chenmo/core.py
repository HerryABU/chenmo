"""
chenmo 核心引擎实现
"""
import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from .utils import ensure_chenmo_dir, is_temp_work, get_work_path, validate_namespace
from .storage import StorageManager
from .operations import OperationManager


class ChenmoEngine:
    """
    chenmo 核心引擎
    负责管理所有操作和数据存储
    """
    
    def __init__(self):
        # 初始化存储管理器
        self.storage = StorageManager()
        # 初始化操作管理器
        self.operations = OperationManager(self.storage)
        
        # 设置基础路径
        self.base_path = Path.home() / '.chenmo'
        ensure_chenmo_dir(self.base_path)
        
        # 操作接口映射
        self._ops = {
            'd': lambda work_name, sub_name='novies': self.deploy(work_name, sub_name),      # 部署
            'u': lambda work_name, sub_name='novies': self.update(work_name, sub_name),      # 更新
            'l': lambda work_name, sub_name='novies': self.register(work_name, sub_name),    # 注册
            'x': lambda work_name, sub_name='novies': self.mix(work_name, sub_name),         # 混合
            'f': lambda work_name, sub_name='novies': self.fabricate(work_name, sub_name),   # 实例化
            'c': lambda work_name, sub_name='novies': self.core(work_name, sub_name),        # 内核提取
            'p': lambda work_name, sub_name='novies': self.persona(work_name, sub_name),     # 人物提取
            'm': lambda work_name, sub_name='novies': self.mirror(work_name, sub_name),      # 镜像
            't': lambda work_name, sub_name='novies': self.transmute(work_name, sub_name),   # 转义
            'r': lambda work_name, sub_name='novies': self.run(work_name, sub_name),         # 推演
            'i': lambda work_name, sub_name='novies': self.inspect(work_name, sub_name),     # 查看
        }
    
    def deploy(self, work_name: str, sub_name: str = 'novies'):
        """
        部署（Deploy）- 从源安装设定包到本地持久空间
        d.[源作品名].[源下名](from="源路径", toas="本地命名")
        """
        def deploy_func(**kwargs):
            source_from = kwargs.get('from', None)
            toas = kwargs.get('toas', work_name)
            
            # 验证命名空间
            if not validate_namespace(toas):
                raise ValueError(f"Invalid namespace: {toas}")
                
            # 检查是否已存在
            work_path = get_work_path(toas, is_temp=False)
            if work_path.exists():
                raise ValueError(f"Namespace collision: {toas} already exists")
            
            # 执行部署逻辑
            return self.operations.deploy(work_name, sub_name, source_from, toas)
        
        return deploy_func
    
    def update(self, work_name: str, sub_name: str = 'novies'):
        """
        更新（Update）- 在已有持久作品上增量合并变更
        u.[本地作品名].[本地下名](from="源路径", merge="策略", lo="本地源", to="目标路径", toas="新作品名")
        """
        def update_func(**kwargs):
            source_from = kwargs.get('from', None)
            merge_strategy = kwargs.get('merge', 'overlay')
            local_origin = kwargs.get('lo', None)
            target_path = kwargs.get('to', None)
            toas = kwargs.get('toas', work_name)
            
            return self.operations.update(work_name, sub_name, source_from, 
                                        merge_strategy, local_origin, target_path, toas)
        
        return update_func
    
    def register(self, work_name: str, sub_name: str = 'novies'):
        """
        注册（Log / Register）- 从零声明新作品、人物、设定或物品
        l.[作品名].[下名](log_works="作品描述", log_person=["人物描述"], log_settings=["设定描述"], log_thing=["物品描述"])
        """
        def register_func(**kwargs):
            log_works = kwargs.get('log_works', None)
            log_person = kwargs.get('log_person', [])
            log_settings = kwargs.get('log_settings', [])
            log_thing = kwargs.get('log_thing', [])
            
            return self.operations.register(work_name, sub_name, log_works, 
                                          log_person, log_settings, log_thing)
        
        return register_func
    
    def mix(self, work_name: str, sub_name: str = 'novies'):
        """
        混合（Mix）- 按权重融合多源设定，生成新实体
        x.mxd.in(sources=[("作品1", "下名1"), ("作品2", "下名2")], weights=[0.6, 0.4], target_type="c|p|t", toas="新实体名")
        """
        def mix_func(**kwargs):
            sources = kwargs.get('sources', [])
            weights = kwargs.get('weights', [])
            target_type = kwargs.get('target_type', 'c')
            toas = kwargs.get('toas', f"mixed_{len(sources)}")
            
            return self.operations.mix(sources, weights, target_type, toas)
        
        return mix_func
    
    def fabricate(self, work_name: str, sub_name: str = 'novies'):
        """
        实例化（Fabricate）- 动态生成作品实例
        f.[作品名].[下名](setting="描述字符串")
        """
        def fabricate_func(**kwargs):
            setting = kwargs.get('setting', '')
            
            return self.operations.fabricate(work_name, sub_name, setting)
        
        return fabricate_func
    
    def core(self, work_name: str, sub_name: str = 'novies'):
        """
        内核提取（Core）- 定义或提取底层法则
        c.[作品名].[下名](axioms=["公理1", "公理2"], constraints=["约束1", "约束2"])
        """
        def core_func(**kwargs):
            axioms = kwargs.get('axioms', [])
            constraints = kwargs.get('constraints', [])
            
            return self.operations.core(work_name, sub_name, axioms, constraints)
        
        return core_func
    
    def persona(self, work_name: str, sub_name: str = 'novies'):
        """
        人物提取（Persona）- 定义人物本体身份
        p.[作品名].[下名](traits=["特质1", "特质2"], constraints=["不可为行为1", "不可为行为2"])
        """
        def persona_func(**kwargs):
            traits = kwargs.get('traits', [])
            constraints = kwargs.get('constraints', [])
            
            return self.operations.persona(work_name, sub_name, traits, constraints)
        
        return persona_func
    
    def mirror(self, work_name: str, sub_name: str = 'novies'):
        """
        镜像（Mirror）- 创建命运变体
        m.[作品名].[下名](mp="源人物名", r="命运变更描述", as_sub="新镜像名")
        """
        def mirror_func(**kwargs):
            mp = kwargs.get('mp', '')
            r = kwargs.get('r', '')
            as_sub = kwargs.get('as_sub', f"{sub_name}_mirror")
            
            return self.operations.mirror(work_name, sub_name, mp, r, as_sub)
        
        return mirror_func
    
    def transmute(self, work_name: str, sub_name: str = 'novies'):
        """
        转义（Transmute）- 派生新作品，保留血缘
        t.[源作品名].[源下名](toas="新作品名", rcd="血缘描述")
        """
        def transmute_func(**kwargs):
            toas = kwargs.get('toas', f"{work_name}_transmuted")
            rcd = kwargs.get('rcd', f"derived from {work_name}.{sub_name}")
            
            return self.operations.transmute(work_name, sub_name, toas, rcd)
        
        return transmute_func
    
    def run(self, work_name: str, sub_name: str = 'novies'):
        """
        推演（Run）- 原生情节发展
        r.[作品名].[下名](when=<条件表达式>, then="情节事件ID", outcome={...})
        """
        def run_func(**kwargs):
            when = kwargs.get('when', None)
            then = kwargs.get('then', '')
            outcome = kwargs.get('outcome', {})
            
            return self.operations.run(work_name, sub_name, when, then, outcome)
        
        return run_func
    
    def inspect(self, work_name: str, sub_name: str = 'novies'):
        """
        查看（Inspect）- 返回指定实体的结构化元数据
        i.[作品名].[下名](target='c' | 'p' | 'm')
        """
        def inspect_func(**kwargs):
            target = kwargs.get('target', 'c')
            
            return self.operations.inspect(work_name, sub_name, target)
        
        return inspect_func

    def __getattr__(self, op_code: str):
        """允许通过属性访问操作方法"""
        if op_code in self._ops:
            return OperationChain(self._ops[op_code])
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{op_code}'")


class OperationChain:
    """
    操作链，支持 work_name.sub_name(...) 的语法
    """
    def __init__(self, operation_func):
        self.operation_func = operation_func

    def __getattr__(self, work_name: str):
        """捕获作品名，返回一个 WorkChain 对象"""
        return WorkChain(self.operation_func, work_name)


class WorkChain:
    """
    作品链，支持 sub_name(...) 的语法
    """
    def __init__(self, operation_func, work_name):
        self.operation_func = operation_func
        self.work_name = work_name

    def __getattr__(self, sub_name: str):
        """捕获下名，返回一个可调用对象或特殊链对象"""
        # 特殊处理混合操作 x.mxd.in
        if sub_name == 'mxd':
            return MixChain(self.operation_func)
        else:
            def callable_func(**kwargs):
                return self.operation_func(self.work_name, sub_name)(**kwargs)
            return callable_func


class MixChain:
    """
    混合操作链，处理 x.mxd.in 语法
    """
    def __init__(self, operation_func):
        self.operation_func = operation_func

    def __getattr__(self, sub_name: str):
        """处理 in 方法"""
        if sub_name == 'in':
            def callable_func(**kwargs):
                # 对于混合操作，work_name 为 'mxd'，sub_name 为 'in'
                return self.operation_func('mxd', 'in')(**kwargs)
            return callable_func
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{sub_name}'")