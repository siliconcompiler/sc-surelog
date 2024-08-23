# Get directory of setup scripts
src_path=$(cd -- "$(dirname "$0")/../../../siliconcompiler" >/dev/null 2>&1 ; pwd -P)

yum install -y libuuid-devel java-11-openjdk-devel python3 zlib-static

python3 -m venv .venv
PYTHON_ROOT=$(realpath .venv)
$PYTHON_ROOT/bin/python -m pip install orderedmultidict
export ADDITIONAL_CMAKE_OPTIONS="-DPython3_ROOT_DIR=$PYTHON_ROOT -DPython3_FIND_STRATEGY=LOCATION"

# Build surelog (install prefix defined outside file)
git clone $(python3 ${src_path}/setup/_tools.py --tool surelog --field git-url) Surelog
cd Surelog
git checkout $(python3 ${src_path}/setup/_tools.py --tool surelog --field git-commit)
git submodule update --init --recursive

export LDFLAGS="-lrt"
make -j$(nproc)
make install PREFIX=$GITHUB_WORKSPACE/sc_surelog

cd -
