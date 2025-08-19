make clean
rm -f *.info
rm -f *.bc
ZERO_SPEC_MODE=DETECT ZERO_BENEFIT_THRESHOLD=10 make 
/usr/bin/time -v numactl -C 0-3 ./backprop 1000000 > logs/backprop.detect.0.out.log 2> logs/backprop.detect.0.err.log
sparse_report.py
