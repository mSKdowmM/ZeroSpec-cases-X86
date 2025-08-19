import matplotlib.pyplot as plt
import numpy as np
import subprocess
import os

# 原始数据
apps = ["IS", "UA", "BT", "CG", "EP", "FT", "LU", "MG", "SP", "QuEST", "backprop"]

slowdown_t0 = []
slowdown_t = []
def line2time(line):
    time = line.split(' ')[-1]
    # change time from xx:xx:xx.xx or xx:xx.xx to float
    time = time.split(':')
    if len(time) == 3:
        time = float(time[0]) * 3600 + float(time[1]) * 60 + float(time[2])
    elif len(time) == 2:
        time = float(time[0]) * 60 + float(time[1])
    else:
        print(f"Error: time format is not correct")
        exit(1)
    return time 

def load(cases, path, overhead_t, overhead_t0):
    for case in cases:
        ori_line = subprocess.check_output(f'cat {path}/logs/{case}.ori.0.err.log | grep "wall clock" | tail -n 1', shell=True).decode('utf-8').strip()
        ori_time = line2time(ori_line)
        t_line = subprocess.check_output(f'cat {path}/logs/{case}.detect.0.err.log | grep "wall clock" | tail -n 1', shell=True).decode('utf-8').strip()
        t_time = line2time(t_line)
        t0_line = subprocess.check_output(f'cat {path}/logs_threshold0/{case}.detect.0.err.log | grep "wall clock" | tail -n 1', shell=True).decode('utf-8').strip()
        t0_time = line2time(t0_line)
        overhead_t.append(t_time / ori_time)
        overhead_t0.append(t0_time / ori_time)

        
        # print(time_line)
        # print(path)

load(['is', 'ua', 'bt', 'cg', 'ep', 'ft', 'lu', 'mg', 'sp'], '/root/ZeroSpec/cases/NPB3.4.3/NPB3.4-OMP', slowdown_t, slowdown_t0)
load(['quest'], '/root/ZeroSpec/cases/QuEST/build', slowdown_t, slowdown_t0)
load(['backprop'], '/root/ZeroSpec/cases/backprop', slowdown_t, slowdown_t0)

# 添加平均值
def mean(lst): return sum(lst) / len(lst)
slowdown_t0.append(mean(slowdown_t0))
slowdown_t.append(mean(slowdown_t))
apps.append("Average")
print(slowdown_t0[-1])
print(slowdown_t[-1])

x = np.arange(len(apps))
width = 0.2
y_limit = 60

fig, ax = plt.subplots(figsize=(12, 4))

# 柱状图绘制
bars3 = ax.bar(x - 0.5*width, slowdown_t0, width, label="X86 Threshold=0", color="#ff9440")
bars4 = ax.bar(x + 0.5*width, slowdown_t, width, label="X86 Threshold=10", color="#ffbb78")

fontsize=16
# 样式设置
ax.set_ylim(0, y_limit)
ax.set_ylabel("Runtime Overhead", fontsize=fontsize)
ax.set_xticks(x)
ax.set_xticklabels(apps, rotation=45, ha="right", fontsize=fontsize)
ax.tick_params(axis='y', labelsize=fontsize)
ax.legend(fontsize=fontsize-2, loc='upper left')

# 标注被 clamp 的柱子
def annotate_clipped_bars(bars, limit=60):
    for bar in bars:
        height = bar.get_height()
        if height > limit-1:
            ax.text(bar.get_x() + bar.get_width()/2, limit + 1.5,
                    f'{height:.0f}', ha='center', va='bottom',
                    fontsize=fontsize, fontweight='bold', color='darkred')

# title = "(a) Runtime Overhead"
# plt.annotate(text=title, xy=(0.5, 0.03), color='black', ha='center', va='center', clip_on=False, xycoords='figure fraction',fontsize=14)

annotate_clipped_bars(bars3)
annotate_clipped_bars(bars4)

plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.savefig('slowdown.pdf')
