make clean
make
mkdir logs
/usr/bin/time -v numactl -C 0-3 ./backprop 1000000 > logs/backprop.ori.0.out.log 2> logs/backprop.ori.0.err.log
