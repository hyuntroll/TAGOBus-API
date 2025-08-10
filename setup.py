from setuptools import setup, find_packages

setup(
    name="UnOffical_TAGO_API",
    version="0.10",
    description="Unofficial Python wrapper for TAGO Bus API",
    url="https://github.com/hyuntroll/TAGOBus-API",
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "xmltodict"
    ],
    license='MIT',
    author='hyuntroll',
    author_email="hsm200905292@gmail.com"
)