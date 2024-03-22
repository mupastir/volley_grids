"""Setup script for the package. Use the CI_COMMIT_TAG environment variable as the version."""
import os

from setuptools import setup

setup(version=os.getenv('CI_COMMIT_TAG', 'patch'))
