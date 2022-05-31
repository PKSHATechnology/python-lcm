#!/bin/sh
SCRIPT_DIR=$(dirname $0)
cd $SCRIPT_DIR

WORKING_DIR="tmp_install_lcm"
INSTALL_PATH="$PYENV_ROOT/shims"

mkdir "$WORKING_DIR"
cd tmp_install_lcm
curl -O http://research.nii.ac.jp/~uno/code/lcm53.zip
unzip lcm53.zip
make
cp -b --suffix=_$(date +%Y%m%d).bk lcm "$INSTALL_PATH"
cd ..
rm -fr "$WORKING_DIR"
