import subprocess
import sys
import os

case = sys.argv[1]
print_mode = sys.argv[2]
workpath = sys.argv[3]
cases = [ 'is', 'ua']

def get_time(case, mode):
    file = subprocess.check_output(f'ls -t logs | grep -P "{case}\.{mode}\.(\d+)\.err.log" | head -n 1', shell=True, cwd=workpath).decode('utf-8').strip()
    path = os.path.join('logs', file)
    time_line = subprocess.check_output(f'cat {path} | grep "wall clock" | tail -n 1', shell=True, cwd=workpath).decode('utf-8').strip()
    # print(time_line)
    # print(path)
    time = time_line.split(' ')[-1]
    # change time from xx:xx:xx.xx or xx:xx.xx to float
    time = time.split(':')
    if len(time) == 3:
        time = float(time[0]) * 3600 + float(time[1]) * 60 + float(time[2])
    elif len(time) == 2:
        time = float(time[0]) * 60 + float(time[1])
    else:
        print(f"Error: time format is not correct for {case}.{mode}")
        exit(1)
    return time 

import sys
def work(*args):
    return get_time(*args)
def main(case, print_mode):
    ori = work(case, 'ori')
    detect = work(case, 'detect')
    opt = work(case, 'opt')
    # print(ori, opt)
    if print_mode == 'speedup':
        print(f"{case}, {ori/opt}")
    elif print_mode == 'overhead':
        print(f"{case}, {detect/ori}")

if case == 'suite':
    for case in cases:
        main(case, print_mode)
else:
    main(case, print_mode)
