from setuptools import setup, find_packages

setup(
    name="tospylib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.21",
        "pandas>=1.4"
    ],
    python_requires=">=3.7",
    author="ProjectHamburg",
    description="Faithful Thinkscript-to-Python technical indicators for pandas/numpy.",
    url="https://github.com/projecthamburg/tospylib",
) 