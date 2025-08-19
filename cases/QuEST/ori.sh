mkdir -p build/logs
cd build
make clean
cmake .. -DCMAKE_C_COMPILER=clang_wrapper.py -DCMAKE_CXX_COMPILER=clang_wrapper.py -DCMAKE_C_FLAGS="--use-clang -O3 -ffinite-math-only -fno-signed-zeros -fno-math-errno -fno-trapping-math"  -DCMAKE_CXX_FLAGS="-O3 -ffinite-math-only -fno-signed-zeros -fno-math-errno -fno-trapping-math" .. 
make -j
/usr/bin/time -v mpirun  --oversubscribe --allow-run-as-root -np 4 ./demo 2> logs/quest.ori.0.err.log > logs/quest.ori.0.out.log
