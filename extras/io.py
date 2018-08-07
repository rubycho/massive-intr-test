# python 3.6
'''
    Plot graph
'''
import os
import subprocess
import matplotlib.pyplot as plt

target = "bw="
delimiter = ","
unit = "KB/s"

cmd = input("FIO COMMAND: ")
p = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        shell=True,
        check=True
    )

stdout = p.stdout.decode("utf-8")
content = stdout.splitlines()

speeds = []
total = 0
for line in content:
    if target in line:
        speed = int(
                    line.split(target)[1] \
                    .split(delimiter)[0] \
                    .replace(unit, "")
                )
        total += speed
        speeds.append(speed)

plt.bar(
    [o for o in range(1, len(speeds)+1)],
    [o for o in speeds]
)
plt.axhline(total / len(speeds))
plt.ylabel('{} (unit: {})'.format(
    target.replace("=", ""),
    unit
))
plt.xlabel('job index')
plt.show()
