import numpy as np
import itertools
import time

shape = [4 for i in range(19)]

start = time.time()
i = 0
for idx in itertools.product(*[range(s) for s in shape]):
    # i += 1
    # q = idx[2] * idx[7] * idx[3] * idx[13]
    pass

print(i)
a = time.time() - start
print(f"{a} sec, {a / 60} min, {a / 3600} hours")