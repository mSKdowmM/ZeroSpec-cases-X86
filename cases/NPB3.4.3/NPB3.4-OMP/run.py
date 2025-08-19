import subprocess
import os
import argparse
from timeit import default_timer as timer
cases = ['bt', 'cg', 'ep', 'ft', 'is', 'lu', 'mg', 'sp', 'ua']

run_prefix = 'numactl -C 0-15'
def check_in_array(value, allowed_values):
    try:
        if value not in allowed_values:
            raise ValueError
        return value
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid value '{value}'. Must be one of {allowed_values}.")
parser = argparse.ArgumentParser(description="Run SPEC CPU benchmarks")
# parser.add_argument('-c', '--case', type=int, choices=case_name.keys(), help='Case number to run')
parser.add_argument('-m', '--mode', type=str, choices=['ori', 'detect', 'opt'], help='Mode to run')
parser.add_argument('-b', '--build', action='store_true', default=False, help='Build the benchmark before running')
parser.add_argument('--clean', action='store_true', default=False, help='Clean the benchmark before running')
parser.add_argument('-c', '--cases', type=lambda x: check_in_array(x, cases + ['suite']), nargs='+', help='Case numbers to run')
parser.add_argument('--threshold', type=int, help='Benefit threshold for instrumentation')
parser.add_argument('--delta', type=int, help='Delta threshold for optimization', default=0)
parser.add_argument('--cost', type=int, help='Branch miss cost', default=0)
parser.add_argument('--size', type=str, choices=['A', 'B', 'C'], default='C')
parser.add_argument('--fake', action='store_true', default=False, help=' Not run the benchmark after building')
parser.add_argument('--logdir', type=str, default="logs")



def build_path(case_id):
    return os.path.curdir
def run_path(case_id):
    return os.path.join(os.path.curdir, case_id)


args = parser.parse_args()
def run_case(case_id):

    log_count = 0
    #while os.path.exists(f"{args.logdir}/{case_id}.{args.mode}.{log_count}.out.log"):
    #    log_count += 1

    if not os.path.exists(run_path(case_id)):
        os.makedirs(run_path(case_id))

    if args.clean:
        # remove the build path
        os.system(f"make clean")


    exe_path = (f"{os.getcwd()}/bin/{case_id}.{args.size}.x")
    if not os.path.exists(f'{args.logdir}'):
        os.makedirs(f'{args.logdir}')
    if not os.path.exists('zero_info'):
        os.makedirs('zero_info')
    build_time = -1
    if args.build:
        code = subprocess.call("find . -name '*.o' | xargs rm -f", shell=True, cwd=build_path(case_id))
        if args.mode == 'detect':
            code = subprocess.call("find . -name '*.info' | xargs rm -f", shell=True, cwd=build_path(case_id))
        if code != 0:
            print("Error removing .o files")
            exit(1)
        build_env = os.environ.copy()
        if args.mode == 'detect':
            if args.threshold is not None:
                build_env['ZERO_BENEFIT_THRESHOLD'] = str(args.threshold)
            build_env['ZERO_SPEC_MODE'] = 'DETECT'
        elif args.mode == 'opt':
            build_env['ZERO_SPEC_MODE'] = 'OPT'
            if args.delta is not None:
                build_env['ZERO_SPEC_OPT_DELTA'] = str(args.delta)
            if args.cost is not None:
                build_env['ZERO_SPEC_BRANCH_MISS_COST'] = str(args.cost)
            if args.threshold is not None:
                build_env['ZERO_BENEFIT_THRESHOLD'] = str(args.threshold)
            with open(os.path.abspath(f"{args.logdir}/{case_id}.{args.mode}.{log_count}.targets.log"), 'a') as f:
                pass
            build_env['ZERO_SPEC_TARGETS_LOG'] = os.path.abspath(f"{args.logdir}/{case_id}.{args.mode}.{log_count}.targets.log")
            # find newest zero_info/{case_id}.xxx/zero.report
            zero_report = subprocess.run(f"ls -t zero_info/ | grep '{case_id}\.' | head -n 1", shell=True, capture_output=True)
            zero_report_path = f'zero_info/{zero_report.stdout.decode().strip()}/zero.report'
            if not os.path.exists(zero_report_path):
                print(f"Zero report {zero_report_path} does not exist.")
                exit(1)
            build_env['ZERO_SPEC_DB'] = os.path.abspath(zero_report_path)
        if case_id == 'suite':
            build_target = ' '.join(cases)
        else:
            build_target = case_id
        st = timer()
        build_res = subprocess.run(f"numactl -C 0-15 make  {build_target} CLASS={args.size}", shell=True, cwd=build_path(case_id), env=build_env, capture_output=True)
        ed = timer()
        if build_res.returncode != 0:
            print("Error building benchmark")
            print(build_res.stderr.decode())
            exit(1)
        build_time = ed - st

        for case in cases:
            if os.path.exists(f"bin/{case}.{args.size}.x"):
                os.system(f"mv bin/{case}.{args.size}.x bin/{case}.{args.size}.x.{args.mode}")

    if not args.fake:
        if args.mode == 'detect':
            subprocess.run('rm -f data-*', cwd=run_path(case_id), shell=True)
        res = subprocess.run(f"{run_prefix} /usr/bin/time -v {exe_path}.{args.mode} ", shell=True, cwd=run_path(case_id), env=os.environ, capture_output=True)
    else:
        res = None




    with open(f"{args.logdir}/{case_id}.{args.mode}.{log_count}.out.log", "w") as f:
        if res is not None:
            f.write(res.stdout.decode())
    with open(f"{args.logdir}/{case_id}.{args.mode}.{log_count}.err.log", "w") as f:
        if res is not None:
            f.write(res.stderr.decode())
            if res.returncode != 0:
                f.write(f"Error code: {res.returncode}\n")
    if args.build:
        with open(f"{args.logdir}/{case_id}.{args.mode}.{log_count}.build.out.log", "w") as f:
            f.write(build_res.stdout.decode())
            f.write(f"Build time: {build_time} seconds\n")
        with open(f"{args.logdir}/{case_id}.{args.mode}.{log_count}.build.err.log", "w") as f:
            f.write(build_res.stderr.decode())
    with open(f"{args.logdir}/{case_id}.{args.mode}.{log_count}.env.log", "w") as f:
        f.write("Environment variables:\n")
        for key, value in os.environ.items():
            f.write(f"{key}={value}\n")

    if args.mode == 'detect' and res is not None and res.returncode == 0:
        subprocess.run('ls | grep data- > reports.txt', cwd=run_path(case_id), shell=True)
        subprocess.run('sparse_report.py reports.txt', cwd=run_path(case_id), shell=True)
        os.system(f"mkdir -p zero_info/{case_id}.{log_count}")
        os.system(f'mv {run_path(case_id)}/data-* zero_info/{case_id}.{log_count}/')
        os.system(f'mv {run_path(case_id)}/zero.report zero_info/{case_id}.{log_count}/')

if ('suite' in args.cases or len(args.cases) > 1) and not args.fake and args.build and args.mode == 'detect':
    print("Error: --fake is necessary when building multiple targets.")
    exit(-1)


if 'suite' in args.cases:
    if args.fake and args.build and args.mode == 'detect':
        run_case('suite')
        exit(0)
    else:
        for case in cases:
            run_case(case)
    exit(0)

for case_id in args.cases:
    if case_id not in cases:
        print(f"Case {case_id} not found.")
        exit(1)
    run_case(case_id)

