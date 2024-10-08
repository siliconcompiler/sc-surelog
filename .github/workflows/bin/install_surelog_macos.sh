#!/bin/bash

# Get directory of setup scripts
src_path=$(cd -- "$(dirname "$0")/../../../siliconcompiler/siliconcompiler/toolscripts" >/dev/null 2>&1 ; pwd -P)

# Install dependencies
pip3 install orderedmultidict
pip3 install cmake

mkdir build

# Install Surelog
git clone $(python3 ${src_path}/_tools.py --tool surelog --field git-url) build/Surelog
cd build/Surelog
git checkout $(python3 ${src_path}/_tools.py --tool surelog --field git-commit)
git submodule update --init --recursive

cmake --version # must be >=3.20

# Point to Python, build universal binary (supporting Intel and Apple Silicon-based Macs)
export ADDITIONAL_CMAKE_OPTIONS="-DPython3_ROOT_DIR=${pythonLocation} -DCMAKE_OSX_ARCHITECTURES='x86_64;arm64'"
make -j$(sysctl -n hw.physicalcpu)
make install PREFIX=$GITHUB_WORKSPACE/surelog
