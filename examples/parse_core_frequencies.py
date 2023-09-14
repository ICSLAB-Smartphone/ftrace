import sys
import argparse
sys.path.append("../")
import ftrace.ftrace
from ftrace.ftrace import FtraceParser
from ftrace.components import *
from ftrace.interval import Interval
from ftrace.task import Task, TaskState
from pandas import DataFrame

LITTLE_CLUSTER_MASK = 0x0F
BIG_CLUSTER_MASK = 0xF0

LITTLE_CPUS = ftrace.common.unpack_bitmap(LITTLE_CLUSTER_MASK)
BIG_CPUS = ftrace.common.unpack_bitmap(BIG_CLUSTER_MASK)
ALL_CPUS = LITTLE_CPUS.union(BIG_CPUS)

'''
parser = argparse.ArgumentParser(description='Per-core frequencies')
parser.add_argument('-f', '--file', dest='file',
                    help='File to parse')
args = parser.parse_args()
'''


#trace = FtraceParser(args.file)
trace = FtraceParser("./trace.txt")
print(trace.interval)
print(trace.cpu.task_intervals(task=7785, interval=Interval(0.016, 0.020215)))
running_time = 0
runnable_time = 0
usleep_time = 0
for task_interval in trace.cpu.task_intervals(task=7785, interval=Interval(0.016, 0.020215)):
    if task_interval.state == TaskState.RUNNING:
        running_time = running_time + task_interval.interval.duration
    elif task_interval.state == TaskState.RUNNABLE or task_interval.state == TaskState.TASK_WAKING:
        runnable_time = runnable_time + task_interval.interval.duration
    elif task_interval.state == TaskState.UNINTERRUPTIBLE:
        usleep_time = usleep_time + task_interval.interval.duration
print("total running time : {}".format(running_time))    #0.840
print("total runnable time : {}".format(runnable_time)) #0.541
print("total usleep time : {}".format(usleep_time))       #0
print("-----------------------------")
print(trace.cpu.task_intervals(task=7785, interval=Interval(0.049, 0.051)))
running_time = 0
runnable_time = 0
usleep_time = 0
for task_interval in trace.cpu.task_intervals(task=7785, interval=Interval(0.049, 0.051)):
    if task_interval.state == TaskState.RUNNING:
        running_time = running_time + task_interval.interval.duration
    elif task_interval.state == TaskState.RUNNABLE or task_interval.state == TaskState.TASK_WAKING:
        runnable_time = runnable_time + task_interval.interval.duration
    elif task_interval.state == TaskState.UNINTERRUPTIBLE:
        usleep_time = usleep_time + task_interval.interval.duration
print("total running time : {}".format(running_time))    #0.654
print("total runnable time : {}".format(runnable_time)) #0.041
print("total usleep time : {}".format(usleep_time))       #0.527

print("-----------------------------")
print(trace.cpu.busy_intervals(cpu=None, interval=Interval(0.016, 0.016)))
print("-----------------------------")
print(trace.cpu.frequency_intervals(cpu=4, interval=Interval(0.016, 0.020215)))
print("-----------------------------")
print(trace.cpu.frequency_intervals(cpu=4, interval=Interval(0.016, 0.016)))

print("************************")
print(trace.android.event_intervals(name="waiting for GPU completion",
                                    task=17218,
                                    #use data.pid instead of task.pid
                                    #task=6980,
                                    interval = Interval(0.016, 0.028),
                                    match_exact=False))
print("**************************")

'''
df_freq = DataFrame(index=ALL_CPUS, columns=FREQ_ALL_CORES)w
df_freq.fillna(0, inplace=True)
'''
for cpu in ALL_CPUS:
    for busy_interval in trace.cpu.busy_intervals(cpu=cpu):
        for freq in trace.cpu.frequency_intervals(cpu=cpu, interval=busy_interval.interval):
            #df_freq.loc[cpu, freq.frequency] += freq.interval.duration
#            print(freq.interval.duration)
            pass

#print(df_freq)