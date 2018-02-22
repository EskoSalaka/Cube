from mtgsdk import Set as mtgsdkSet
from mtgsdk import Card as mtgsdkCard
import random
from persistent.list import PersistentList
from persistent import Persistent

from Base.PCardList import PCardList


class PSet(mtgsdkSet, PCardList, Persistent):

    def __init__(self, mtgsdkSeti, cards=[]):
        super(mtgsdkSet, self).__init__()
        super(PCardList, self).__init__()
        self.__dict__.update(mtgsdkSeti.__dict__)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.release_date < other.release_date

    def __le__(self, other):
        return self.release_date <= other.release_date

    def __gt__(self, other):
        return self.release_date > other.release_date

    def __ge__(self, other):
        return self.release_date >= other.release_date

    def __ne__(self, other):
        return not self == other

    def __cmp__(self, other):
        if self.__eq__(other):
            return 0
        elif self.__lt__(other):
            return -1
        else:
            return 1

    def __str__(self):
        return self.name + '(' + self.code + ')'

    @staticmethod
    def clsVars():
        return ['release_date', 'code', 'gatherer_code', 'mkm_id', 'online_only', 'old_code', 'booster',
                'mkm_name', 'block', 'type', 'border', 'name', 'magic_cards_info_code']