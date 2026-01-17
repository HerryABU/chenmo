from setuptools import setup, find_packages

setup(
    name="chenmo",
    version="2.5.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pyyaml>=6.0",
        "jsonschema>=4.0.0",
        "openai>=1.0.0",
        "ollama>=0.1.0",
    ],
    entry_points={
        'console_scripts': [
            'cm=chenmo.cli:main',
        ],
    },
    author="You",
    description="可编程元叙事引擎 - Deploy, Register, Mix, Inspect, Reason, Import, Search, Generate, Update, and Output Structured Fictional Universes",
    license="MIT",
    keywords="fiction universe narrative engine",
    url="https://github.com/your-repo/chenmo",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)