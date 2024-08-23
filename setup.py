#!/usr/bin/env python3

from setuptools import setup
from setuptools.dist import Distribution

# Hack to get version number since it's considered bad practice to import your
# own package in setup.py. This call defines keys 'version', 'authors', and
# 'banner' in the `metadata` dict.
metadata = {}
with open('surelog/__init__.py') as f:
    exec(f.read(), metadata)

with open("README.md", "r", encoding="utf-8") as readme:
    long_desc = readme.read()


def parse_reqs():
    '''Parse out each requirement category from requirements.txt'''
    install_reqs = []
    extras_reqs = {}
    current_section = None  # default to install

    with open('requirements.txt', 'r') as reqs_file:
        for line in reqs_file.readlines():
            line = line.rstrip('\n')
            if line.startswith('#:'):
                # strip off '#:' prefix to read extras name
                current_section = line[2:]
                if current_section not in extras_reqs:
                    extras_reqs[current_section] = []
            elif not line or line.startswith('#'):
                # skip blanks and comments
                continue
            elif current_section is None:
                install_reqs.append(line)
            else:
                extras_reqs[current_section].append(line)

    return install_reqs, extras_reqs


install_reqs, extras_req = parse_reqs()


# Hack to force cibuildwheels to build a pure python package
# https://stackoverflow.com/a/36886459
class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name"""
    def has_ext_modules(foo):
        return True


setup(
    name="sc-surelog",
    description="Precompiled binary for surelog.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    author="ZeroASIC",
    author_email="gadfort@zeroasic.com",
    url="https://github.com/siliconcompiler/sc-surelog",
    project_urls={
        "Source Code": "https://github.com/siliconcompiler/sc-surelog",
        "Bug Tracker": "https://github.com/siliconcompiler/sc-surelog/issues"
    },
    version=metadata['__version__'],
    packages=['surelog'],

    include_package_data=True,

    python_requires=">=3.8",
    install_requires=install_reqs,
    extras_require=extras_req,
    distclass=BinaryDistribution
)
