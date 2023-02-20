from .main import run, run_auto, FailedAutoMinsupError
from .adapter import NoFrequentItemError
from .structure import Itemset, ItemsetPattern

import shutil

if shutil.which("lcm") is None:
    raise FileNotFoundError("lcm command is not found. Please install lcm according to README.")

