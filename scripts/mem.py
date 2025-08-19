import matplotlib.pyplot as plt
import numpy as np

# 原始数据
apps = ["IS", "UA", "BT", "CG", "EP", "FT", "LU", "MG", "SP", "QuEST", "backprop"]

import subprocess

def load(cases, path, t7, t0):
    for case in cases:
        print(case)
        ori_mem = subprocess.check_output(f"cat {path}/logs/{case}.ori.0.err.log  | grep Maximum | awk '{{print $NF}}'", shell=True)
        print(ori_mem)
        detect_mem = subprocess.check_output(f"cat {path}/logs/{case}.detect.0.err.log  | grep Maximum | awk '{{print $NF}}'", shell=True)
        print(detect_mem)
        threshold0_mem = subprocess.check_output(f"cat {path}/logs_threshold0/{case}.detect.0.err.log  | grep Maximum | awk '{{print $NF}}'", shell=True)
        print(threshold0_mem)

        t7.append(int(detect_mem) / int(ori_mem))
        t0.append(int(threshold0_mem) / int(ori_mem))

mem_t = []
mem_t0 = []
load(['is', 'ua', 'bt', 'cg', 'ep', 'ft', 'lu', 'mg', 'sp'], '/root/ZeroSpec/cases/NPB3.4.3/NPB3.4-OMP', mem_t, mem_t0)
load(['quest'], '/root/ZeroSpec/cases/QuEST/build', mem_t, mem_t0)
load(['backprop'], '/root/ZeroSpec/cases/backprop', mem_t, mem_t0)
    



# 添加平均值
def mean(lst): return sum(lst) / len(lst)
mem_t0.append(mean(mem_t0))
mem_t.append(mean(mem_t))
apps.append("Average")
print(mem_t0[-1])
print(mem_t[-1])

x = np.arange(len(apps))
width = 0.2
y_limit = 60

fontsize=16
fig, ax = plt.subplots(figsize=(12, 4))

# 柱状图绘制
bars3 = ax.bar(x - 0.5*width, mem_t0, width, label="X86 Threshold=0", color="#ff7f0e")
bars4 = ax.bar(x + 0.5*width, mem_t, width, label="X86 Threshold=10", color="#ffbb78")

# 样式设置
ax.set_ylim(0.95, 1.75)
ax.set_ylabel("Memory Overhead", fontsize=fontsize)
ax.set_xticks(x)
ax.set_xticklabels(apps, rotation=45, ha="right", fontsize=fontsize)
ax.tick_params(axis='y', labelsize=fontsize)
ax.legend(fontsize=fontsize-2, loc='upper left')

# title = "(b) Memory Overhead"
# plt.annotate(text=title, xy=(0.5, 0.03), color='black', ha='center', va='center', clip_on=False, xycoords='figure fraction',fontsize=14)

# 标注被 clamp 的柱子
def annotate_clipped_bars(bars, limit=60):
    for bar in bars:
        height = bar.get_height()
        if height > limit:
            ax.text(bar.get_x() + bar.get_width()/2, limit + 1.5,
                    f'{height:.1f}', ha='center', va='bottom',
                    fontsize=fontsize, fontweight='bold', color='darkred')

annotate_clipped_bars(bars3)
annotate_clipped_bars(bars4)

plt.tight_layout()
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.savefig('memory.pdf')
