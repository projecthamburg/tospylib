from setuptools import setup, find_packages

setup(
    name='tospylib',
    version='0.1.0',
    description='Thinkscript to Python technical indicator library for pandas.',
    author='Your Name',
    packages=find_packages(),
    install_requires=[
        'pandas>=1.0.0',
        'numpy>=1.18.0'
    ],
)
