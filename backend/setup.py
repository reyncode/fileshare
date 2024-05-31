import os
from setuptools import setup

setup(
    version=os.getenv("PROJECT_VERSION", "0.0.1")
)
