import json

from mtgsdk import Card as mtgsdkCard
import ZODB
import persistent


class PCard(mtgsdkCard, persistent.Persistent):

    def __init__(self, card):
        super(mtgsdkCard, self).__init__()
        self.__dict__.update(card.__dict__)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ge__(self, other):
        return self.id >= other.id

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
        return self.name

    def __repr__(self):
        return '{}({})'.format(self.name, self.set)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def isFrontSide(self):
        if self.names:
            if self.name == self.names[0]:
                return True
            else:
                return False
        else:
            return True

    def getFlipSideName(self):
        if self.names:
            return [name for name in self.names if name != self.name][0]
        else:
            return None


    @staticmethod
    def clsVars():
        return ['original_text', 'colors', 'names', 'loyalty', 'variations', 'layout', 'source', 'text', 'id', 'cmc',
                'toughness', 'multiverse_id', 'legalities', 'supertypes', 'watermark', 'image_url', 'life',
                'timeshifted', 'set', 'power', 'original_type', 'hand', 'starter', 'name', 'artist', 'border',
                'subtypes', 'flavor', 'set_name', 'rarity', 'number', 'rulings', 'foreign_names', 'mana_cost',
                'types', 'type', 'release_date', 'printings']