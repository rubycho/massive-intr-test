# python 3.6
'''
    THE TARGET PROGRAM's last nproc lines should be:
    pid \t cnt
    ...

    COMMAND SAMPLES:
        [1] ./samples/massive_intr {} {}
        [2] sudo ./samples/massive_intr_1 {} {}
'''
import signal
import subprocess
import matplotlib.pyplot as plt

nproc = input("Process #: ")
runtime = input("Run Time(s): ")

print()
print("massive_intr is running with {}procs for {}sec."
    .format(nproc, runtime))

# block signal coming from massive_intr
signal.signal(signal.SIGUSR1, signal.SIG_IGN)

procs = []
total_cnt = 0
p = subprocess.run(
        "sudo ./samples/massive_intr_1 {} {}".format(
            nproc, runtime
        ),
        stdout=subprocess.PIPE,
        shell=True,
        check=True
    )

stdout = p.stdout.decode("utf-8")

print()
print("STDOUT: ")
print(stdout)

nproc = int(nproc)
for line in stdout.splitlines()[-1:-(nproc+1):-1]:
    pid, cnt = line.split('\t')
    proc = {
        'pid': int(pid),
        'cnt': int(cnt)
    }
    procs.append(proc)
    total_cnt += int(cnt)

sorted_procs = sorted(procs, key=lambda o: o['cnt'], reverse=True)
plt.bar(
    [o['pid'] for o in sorted_procs],
    [o['cnt'] for o in sorted_procs],
)
plt.axhline(total_cnt/nproc)
plt.show()
