import os

from setuptools import setup

setup(version=os.getenv('CI_COMMIT_TAG', 'patch'))
