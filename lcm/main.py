from pprint import pprint as pp
from pprint import pformat as pf

import timeout_decorator

# mine
from .structure import Itemset, ItemsetPattern
from .adapter import prepare_input, lcm, arrange_output

"""
data: [Itemset, ... ]
return: [ItemsetPattern, ... ]
"""
def run(data, minsup):
    prepare_input(data)
    flg_successed, msg = lcm(minsup)
    if not flg_successed:
        raise RuntimeError(msg)
    return arrange_output()

"""
seek suit minsup by binary search.
max waiting time is `timeout * try_count`.

timeout: seconds
try_count: depth of binary search. minsup is seeked in units of 6.25% when try_count is 4.
"""
def run_auto(data, timeout=20, try_count=4, flg_report=False):

    @timeout_decorator.timeout(timeout)
    def timeout_lcm(minsup):
        lcm(minsup)

    prepare_input(data)
    d = 2
    minsup = len(data) // d
    saved = None
    for i in range(try_count):
        d *= 2
        unit = len(data) // d
        if flg_report: print(f"{i}-th time try. minsup:{minsup}")
        try:
            timeout_lcm(minsup)
        except timeout_decorator.TimeoutError:
            if flg_report: print("  timeout")
            minsup += unit
        else:
            if flg_report: print("  ended")
            saved = arrange_output()
            minsup -= unit
            if minsup <= 0:
                minsup = 1
    return minsup, saved




