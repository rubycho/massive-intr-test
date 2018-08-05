# python 3.6
'''
    Plot graph
'''
import os
import matplotlib.pyplot as plt

target = "bw="
delimiter = ","
unit = "KB/s"

filename = input("file path: ")
with open(filename) as f:
    content = f.readlines()

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
plt.xlabel('job #')
plt.show()
