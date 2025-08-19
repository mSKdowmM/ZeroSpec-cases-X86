import os
import subprocess
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import sys
is_show = len(sys.argv) == 2
def get_time(time):
    time = time.split(' ')[-1]
    # change time from xx:xx:xx.xx or xx:xx.xx to float
    time = time.split(':')
    if len(time) == 3:
        time = float(time[0]) * 3600 + float(time[1]) * 60 + float(time[2])
    elif len(time) == 2:
        time = float(time[0]) * 60 + float(time[1])
    else:
        print("Error: time format is not correct")
        exit(1)
    return time 
# cases = ['bt', 'cg', 'ep', 'ft', 'is', 'lu', 'mg', 'sp', 'ua']
data = {}
data_dict = {}
# cases = ['ua', 'is']
def load(cases, path):
    for case in cases:
        try:
        # if True:
            targets_file = subprocess.check_output(f'ls logs_threshold0/{case}.* -t | grep targets | head -n 1', shell=True, cwd=path).decode().strip()
            # time_file = subprocess.check_output(f'ls -t logs | grep -P "{case}\.ori\.(\d+)\.err.log" | head -n 1', shell=True, cwd=path).decode().strip()
            build_file = subprocess.check_output(f'ls logs_threshold0/{case}.* -t | grep opt |grep build | grep err | head -n 1', shell=True, cwd=path).decode().strip()
            # time_file = os.path.join('logs',time_file)
            if targets_file == '':
                dynamic = []
                static = []
            else:
                info = subprocess.check_output(f'cat {targets_file} | grep -v "\["', shell=True, cwd=path).decode().strip()
                # time_info = subprocess.check_output(f'cat {time_file} | grep "wall "', shell=True, cwd=path).decode().strip()
                # time_wall = get_time(time_info)
                # time_info = subprocess.check_output(f'cat {time_file} | grep "User time"', shell=True, cwd=path).decode().strip()
                # time_cpu = time_info.split(' ')[-1]
                static = [float(x.split(' ')[-3]) for x in info.split('\n')]
                def get_dynamic(x):
                    xs = x.split(' ')
                    weighted_benefit = float(xs[-2])
                    zero_count = float(xs[-6])
                    static_benefit = float(xs[-3])
                    zero_ratio = float(xs[-4])
                    # alpha = 1 if weighted_benefit >= static_benefit * zero_ratio else 0.3
                    alpha = 1
                    return weighted_benefit * alpha * zero_count
                # dynamic = [get_dynamic(x)/ float(time_cpu)/1e9 for x in info.split('\n')]
                if is_show:
                    dynamic = [(float(x.split(' ')[-2])   ) for x in info.split('\n')]
                else:
                    cost_info = subprocess.check_output(f'cat {build_file} | grep "TOTAL COST"', shell=True, cwd=path).decode().strip()
                    cost = sum([float(x.split(' ')[-1]) for x in cost_info.split('\n')])
                    dynamic = [(float(x.split(' ')[-2]) * float(x.split(' ')[-6])  )/ cost for x in info.split('\n')]

                # dynamic = [float(x.split(' ')[-1])/float(time_cpu)/1e9 if '.omp' in x else float(x.split(' ')[-1])/float(time_wall)/1e9 for x in info.split('\n')]
                # dynamic = [float(x.split(' ')[-1])/float(time_cpu)/1e9 for x in info.split('\n')]
        except Exception as e:
            #print(e)
            static = []
            dynamic = []
        data[case] = {
            'dynamic': dynamic,
            'static': static
        }
        if len(dynamic) != 0:
            print(f"{case}, {sum(dynamic)}")
        else:
            print(f"{case}, 0")
        #print('\t',targets_file)
load(['bt', 'cg', 'ep', 'ft', 'is', 'lu', 'mg', 'sp', 'ua'], '/root/ZeroSpec/cases/NPB3.4.3/NPB3.4-OMP')
load(['quest'], '/root/ZeroSpec/cases/QuEST/build')
load(['backprop'], '/root/ZeroSpec/cases/backprop/')

data_dict['X86'] = data
# print(data)
name_map = {
    'bt': "BT",
    "cg": "CG",
    "ep": "EP",
    "ft": "FT",
    "is": "IS",
    "lu": "LU",
    "mg": "MG",
    "sp": "SP",
    "ua": "UA",
    "quest": "QuEST",
    "backprop": "backprop"
}
new_data_dict = {}
for platform in data_dict.keys():
    new_data_dict[platform] = {}
    for case in data_dict[platform]:
        new_data_dict[platform][name_map[case]] = data_dict[platform][case]
data_dict = new_data_dict


# records = []
# for app, values in data.items():
#     statics = values['static']
#     dynamics = values['dynamic']
#     for s, d in zip(statics, dynamics):
#         records.append({'Application': app, 'Static Gain': s, 'Dynamic Gain': d})


# df = pd.DataFrame(records)
# # df["Static Gain"] = np.log1p(df["Static Gain"])


# # 画图风格
# sns.set(style="whitegrid", font_scale=1.2)

# # 📦 静态收益箱线图 + 散点
# plt.figure(figsize=(12, 6))
# # plt.yscale('log')
# sns.boxplot(x="Application", y="Static Gain", data=df, whis=1.5, width=0.6, fliersize=0)
# sns.stripplot(x="Application", y="Static Gain", data=df, jitter=True, color='black', alpha=0.6, size=4)
# plt.title("Static Optimization Gain per Instruction")
# plt.tight_layout()
# plt.savefig('static7.pdf')

# # 📦 动态收益箱线图 + 散点
# plt.figure(figsize=(12, 6))
# plt.yscale('log')
# sns.boxplot(x="Application", y="Dynamic Gain", data=df, whis=1.5, width=0.6, fliersize=0)
# sns.stripplot(x="Application", y="Dynamic Gain", data=df, jitter=True, color='black', alpha=0.6, size=4)
# plt.title("Dynamic Optimization Gain per Instruction")
# plt.tight_layout()
# plt.savefig('dynamic7.pdf')
records = []
for platform, apps in data_dict.items():
    for app, values in apps.items():
        for s, d in zip(values['static'], values['dynamic']):
            records.append({
                'Platform': platform,
                'Application': app,
                'Static Benefit': s,
                'Dynamic Benefit': d
            })

df = pd.DataFrame(records)
box_width = 0.4
dodge = box_width 
# ✅ 开始画图（静态收益）
sns.set(style="whitegrid", font_scale=1.5)
fig = plt.figure(figsize=(11, 4))
plt.xticks(rotation=30)
plt.yscale('log')
ax = sns.boxplot(x="Application", y="Static Benefit", hue="Platform", data=df,
            whis=1.5, width=box_width, dodge=True, legend=True)
# sns.stripplot(x="Application", y="Static Gain", hue="Platform", data=df,
            #   jitter=True, dodge=True, marker='o', alpha=0.6, size=4, palette="dark")

ax.set(xlabel=None)


title = "(a) Static Optimization Benefit Distribution"
# plt.title()
# plt.annotate(text=title, xy=(0.5, 0.03), color='black', ha='center', va='center', clip_on=False, xycoords='figure fraction')
plt.legend(bbox_to_anchor=(0.0, 1.05), loc='upper left')
plt.tight_layout()
plt.savefig('static.pdf')

# ✅ 动态收益
plt.figure(figsize=(11, 4))
plt.xticks(rotation=30)

plt.yscale('log')
# plt.ylim(0,0.2)
ax = sns.boxplot(x="Application", y="Dynamic Benefit", hue="Platform", data=df,
            whis=1.5, width=box_width,  dodge=True, legend=True)
# sns.stripplot(x="Application", y="Dynamic Gain", hue="Platform", data=df,
            #   jitter=True, dodge=True, marker='o', alpha=0.6, size=4, palette="dark")
ax.set(xlabel=None)
# plt.title("(b) Dynamic Optimization Benefit Distribution", y=-0.1)
title = ("(b) Dynamic Optimization Benefit Distribution")
# plt.annotate(text=title, xy=(0.5, 0.03), color='black', ha='center', va='center', clip_on=False, xycoords='figure fraction')
plt.legend( bbox_to_anchor=(0.0, 1.05), loc='upper left')
plt.tight_layout()
plt.savefig('dynamic.pdf')
