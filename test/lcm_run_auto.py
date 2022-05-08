from pprint import pprint as pp
from pprint import pformat as pf

import random

import lcm

def make_random_data():
    data = []
    size = 10000
    u = list(range(2000))
    for _ in range(size):
        s = random.randint(500, 600)
        one = random.sample(u, s)
        data.append(set(one))
    return data


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("Test lcm")
    args = parser.parse_args()

    data = make_random_data()
    minsup, result = lcm.run_auto(data, timeout=1, flg_report=True)
    print(f'minsup', minsup) # debug
    print('result[:2]') # debug
    pp(result[:2]) # debug

    print('\33[32m' + 'end' + '\033[0m')

