from pprint import pprint as pp
from pprint import pformat as pf
import logging
logger = logging.getLogger(__name__)

import wrapt_timeout_decorator

# mine
from .structure import Itemset, ItemsetPattern
from .adapter import prepare_input, lcm, arrange_output, NoFrequentItemError

"""
data: [Itemset, ... ]
return: [ItemsetPattern, ... ]
"""
def run(data, minsup):
    prepare_input(data)
    lcm(minsup)
    return arrange_output()

"""
seek suit minsup by binary search.
max waiting time is `timeout * try_count`.

timeout: seconds
try_count: depth of binary search. minsup is seeked in units of 6.25% when try_count is 4, and 1.5625% when try_count is 6.
"""
def run_auto(data, timeout=20, try_count=6):

    @wrapt_timeout_decorator.timeout(timeout)
    def timeout_lcm(minsup):
        lcm(minsup)

    prepare_input(data)
    d = 2
    minsup = len(data) // d
    saved = None
    for i in range(try_count):
        d *= 2
        unit = len(data) // d
        logger.info(f"{i}-th time try. minsup:{minsup}")
        try:
            timeout_lcm(minsup)
        except TimeoutError:
            logger.info("  timeout")
            minsup += unit
        except NoFrequentItemError as err:
            logger.info(str(err))
            minsup -= unit
        else:
            logger.info("  ended")
            saved = arrange_output()
            minsup -= unit
        if minsup <= 0:
            minsup = 1
    if saved is None:
        raise ValueError("Failed to find minsup automatically")
    return minsup, saved




