# python 3.6
'''
    THE TARGET PROGRAM's last nproc lines should be:
    pid \t cnt
    ...
'''
import os
import signal
import subprocess
import matplotlib.pyplot as plt

# block signal coming from massive_intr
signal.signal(signal.SIGUSR1, signal.SIG_IGN)

procs = []
total_cnt = 0

os.chdir("./application")
p = subprocess.run(
        "sudo ./massive_intr",
        stdout=subprocess.PIPE,
        shell=True,
        check=True
    )
os.chdir("..")

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
plt.ylabel('cnt')
plt.xlabel('task #')
plt.show()
