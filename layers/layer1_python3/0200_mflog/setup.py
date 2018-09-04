import fastentrypoints  # noqa: F401
from setuptools import setup
from setuptools import find_packages

setup(
    name='mflog',
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "log = mflog.log:main",
        ]
    }
)
