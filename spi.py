from __future__ import division, print_function

import pygion
from pygion import index_launch, task, ID, Partition, Region, R, Reduce
import numpy as np

@task(privileges=[R, R, R, Reduce('+')])
def update_step(A, B, x_old, x):
    np.add(x.data, np.matmul(np.matmul(A.data, B.data), x_old.data), out=x.data)

@task(privileges=[R])
def check_result(x):
    print(x.data)

@task
def main():
    short_size = 10
    long_size = 1000
    A = Region([short_size, long_size], {'data': pygion.float64})
    B = Region([long_size, short_size], {'data': pygion.float64})
    x = Region([short_size], {'data': pygion.float64})
    x_old = Region([short_size], {'data': pygion.float64})
    pygion.fill(A, 'data', 0)
    pygion.fill(B, 'data', 0)
    pygion.fill(x, 'data', 0)
    pygion.fill(x_old, 'data', 0)

    n_tasks = 10
    n_steps = 10

    A_transform = [[0], [long_size/n_tasks]]
    A_extent = [short_size, long_size//n_tasks]
    A_part = Partition.restrict(A, [n_tasks], A_transform, A_extent)

    B_transform = [[long_size/n_tasks], [0]]
    B_extent = [long_size//n_tasks, short_size]
    B_part = Partition.restrict(B, [n_tasks], B_transform, B_extent)

    for step in range(n_steps):
        x, x_old = x_old, x
        index_launch([n_tasks], update_step, A_part[ID], B_part[ID], x_old, x)
    check_result(x)

if __name__ == '__main__':
    main()
