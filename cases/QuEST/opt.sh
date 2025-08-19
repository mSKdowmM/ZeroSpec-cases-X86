cd build
make clean
cmake .. -DCMAKE_C_COMPILER=clang_wrapper.py -DCMAKE_CXX_COMPILER=clang_wrapper.py -DCMAKE_C_FLAGS="--use-clang -O3 -ffinite-math-only -fno-signed-zeros -fno-math-errno -fno-trapping-math"  -DCMAKE_CXX_FLAGS="-O3 -ffinite-math-only -fno-signed-zeros -fno-math-errno -fno-trapping-math" ..
rm -f $PWD/logs/quest.opt.0.targets.log
ZERO_SPEC_MODE=OPT ZERO_SPEC_DB=$PWD/zero.report ZERO_SPEC_TARGETS_LOG=$PWD/logs/quest.opt.0.targets.log make -j > logs/quest.opt.0.build.out.log 2> logs/quest.opt.0.build.err.log
/usr/bin/time -v mpirun -np 4 --oversubscribe --allow-run-as-root  ./demo > logs/quest.opt.0.out.log 2> logs/quest.opt.0.err.log
