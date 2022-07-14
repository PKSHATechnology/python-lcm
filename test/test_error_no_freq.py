from pprint import pprint as pp
from pprint import pformat as pf

import lcm

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser("Test lcm")
    args = parser.parse_args()

    data = [
            lcm.Itemset((0, 1)),
            lcm.Itemset((2, 3)),
            lcm.Itemset((4, 5)),
            lcm.Itemset((6, 7)),
            lcm.Itemset((8, 9)),
            ]
    print('data') # debug
    pp(data) # debug
    try:
        result = lcm.run(data, 2)
    except ValueError as e:
        assert str(e) == "there is no frequent item"

    print('\33[32m' + 'end' + '\033[0m')

