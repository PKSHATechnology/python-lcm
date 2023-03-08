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
def run_auto(data, timeout=20, try_count=6):

    @wrapt_timeout_decorator.timeout(timeout)
    def timeout_lcm(minsup):
        lcm(minsup)

    prepare_working_dir()
    prepare_input(data)
    d = 2
    minsup = len(data) // d
    saved = None
    saved_minsup = None
    for i in range(try_count):
        d *= 2
        unit = len(data) // d
        if unit == 0: unit = 1
        logger.debug(f"{i}-th time try. minsup:{minsup}")
        try:
            timeout_lcm(minsup)
        except TimeoutError:
            logger.debug("  timeout")
            minsup += unit
        except NoFrequentItemError as err:
            logger.debug(str(err))
            minsup -= unit
        else:
            logger.debug("  ended")
            saved = arrange_output()
            saved_minsup = minsup
            minsup -= unit
        if minsup <= 0:
            break
    if saved is None:
        raise FailedAutoMinsupError("Failed to find minsup automatically")
    logger.info(f"auto seeded minsup:{saved_minsup}")
    delete_working_dir()
    return saved_minsup, saved

class FailedAutoMinsupError(ValueError):
    pass

