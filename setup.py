"""
S1-InSAR-Pipeline-EastKorea Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="s1-insar-pipeline",
    version="0.1.0",
    author="wukdddang",
    description="Sentinel-1 SLC 데이터를 활용한 한반도 동남권 지표 변위 모니터링 파이프라인",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wukdddang/S1-InSAR-Pipeline-EastKorea",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: GIS",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            's1-retrieve=src.data_retrieval:main',
        ],
    },
)
