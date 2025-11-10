# colorara/setup.py

from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

import os
import re

def get_version():
    """Reads the version from the package's __init__.py file."""
    with open(os.path.join('colrs', '__init__.py'), 'r') as f:
        version_match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)
        if version_match:
            return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='colrs',
    version=get_version(),
    author='hussain_syrer',
    author_email='h2311065@gmail.com',
    description='A simple and elegant Python library for terminal text coloring.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/HussainAlkhatib/colrs', # Placeholder URL
    license_files=('LICENSE',),
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
    python_requires='>=3.7',
    keywords='color terminal ansi text style coloring cli print input',
)
