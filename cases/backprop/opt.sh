make clean
rm $PWD/logs/backprop.opt.0.targets.log
ZERO_SPEC_MODE=OPT ZERO_SPEC_DB=$PWD/zero.report ZERO_SPEC_TARGETS_LOG=$PWD/logs/backprop.opt.0.targets.log make > logs/backprop.opt.0.build.out.log 2> logs/backprop.opt.0.build.err.log
/usr/bin/time -v numactl -C 0-3 ./backprop 1000000 > logs/backprop.opt.0.out.log 2> logs/backprop.opt.0.err.log
