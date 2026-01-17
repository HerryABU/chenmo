"""
可编程元叙事引擎 - chenmo
Deploy, Register, Mix, Inspect, Reason, Import, Search, Generate, Update, and Output Structured Fictional Universes
"""

import os
import json
from pathlib import Path

# 创建主类和操作接口
from .core import ChenmoEngine
from .operations import Operations
from .llm_interface import LLMInterface
from .storage import StorageManager

# 初始化引擎
engine = ChenmoEngine()
ops = Operations(engine)
storage = StorageManager()

# DSL 操作接口 - 使用代理来支持点操作符语法
d = ops.deploy_proxy()  # 部署
u = ops.update_proxy()  # 更新
l = ops.register_proxy()  # 注册
x = ops.mix_proxy()  # 混合
f = ops.fabricate_proxy()  # 实例化
c = ops.core_extract_proxy()  # 内核提取
p = ops.persona_extract_proxy()  # 人物提取
m = ops.mirror_proxy()  # 镜像
t = ops.transmute_proxy()  # 转义
r = ops.run_proxy()  # 推演
i = ops.inspect_proxy()  # 查看
s = ops.search_proxy()  # 搜索

# LLM 接口
llm = LLMInterface

# 输出接口
def print_func(content, to=None, format="narrative", merge="strict"):
    """
    智能输出与更新接口
    """
    from .utils import print_content
    return print_content(content, to, format, merge)

# CLI 快速引用接口
def frm(identifier):
    """设置当前工作标识符"""
    engine.set_current_work(identifier)
    return identifier

def inport(entity, as_alias=None):
    """导入实体"""
    return engine.import_entity(entity, as_alias)

# 导出主要接口
__all__ = ['d', 'u', 'l', 'x', 'f', 'c', 'p', 'm', 't', 'r', 'i', 's', 'llm', 'print', 'frm', 'inport']

# 设置别名
print = print_func