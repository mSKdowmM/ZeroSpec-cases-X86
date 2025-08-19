make clean
rm -f *.info
rm -f *.bc
mkdir logs_threshold0
export NO_FILTER=1
ZERO_SPEC_MODE=DETECT ZERO_BENEFIT_THRESHOLD=0 make 
/usr/bin/time -v numactl -C 0-3 ./backprop 1000000 > logs_threshold0/backprop.detect.0.out.log 2> logs_threshold0/backprop.detect.0.err.log
sparse_report.py
