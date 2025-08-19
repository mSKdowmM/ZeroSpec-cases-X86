make clean
rm $PWD/logs_threshold0/backprop.opt.0.targets.log
ZERO_SPEC_MODE=OPT ZERO_SPEC_DB=$PWD/zero.report ZERO_SPEC_TARGETS_LOG=$PWD/logs_threshold0/backprop.opt.0.targets.log make > logs_threshold0/backprop.opt.0.build.out.log 2> logs_threshold0/backprop.opt.0.build.err.log
/usr/bin/time -v numactl -C 0-3 ./backprop 1000000 > logs_threshold0/backprop.opt.0.out.log 2> logs_threshold0/backprop.opt.0.err.log
