from pprint import pprint as pp
from pprint import pformat as pf

import os
import subprocess

working_dir = "_lcm_working_dir"
subprocess.call(["mkdir", "-p", working_dir])
fname_input_tmp = os.path.join(working_dir, "tmp_lcm_input.dat")
fname_output_tmp = os.path.join(working_dir, "tmp_lcm_output.dat")

# set of int
class Itemset(set): # item id starts from 0
    pass

class ItemsetPattern:

    def __init__(self, freqency, items, hit):
        self.freqency = int(freqency)
        self.items = items
        self.hit = hit # contains itemset ids which have this pattern # itemset id starts from 0

    def __repr__(self):
        return f"(freq:{self.freqency}, items:{self.items}, hit:{self.hit})"

    def __eq__(self, other):
        conditions = (
                self.freqency == other.freqency,
                self.items == other.items,
                self.hit == other.hit,
                )
        return all(conditions)

def run(data, minsup):
    prepare_input(data)
    lcm(minsup)
    return arrange_output()

"""
Linear time Closed itemset Miner (Uno.)

data: [Itemset, ... ]
return: [ItemsetPattern, ... ]

ref.
    http://research.nii.ac.jp/~uno/codes-j.htm
    http://research.nii.ac.jp/~uno/code/lcm.html
"""
def lcm(minsup):
    cmd = [
            "lcm",
            "CQI",
            fname_input_tmp,
            str(minsup),
            fname_output_tmp,
            ]
    fname_out = open(os.path.join(working_dir, "tmp_lcm_stdout.txt"), "w")
    fname_err = open(os.path.join(working_dir, "tmp_lcm_stderr.txt"), "w")
    subprocess.run(cmd, stdout=fname_out, stderr=fname_err)

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
        pattern = ItemsetPattern(freq, items, hit_list)
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

