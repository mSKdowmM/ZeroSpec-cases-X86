cd build
make clean
cmake .. -DCMAKE_C_COMPILER=clang_wrapper.py -DCMAKE_CXX_COMPILER=clang_wrapper.py -DCMAKE_C_FLAGS="--use-clang -O3 -ffinite-math-only -fno-signed-zeros -fno-math-errno -fno-trapping-math"  -DCMAKE_CXX_FLAGS="-O3 -ffinite-math-only -fno-signed-zeros -fno-math-errno -fno-trapping-math" ..
ZERO_SPEC_MODE=DETECT ZERO_BENEFIT_THRESHOLD=10 make -j > logs/quest.detect.0.build.out.log 2> logs/quest.detect.0.build.err.log
rm -rf data-*
/usr/bin/time -v mpirun -np 4 --allow-run-as-root --oversubscribe ./demo 2> logs/quest.detect.0.err.log > logs/quest.detect.0.out.log
ls |  grep data- > datas.txt
sparse_report.py datas.txt
