from pprint import pprint as pp
from pprint import pformat as pf
import logging
logger = logging.getLogger(__name__)

import wrapt_timeout_decorator

# mine
from .structure import Itemset, ItemsetPattern
from .adapter import prepare_working_dir, delete_working_dir, prepare_input, lcm, arrange_output, NoFrequentItemError

"""
data: [Itemset, ... ]
return: [ItemsetPattern, ... ]
"""
def run(data, minsup):
    prepare_working_dir()
    prepare_input(data)
    lcm(minsup)
    result = arrange_output()
    delete_working_dir()
    return result

"""
seek suit minsup by binary search.
max waiting time is `timeout * try_count`.

timeout: seconds
try_count: depth of binary search. minsup is seeked in units of 6.25% when try_count is 4, and 1.5625% when try_count is 6.
"""
def run_auto(data, min_minsup=2, *, timeout=20, try_count=6):

    @wrapt_timeout_decorator.timeout(timeout)
    def timeout_lcm(minsup):
        lcm(minsup)

    prepare_working_dir()
    prepare_input(data)
    saved = None
    saved_minsup = None
    minsup = len(data)
    next_sign = -1
    d = 1
    bef_minsup = None
    for i in range(try_count):
        d *= 2
        unit = round(len(data) / d)
        if unit == 0: unit = 1
        minsup = minsup + next_sign * unit
        if minsup < min_minsup:
            minsup = min_minsup
        if bef_minsup == minsup:
            break
        logger.debug(f"{i+1}-th time try. minsup:{minsup}")
        try:
            timeout_lcm(minsup)
        except TimeoutError:
            logger.debug("  timeout")
            next_sign = 1
        except NoFrequentItemError as err:
            logger.debug(str(err))
            next_sign = -1
        else:
            logger.debug("  ended")
            saved = arrange_output()
            saved_minsup = minsup
        run_auto.tried_count = i + 1
        bef_minsup = minsup
    if saved is None:
        raise FailedAutoMinsupError("Failed to find minsup automatically")
    logger.info(f"auto seeded minsup:{saved_minsup}")
    delete_working_dir()
    return saved_minsup, saved
run_auto.tried_count = -1

class FailedAutoMinsupError(ValueError):
    pass

