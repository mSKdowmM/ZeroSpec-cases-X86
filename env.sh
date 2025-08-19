cd /workdir/zerospec
source env.sh
cd $OLDPWD
export PATH=$LLVM_INSTALL_PREFIX/bin:$PATH
export LD_LIBRARY_PATH=$LLVM_INSTALL_PREFIX/lib:$LLVM_INSTALL_PREFIX/lib/x86_64-unknown-linux-gnu/:$LD_LIBRARY_PATH
export THRESHOLD=0
