import numpy as np
import itertools
import time

shape = [3 for i in range(15)]

start = time.time()
i = 0
for idx in itertools.product(*[range(s) for s in shape]):
    # i += 1
    # print(idx)
    # q = idx[2] * idx[7] * idx[3] * idx[13]
    pass

print(i)
a = time.time() - start
print(f"{a} sec, {a / 60} min, {a / 3600} hours")