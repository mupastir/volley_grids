"""Setup script for the package. Use the GITHUB_REF_NAME environment variable as the version."""
import os

from setuptools import setup

setup(version=os.getenv('GITHUB_REF_NAME', 'patch'))
