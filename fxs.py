from __future__ import print_function

import pygion
from pygion import index_launch, task, Region, R, Reduce
import numpy as np

@task(privileges=[Reduce('+')])
def inc(data):
    np.add(data.x, 1, out=data.x)

@task(privileges=[R])
def check_result(data, n_steps, n_tasks):
    x = data.x
    assert np.sum(x) == float(n_steps * n_tasks * x.size)
    print('PASSED')

@task
def main():
    data = Region([10, 10, 10], {'x': pygion.float64})
    pygion.fill(data, 'x', 0)

    n_tasks = 10
    n_steps = 10
    for step in range(n_steps):
        index_launch([n_tasks], inc, data)
    check_result(data, n_steps, n_tasks).get()

if __name__ == '__main__':
    main()
