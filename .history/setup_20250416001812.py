from setuptools import setup, find_packages

setup(
    name="tospylib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    python_requires=">=3.7",
    description="A Python library for technical analysis and trading indicators",
    author="Mordecai Machazire",
    author_email="",  # Add your email if you wish
    url="https://github.com/mordecaimachazire/tospylib",
) 