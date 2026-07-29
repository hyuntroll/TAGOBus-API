from pathlib import Path

from setuptools import find_packages, setup


PROJECT_ROOT = Path(__file__).parent


def read_version() -> str:
    version_file = PROJECT_ROOT / "src" / "tagoapi" / "_version.py"
    for line in version_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("__version__"):
            return line.split("=", 1)[1].strip().strip("\"'")
    raise RuntimeError("패키지 버전을 찾을 수 없습니다.")


setup(
    name="UnOffical_TAGO_API",
    version=read_version(),
    description="Unofficial Python wrapper for TAGO Bus API",
    url="https://github.com/hyuntroll/TAGOBus-API",
    long_description=(PROJECT_ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[
        "httpx",
        "xmltodict",
    ],
    license="MIT",
    author="hyuntroll",
    author_email="hsm200905292@gmail.com",
)
