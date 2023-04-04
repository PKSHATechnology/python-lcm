from pprint import pprint as pp
from pprint import pformat as pf

import logging
logger = logging.getLogger()
#handler = logging.FileHandler(filename="log")
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)8s %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

import random

import lcm

def make_random_data(size=10000):
    data = []
    u = list(range(2000))
    for _ in range(size):
        s = random.randint(500, 600)
        one = random.sample(u, s)
        data.append(set(one))
    return data

def test_run_auto():
    data = make_random_data()
    minsup, result = lcm.run_auto(data, timeout=7, try_count=5)
    print(f'minsup', minsup) # debug
    #print('result[:2]') # debug
    #pp(result[:2]) # debug

def test_run_auto_small():
    data = make_random_data(10)
    minsup, result = lcm.run_auto(data, timeout=7, try_count=5)
    print(f'minsup', minsup) # debug
    assert minsup == 2
    #print('result') # debug
    #pp(result) # debug


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("Test lcm")
    args = parser.parse_args()

    #test_run_auto()
    test_run_auto_small()

    print('\33[32m' + 'end' + '\033[0m')

