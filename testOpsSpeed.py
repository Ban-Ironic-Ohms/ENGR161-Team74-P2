import numpy as np
import itertools
import time

shape = [4 for i in range(15)]

start = time.time()

for idx in itertools.product(*[range(s) for s in shape]):
    # print(idx)
    pass

print(time.time() - start)