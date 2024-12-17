import heapq
from collections import deque
from heapq import heappop, heappush

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
start = (0, 0)
end = (5, 5)
queue = deque([(start, [start])])


def heapsort(iterable):
    h = []
    for value in iterable:
        heapq.heappushpop(h, value)
    return [heapq.heappop(h) for i in range(len(h))]


heapsort([1, 3, 5, 7, 9, 2, 4, 6, 8, 0])

h = []
xs = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
heapq.heappush(h, 1)
heapq.heappush(h, 3)

h = []
heappush(h, (5, "write code"))
heappush(h, (7, "release product"))
heappush(h, (1, "write spec"))
heappush(h, (3, "create tests"))
heappop(h)

h
