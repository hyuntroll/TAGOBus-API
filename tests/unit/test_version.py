import re

from tagoapi import __version__


def test_package_version_uses_three_part_semver():
    assert re.fullmatch(r"\d+\.\d+\.\d+", __version__)


def test_current_package_version():
    assert __version__ == "0.14.0"
