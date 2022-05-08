from pprint import pprint as pp
from pprint import pformat as pf

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

