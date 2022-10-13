from pprint import pprint as pp
from pprint import pformat as pf

import lcm

def get_data():
    data = [
            lcm.Itemset((0, 1)),
            lcm.Itemset((2, 3)),
            lcm.Itemset((4, 5)),
            lcm.Itemset((6, 7)),
            lcm.Itemset((8, 9)),
            ]
    print('data') # debug
    pp(data) # debug
    return data

def test_error_no_freq():
    data = get_data()
    try:
        result = lcm.run(data, 2)
        assert False
    except lcm.NoFrequentItemError as e:
        assert str(e) == "there is no frequent item"

def test_failed_error():
    data = get_data()
    minsup, result = lcm.run_auto(data)
    try:
        result = lcm.run_auto(data, try_count=1)
        assert False
    except lcm.FailedAutoMinsupError as e:
        assert str(e) == "Failed to find minsup automatically"


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("Test lcm")
    args = parser.parse_args()

    test_error_no_freq()
    test_failed_error()

    print('\33[32m' + 'end' + '\033[0m')

