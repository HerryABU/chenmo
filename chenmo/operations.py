"""
操作模块
实现各种DSL操作：d, u, l, x, f, c, p, m, t, r, i, s
"""
import json
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from .core import ChenmoEngine
from .storage import StorageManager


class OperationProxy:
    """操作代理类，用于支持DSL语法: op.work.subname(...)"""
    
    def __init__(self, operation_func, work_name: str = None, sub_name: str = None):
        self.operation_func = operation_func
        self.work_name = work_name
        self.sub_name = sub_name
    
    def __call__(self, *args, **kwargs):
        # 确定work_name - 如果self.work_name为空，第一个参数是work_name
        if self.work_name is None:
            if args:
                work_name = args[0]
                remaining_args = args[1:]
            else:
                raise ValueError("Work name must be provided as first argument")
        else:
            work_name = self.work_name
            remaining_args = args
        
        # 确定sub_name - 如果self.sub_name为空，使用默认值，否则使用已有的sub_name
        if self.sub_name is None:
            # 如果sub_name仍为None，这意味着只有work_name被设置了，而sub_name还未被指定
            # 这种情况下，我们应该使用默认值
            sub_name = "novies"
        else:
            sub_name = self.sub_name
        
        return self.operation_func(work_name, sub_name, *remaining_args, **kwargs)
    
    def __getattr__(self, attr_name: str):
        # 当访问属性时，如果当前work_name为空，说明attr_name是work_name
        # 如果work_name不为空但sub_name为空，说明attr_name是sub_name
        if self.work_name is None:
            # First access: attr_name is the work name
            return OperationProxy(self.operation_func, work_name=attr_name, sub_name=self.sub_name)
        elif self.sub_name is None:
            # Second access: attr_name is the sub name
            return OperationProxy(self.operation_func, work_name=self.work_name, sub_name=attr_name)
        else:
            # If both are already set, accessing another attribute doesn't make sense in this context
            # Return a new proxy with the same function but reset work and sub names
            # This handles cases like chained calls incorrectly
            return OperationProxy(self.operation_func, work_name=attr_name, sub_name=None)


class Operations:
    """操作类"""
    
    def __init__(self, engine: ChenmoEngine):
        self.engine = engine
        self.storage = StorageManager()
        self.storage.initialize_with_engine(engine)
    
    def deploy(self, work_name: str, sub_name: str = "novies", **kwargs):
        """部署操作 - 从源安装设定包到本地持久空间"""
        from_path = kwargs.get('from', None)
        doad = kwargs.get('doad', None)
        to_path = kwargs.get('to', str(self.engine.works_dir))
        toas = kwargs.get('toas', work_name)
        
        # 如果提供了doad，则从官方仓库下载
        if doad:
            # 下载包文件
            package_file = f"/tmp/{doad}.narr"
            # 这里应该实现从官方仓库下载包的逻辑
            # 为了演示，我们创建一个模拟包
            self._create_mock_package(doad, package_file)
            
            # 导入包
            self.storage.import_package(package_file, toas)
            
            # 清理临时文件
            import os
            os.remove(package_file)
            
            return f"Deployed {doad} to {toas}"
        
        # 如果提供了from路径，则复制现有结构
        elif from_path:
            # 实现从指定路径复制的逻辑
            source_path = Path(from_path)
            target_path = self.engine.works_dir / toas
            
            if target_path.exists():
                raise ValueError(f"Namespace collision: {toas} already exists")
            
            import shutil
            shutil.copytree(source_path, target_path)
            
            return f"Deployed from {from_path} to {toas}"
        
        else:
            # 创建新的作品结构
            work_path = self.engine.create_work_structure(toas)
            return f"Created new work structure at {work_path}"
    
    def deploy_proxy(self):
        return OperationProxy(self.deploy)
    
    def update(self, work_name: str, sub_name: str = "novies", **kwargs):
        """更新操作 - 在已有持久作品上增量合并变更"""
        from_path = kwargs.get('from', None)
        local_origin = kwargs.get('lo', None)
        to_path = kwargs.get('to', str(self.engine.get_work_path(work_name)))
        toas = kwargs.get('toas', work_name)
        merge_strategy = kwargs.get('merge', 'overlay')
        
        if not from_path:
            raise ValueError("'from' parameter is required for update operation")
        
        # 如果提供了local origin，进行分支合并
        if local_origin:
            # 获取源数据
            source_path = Path(from_path)
            target_path = self.engine.works_dir / toas
            
            if target_path.exists():
                raise ValueError(f"Namespace collision: {toas} already exists")
            
            # 复制local origin作为基础
            origin_path = Path(local_origin)
            import shutil
            shutil.copytree(origin_path, target_path)
            
            # 合并from_path的数据
            self._merge_directories(source_path, target_path, merge_strategy)
            
            return f"Merged {from_path} into {toas} with strategy {merge_strategy}"
        
        else:
            # 原地更新
            target_path = self.engine.get_work_path(work_name)
            source_path = Path(from_path)
            
            self._merge_directories(source_path, target_path, merge_strategy)
            
            return f"Updated {work_name} with strategy {merge_strategy}"
    
    def update_proxy(self):
        return OperationProxy(self.update)
    
    def _merge_directories(self, src: Path, dst: Path, strategy: str):
        """合并目录"""
        import shutil
        
        for item in src.iterdir():
            dst_item = dst / item.name
            
            if item.is_dir():
                if dst_item.exists() and dst_item.is_dir():
                    # 递归合并子目录
                    self._merge_directories(item, dst_item, strategy)
                else:
                    # 复制新目录
                    shutil.copytree(item, dst_item)
            else:
                # 处理文件
                if dst_item.exists() and strategy != 'overlay':
                    if strategy == 'strict':
                        raise ValueError(f"File conflict: {dst_item}")
                    elif strategy == 'interactive':
                        # 在实际应用中，这里应该询问用户如何处理冲突
                        # 现在我们简单地覆盖
                        pass
                
                # 复制文件
                shutil.copy2(item, dst_item)
    
    def register(self, work_name: str, sub_name: str = "novies", **kwargs):
        """注册操作 - 从零声明新作品、人物、设定或物品"""
        log_works = kwargs.get('log_works', None)
        log_person = kwargs.get('log_person', [])
        log_settings = kwargs.get('log_settings', [])
        log_thing = kwargs.get('log_thing', [])
        
        # 创建作品结构
        work_path = self.engine.create_work_structure(work_name)
        
        # 注册作品描述
        if log_works:
            data = {"description": log_works}
            self.storage.save_work_data(work_name, sub_name, 'novies', data)
        
        # 注册人物
        for person_desc in log_person:
            person_data = {"description": person_desc}
            self.storage.save_work_data(work_name, person_desc.replace(' ', '_').lower(), 'p', person_data)
        
        # 注册设定
        for setting_desc in log_settings:
            if isinstance(setting_desc, str):
                setting_data = {"description": setting_desc}
                self.storage.save_work_data(work_name, setting_desc.replace(' ', '_').lower(), 'c', setting_data)
            else:
                # 如果是复杂对象，可能是从其他地方引用的
                # 这里简化处理
                setting_data = setting_desc
                self.storage.save_work_data(work_name, "referenced_setting", 'c', setting_data)
        
        # 注册物品/科技
        for thing_desc in log_thing:
            thing_data = {"description": thing_desc}
            self.storage.save_work_data(work_name, thing_desc.replace(' ', '_').lower(), 't', thing_data)
        
        return f"Registered new work '{work_name}' with {len(log_person)} persons, {len(log_settings)} settings, {len(log_thing)} things"
    
    def register_proxy(self):
        return OperationProxy(self.register)
    
    def mix(self, work_name: str, sub_name: str = "novies", **kwargs):
        """混合操作 - 按权重融合多源设定，生成新实体"""
        sources = kwargs.get('sources', [])
        weights = kwargs.get('weights', [])
        target_type = kwargs.get('target_type', 'c')
        toas = kwargs.get('toas', f"mixed_{work_name}_{sub_name}")
        
        if len(sources) != len(weights):
            raise ValueError("Number of sources must match number of weights")
        
        if sum(weights) != 1.0:
            # 归一化权重
            total_weight = sum(weights)
            weights = [w / total_weight for w in weights]
        
        # 收集源数据
        combined_data = {}
        for (src_work, src_sub), weight in zip(sources, weights):
            src_data = self.engine.load_entity(src_work, src_sub, target_type)
            if src_data:
                # 简单加权合并（实际应用中可能需要更复杂的合并逻辑）
                for key, value in src_data.items():
                    if key not in combined_data:
                        combined_data[key] = []
                    combined_data[key].append((value, weight))
        
        # 创建混合后的内容
        final_data = {}
        for key, weighted_values in combined_data.items():
            # 对于每个键，按权重合并值
            # 这里简化处理，只取第一个值乘以权重
            if isinstance(weighted_values[0][0], (int, float)):
                final_value = sum(v * w for v, w in weighted_values)
            else:
                # 对于字符串或其他类型，选择权重最高的
                max_weight_idx = max(range(len(weighted_values)), key=lambda i: weighted_values[i][1])
                final_value = weighted_values[max_weight_idx][0]
            
            final_data[key] = final_value
        
        # 保存混合结果
        result_path = self.engine.create_work_structure(toas)
        self.storage.save_work_data(toas, "mixed_result", target_type, final_data)
        
        return f"Mixed {len(sources)} sources into new entity '{toas}'"
    
    def mix_proxy(self):
        return OperationProxy(self.mix)
    
    def fabricate(self, work_name: str, sub_name: str = "novies", **kwargs):
        """实例化操作 - 动态生成作品实例"""
        setting = kwargs.get('setting', '')
        
        work_path = self.engine.create_work_structure(work_name)
        
        # 创建基本设置
        data = {
            "description": setting,
            "created_via": "fabricate"
        }
        self.storage.save_work_data(work_name, sub_name, 'novies', data)
        
        return f"Fabricated new work '{work_name}' with setting: {setting}"
    
    def fabricate_proxy(self):
        return OperationProxy(self.fabricate)
    
    def core_extract(self, work_name: str, sub_name: str = "novies", **kwargs):
        """内核提取操作 - 定义或提取底层法则"""
        axioms = kwargs.get('axioms', [])
        constraints = kwargs.get('constraints', [])
        
        data = {
            "axioms": axioms,
            "constraints": constraints,
            "extracted_from": f"{work_name}.{sub_name}"
        }
        
        self.storage.save_work_data(work_name, sub_name, 'c', data)
        
        return f"Extracted core for {work_name}.{sub_name} with {len(axioms)} axioms and {len(constraints)} constraints"
    
    def core_extract_proxy(self):
        return OperationProxy(self.core_extract)
    
    def persona_extract(self, work_name: str, sub_name: str = "novies", **kwargs):
        """人物提取操作 - 定义人物本体身份"""
        traits = kwargs.get('traits', [])
        constraints = kwargs.get('constraints', [])
        
        data = {
            "traits": traits,
            "constraints": constraints,
            "extracted_from": f"{work_name}.{sub_name}"
        }
        
        self.storage.save_work_data(work_name, sub_name, 'p', data)
        
        return f"Extracted persona for {work_name}.{sub_name} with {len(traits)} traits and {len(constraints)} constraints"
    
    def persona_extract_proxy(self):
        return OperationProxy(self.persona_extract)
    
    def mirror(self, work_name: str, sub_name: str = "novies", **kwargs):
        """镜像操作 - 创建命运变体"""
        source_persona = kwargs.get('mp', '')
        fate_change = kwargs.get('r', '')
        as_sub = kwargs.get('as_sub', f"{sub_name}_mirror")
        
        # 加载源人物数据
        source_data = self.engine.load_entity(work_name, source_persona, 'p')
        if not source_data:
            raise ValueError(f"Source persona {source_persona} does not exist in {work_name}")
        
        # 创建镜像数据（基于源数据修改）
        mirror_data = source_data.copy()
        mirror_data['fate_variant'] = fate_change
        mirror_data['based_on'] = source_persona
        mirror_data['created_via'] = 'mirror'
        
        self.storage.save_work_data(work_name, as_sub, 'm', mirror_data)
        
        return f"Created mirror {as_sub} of {source_persona} with fate change: {fate_change}"
    
    def mirror_proxy(self):
        return OperationProxy(self.mirror)
    
    def transmute(self, source_work: str, source_sub: str = "novies", **kwargs):
        """转义操作 - 派生新作品，保留血缘"""
        toas = kwargs.get('toas', '')
        rcd = kwargs.get('rcd', '')
        
        if not toas:
            raise ValueError("'toas' parameter is required for transmute operation")
        
        # 获取源作品路径
        source_path = self.engine.get_work_path(source_work)
        if not source_path.exists():
            raise ValueError(f"Source work {source_work} does not exist")
        
        # 创建新作品路径
        target_path = self.engine.get_work_path(toas)
        if target_path.exists():
            raise ValueError(f"Namespace collision: {toas} already exists")
        
        # 复制整个作品结构
        import shutil
        shutil.copytree(source_path, target_path)
        
        # 添加血缘元数据
        lineage_data = {
            "original_source": source_work,
            "transmutation_reason": rcd,
            "transmutation_date": str(Path.home() / '.chenmo' / 'timestamp')  # 简化表示
        }
        
        lineage_file = target_path / 'lineage.json'
        with open(lineage_file, 'w', encoding='utf-8') as f:
            json.dump(lineage_data, f, ensure_ascii=False, indent=2)
        
        return f"Transmuted {source_work} to {toas} with lineage record: {rcd}"
    
    def transmute_proxy(self):
        return OperationProxy(self.transmute)
    
    def run(self, work_name: str, sub_name: str = "novies", **kwargs):
        """推演操作 - 原生情节发展"""
        when_condition = kwargs.get('when', None)
        then_event = kwargs.get('then', '')
        outcome = kwargs.get('outcome', {})
        
        # 检查条件是否满足（简化实现）
        condition_met = True  # 在实际实现中，这里应该评估when_condition
        if condition_met:
            # 记录发生的事件
            event_data = {
                "event": then_event,
                "outcome": outcome,
                "triggered_by": f"{work_name}.{sub_name}",
                "timestamp": "placeholder_timestamp"  # 实际应用中应使用真实时间戳
            }
            
            # 保存事件到历史记录
            events_dir = self.engine.get_work_path(work_name) / 'events'
            events_dir.mkdir(exist_ok=True)
            
            import time
            event_filename = f"event_{int(time.time())}_{sub_name.replace(' ', '_')}.json"
            event_path = events_dir / event_filename
            
            with open(event_path, 'w', encoding='utf-8') as f:
                json.dump(event_data, f, ensure_ascii=False, indent=2)
            
            return f"Executed event: {then_event} in {work_name}.{sub_name}"
        else:
            return f"Condition not met for event: {then_event}"
    
    def run_proxy(self):
        return OperationProxy(self.run)
    
    def inspect(self, work_name: str, sub_name: str = "novies", **kwargs):
        """查看操作 - 返回指定实体的结构化元数据"""
        target_type = kwargs.get('target', 'novies')
        
        data = self.engine.load_entity(work_name, sub_name, target_type)
        if data is None:
            return f"No data found for {work_name}.{sub_name} (type: {target_type})"
        
        return data
    
    def inspect_proxy(self):
        return OperationProxy(self.inspect)
    
    def search(self, what: str, work_filter: str = "none", **kwargs):
        """搜索操作 - 搜索官方与本地作品及实体"""
        # 处理关键字参数
        if work_filter == "none":
            work_filter = None
        elif work_filter == what:
            # 这意味着是在使用DSL语法 s.what.what("keyword")
            keyword = work_filter  # 实际的关键词
            work_filter = None
        else:
            keyword = what
        
        # 搜索实体
        results = self.engine.search_entities(keyword, work_filter)
        
        return results
    
    def search_proxy(self):
        return OperationProxy(self.search)
    
    def _create_mock_package(self, package_id: str, package_file: str):
        """创建模拟包文件用于演示"""
        import zipfile
        import tempfile
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 创建模拟作品结构
            work_path = temp_path / package_id
            work_path.mkdir()
            
            # 创建manifest.json
            manifest = {
                "name": package_id,
                "version": "1.0",
                "canonical_source": package_id
            }
            with open(work_path / 'manifest.json', 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
            
            # 创建各个子目录
            (work_path / 'novies').mkdir()
            (work_path / 'cores').mkdir()
            (work_path / 'personas').mkdir()
            (work_path / 'tech').mkdir()
            
            # 创建一些示例文件
            with open(work_path / 'novies' / 'intro.json', 'w', encoding='utf-8') as f:
                json.dump({"description": f"Introductory content for {package_id}"}, f, ensure_ascii=False, indent=2)
            
            # 打包成.narr文件
            with zipfile.ZipFile(package_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(work_path):
                    for file in files:
                        file_path = Path(root) / file
                        arcname = file_path.relative_to(temp_path)
                        zipf.write(file_path, arcname)