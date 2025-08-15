#!/usr/bin/env python3
"""
Setup script for TuxTray
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text() if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text().strip().split('\n')

setup(
    name="tuxtray",
    version="1.0.0",
    author="Aravind Lal",
    author_email="",
    description="An ultra-cute system tray penguin that reacts to system resource usage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aravindlal/TuxTray",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'tuxtray=src.main:main',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment",
        "Topic :: System :: Monitoring",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10",
    include_package_data=True,
    package_data={
        "": ["assets/**/*"],
    },
)
