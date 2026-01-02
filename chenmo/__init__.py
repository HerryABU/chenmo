"""
chenmo - 可编程元叙事引擎
Deploy, Register, Mix, Inspect, and Reason with Structured Fictional Universes
"""

from .core import ChenmoEngine
from . import config

__version__ = "1.0.0"
__author__ = "You"

# 初始化引擎实例
engine = ChenmoEngine()

# 导出操作接口
d = engine.d  # 部署
u = engine.u  # 更新
l = engine.l  # 注册
x = engine.x  # 混合
f = engine.f  # 实例化
c = engine.c  # 内核提取
p = engine.p  # 人物提取
m = engine.m  # 镜像
t = engine.t  # 转义
r = engine.r  # 推演
i = engine.i  # 查看