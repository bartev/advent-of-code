"""Matplotlib example with imaginary numbers

https://aoc.just2good.co.uk/python/complex
"""

import matplotlib.pyplot as plt


def cw_rotate(z: complex, degrees: float) -> complex:
    return z * 1j ** ((360 - degrees / 90))


points: list[complex] = []
POINT = 3 + 2j
print(POINT)

points.append(POINT)

for cw_angle in (90, 180, 270):
    rotated_point = cw_rotate(POINT, cw_angle)
    points.append(rotated_point)

fig, axes = plt.subplots()
axes.set_aspect("equal")
axes.grid(True)

plt.axhline(0, color="black")
plt.axvline(0, color="black")

all_x = [num.real for num in points]
all_y = [num.imag for num in points]

axes.set_xlim(min(all_x), max(all_x))
axes.set_ylim(min(all_y), max(all_y))
axes.set_xlabel("real")
axes.set_ylabel("imag")

colours = ["blue", "orange", "green", "red"]

for i, point in enumerate(points):
    plt.plot([0, point.real], [0, point.imag], "-", marker="o", color=colours[i])
    plt.annotate(str(point), (point.real, point.imag), color=colours[i])

plt.show()
