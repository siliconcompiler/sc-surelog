#!/usr/bin/env python3

import glob
import os
from setuptools import find_packages
from setuptools import setup
from setuptools.dist import Distribution

# Hack to get version number since it's considered bad practice to import your
# own package in setup.py. This call defines keys 'version', 'authors', and
# 'banner' in the `metadata` dict.
metadata = {}
with open('sc_surelog/__init__.py') as f:
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


def get_package_data(item, package):
    '''Used to compensate for poor glob support in package_data'''
    package_data = []
    for f in glob.glob(f'{package}/{item}/**/*', recursive=True):
        if os.path.isfile(f):
            # strip off directory and add to list
            package_data.append(f[len(package + '/'):])
    return package_data


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
    version=metadata['version'],
    packages=find_packages(where='.', exclude=['tests*']),

    # TODO: hack to work around weird scikit-build behavior:
    # https://github.com/scikit-build/scikit-build/issues/590
    # Once this issue is resolved, we should switch to setting
    # include_package_data to True instead of manually specifying package_data.

    # include_package_data=True,
    package_data={
        'sc_surelog': get_package_data('sc_surelog')
    },

    python_requires=">=3.8",
    install_requires=install_reqs,
    extras_require=extras_req,
    distclass=BinaryDistribution
)
