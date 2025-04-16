from setuptools import setup, find_packages

setup(
    name="tospylib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
    ],
    python_requires=">=3.6",
    license="Apache-2.0",
) 
