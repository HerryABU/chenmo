"""
chenmo 包安装配置
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chenmo",
    version="1.0.0",
    author="You",
    author_email="you@example.com",
    description="可编程元叙事引擎 - Deploy, Register, Mix, Inspect, and Reason with Structured Fictional Universes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/chenmo",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        # 无外部依赖，这是一个纯Python库
    ],
)