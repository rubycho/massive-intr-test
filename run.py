# python 3.6
'''
    THE TARGET PROGRAM's last nproc lines should be:
    pid \t cnt
    ...
'''
import os
import sys
import signal
import subprocess
import matplotlib.pyplot as plt

# block signal coming from massive_intr
signal.signal(signal.SIGUSR1, signal.SIG_IGN)

procs = []
total_cnt = 0

if len(sys.argv) != 2:
    print("{} <configfile>".format(sys.argv[0]))
    print("\t\tconfigfile: path to config file")
    sys.exit(1)

print("Waiting massive_intr to terminate...\n")
p = subprocess.run(
        "sudo ./application/massive_intr {}".format(
            sys.argv[1]
        ),
        stdout=subprocess.PIPE,
        shell=True,
        check=True
    )

stdout = p.stdout.decode("utf-8")
print(stdout)

content = stdout.split("[RESULT]\n")[1].splitlines()
nproc = len(content)
for line in content[-1:-(nproc+1):-1]:
    pid, cnt = line.split('\t')
    proc = {
        'pid': int(pid),
        'cnt': int(cnt)
    }
    procs.append(proc)
    total_cnt += int(cnt)

sorted_procs = sorted(procs, key=lambda o: o['pid'])
plt.bar(
    [o for o in range(0, len(sorted_procs))],
    [o['cnt'] for o in sorted_procs],
)
plt.axhline(total_cnt/nproc)
plt.ylabel('loop count')
plt.xlabel('task index')
plt.show()
