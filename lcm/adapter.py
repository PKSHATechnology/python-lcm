from pprint import pprint as pp
from pprint import pformat as pf

import os
import subprocess

# mine
from .structure import Itemset, ItemsetPattern

working_dir = "_lcm_working_dir"
os.makedirs(working_dir, exist_ok=True)
fname_input_tmp = os.path.join(working_dir, "tmp_lcm_input.dat")
fname_output_tmp = os.path.join(working_dir, "tmp_lcm_output.dat")


class NoFrequentItemError(ValueError):
    pass

"""
Linear time Closed itemset Miner (Uno.)

ref.
    http://research.nii.ac.jp/~uno/codes-j.htm
    http://research.nii.ac.jp/~uno/code/lcm.html

return: flg_successed, msg
"""
def lcm(minsup):
    if os.path.exists(fname_output_tmp): os.remove(fname_output_tmp)
    cmd = [
            "lcm",
            "CQI",
            fname_input_tmp,
            str(minsup),
            fname_output_tmp,
            ]
    fname_out = open(os.path.join(working_dir, "tmp_lcm_stdout.txt"), "w")
    fname_err = open(os.path.join(working_dir, "tmp_lcm_stderr.txt"), "w")
    res = subprocess.run(cmd, stdout=fname_out, stderr=fname_err)
    if res.returncode == -11:
        raise NoFrequentItemError( "there is no frequent item") #TODO raise your own Error class
    if res.returncode != 0:
        print('res', res) # debug
        raise RuntimeError("lcm command raise error. Please look at _lcm_working_dir/tmp_lcm_stderr.txt")
    return True

def prepare_input(data):
    lines = []
    for itemset in data:
        l = " ".join(map(str, itemset))
        lines.append(l)
    open(fname_input_tmp, "w").write("\n".join(lines))

def arrange_output():
    lines = open(fname_output_tmp).readlines()
    pattern_list = []
    i = 0
    while i < len(lines):
        freq, items = parse_line(lines[i]); i += 1;
        hit_list = parse_hit_line(lines[i]); i += 1;
        pattern = ItemsetPattern(items, hit_list)
        pattern_list.append(pattern)
    return pattern_list

def parse_line(l):
    one = l.split(")")
    freq, l = one[0][1:], one[1]
    items = set(map(int, l.strip().split()))
    return freq, items

def parse_hit_line(l):
    hit = set()
    for value in l.split(" "):
        value = value.strip()
        if not value.isnumeric():
            continue
        hit.add(int(value))
    return hit

