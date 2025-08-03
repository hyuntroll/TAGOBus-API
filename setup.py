from setuptools import setup, find_packages

setup(
    name="UnOffical_TAGO_API",
    version="0.3",
    description="test1",
    url="https://github.com/hyuntroll/TAGOBus-API",
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "requests",
        "xmltodict"
    ],
    license='MIT',
    author='hyuntroll',
    author_email="hsm200905292@gmail.com"
)