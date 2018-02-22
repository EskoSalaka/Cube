import json
import random
from itertools import groupby
from pprint import pprint
from multiprocessing import Process

from persistent import Persistent
from persistent.list import PersistentList
from collections import ChainMap

class PCardList(Persistent):

    def __init__(self, cards=()):
        if type(cards) is PCardList:
            self.cards = PersistentList(cards.cards)
        elif type(cards) is list:
            self.cards = PersistentList(cards)
        else:
            self.cards = PersistentList()

        self.name = ''

    def __getitem__(self, item):
        return self.cards.__getitem__(item)

    def __setitem__(self, key, value):
        self.cards.__setitem__(key, value)

    def __iter__(self):
        return iter(self.cards)

    def __str__(self):
        return str(self.cards)

    def __repr__(self):
        return repr(self.cards)

    def __add__(self, other):
        if type(other) is PCardList:
            return PCardList(self.cards + other.cards)
        elif type(other) is list:
            return PCardList(self.cards + other)

    def __len__(self):
        return self.cards.__len__()

    def append(self, card):
        self.cards.append(card)
        return self

    def extend(self, other):
        if type(other) is PCardList:
            self.cards.extend(other.cards)
        elif type(other) is list:
            self.cards.extend(other)
        return self

    def get(self, invert=False, matchExactly=True, **kwargs):
        qResult = set()

        for (key, val) in kwargs.items():
            if invert:
                if matchExactly:
                    result = [card for card in self if not getattr(card, key) == val]
                else:
                    result = [card for card in self if getattr(card, key) and not set(val).issubset(set(getattr(card, key, [])))]
            else:
                if matchExactly:
                    result = [card for card in self if getattr(card, key) == val]
                else:
                    result = [card for card in self if getattr(card, key) and set(val).issubset(set(getattr(card, key, [])))]
            qResult.update(result)

        return PCardList(list(qResult))

    def getRandomSample(self, num, duplicates=False):
        if duplicates:
            return PCardList([random.choice(self.cards) for _ in range(num)])
        else:
            try:
                return random.sample(self.cards, num)
            except ValueError:
                return PCardList([random.choice(self.cards) for _ in range(num)])

    def getRandomPack(self, numOfCards, numOfRares=1, numOfUncommons=3):
        if not numOfRares:
            numOfRares = int(round(numOfCards / 14.0))

        if not numOfUncommons:
            numOfUncommons = 3 * int(round(numOfCards / 14.0))

        numOfCommons = numOfCards - numOfRares - numOfUncommons

        commons = self.get(rarity='Common').getRandomSample(numOfCommons)
        uncommons = self.get(rarity='Uncommon').getRandomSample(numOfUncommons)
        rares = PCardList()

        if self.get(rarity='Mythic Rare'):
            for _ in range(numOfRares):
                if random.randint(0, 7) == 0:
                    rares.extend(self.get(rarity='Mythic Rare').getRandomSample(1))
                else:
                    rares.extend(self.get(rarity='Rare').getRandomSample(1))
        else:
            rares.extend(self.get(rarity='Rare').getRandomSample(numOfRares))

        return PCardList().extend(commons).extend(uncommons).extend(rares)

    def getStats(self):
        totManacosts = ''
        totC = 0

        for c in self.cards:
            if c.mana_cost:
                totManacosts += c.mana_cost
                digits = ''.join(filter(lambda x: x.isdigit(), c.mana_cost))
                if digits:
                    totC += int(digits)

        creatures = sorted(self.get(types=['Creature'], matchExactly=False), key=lambda c: c.cmc or 0)
        nonCreatures = sorted(self.get(types=['Creature'], matchExactly=False, invert=True)
                                  .get(types=['Land'], invert=True, matchExactly=False), key=lambda c: c.cmc or 0)
        lands = self.get(types=['Land'], matchExactly=False)
        nonLands = creatures + nonCreatures

        cardsByColors = dict((tuple(k), len(list(v))) for k, v in
                      groupby(sorted(self, key=lambda card: card.colors or ['Colorless']),
                              key=lambda card: card.colors or ['Colorless']))

        cmc = dict((k, len(list(v))) for k, v in
                   groupby(nonLands, key=lambda card: card.cmc or 0))

        types = dict((tuple(k), len(list(v))) for k, v in
                     groupby(sorted(self.cards, key=lambda x: x.types or ['None']), key=lambda x: x.types or ['None']))

        creatureCmc = dict((k, len(list(v))) for k, v in
                            groupby(creatures, key=lambda card: card.cmc or 0))

        nonCreatureCmc = dict((k, len(list(v))) for k, v in
                   groupby(nonCreatures, key=lambda card: card.cmc or 0))

        manaSymbols = {'B': totManacosts.count('B'), 'R': totManacosts.count('R'), 'G': totManacosts.count('G'),
                       'U': totManacosts.count('U'), 'W': totManacosts.count('W'), 'C': totC}

        simpleTypes = {'Creature': len(creatures), 'Non-Creature': len(nonCreatures), 'Land': len(lands)}

        try:
            avgCmc = round(float(sum([cmc*num for (cmc, num) in cmc.items()])) / float(sum(cmc.values())), 1)
        except ZeroDivisionError:
            avgCmc = 0

        return {'colors': cardsByColors, 'cmc': cmc, 'types': types, 'nonCreatureCmc': nonCreatureCmc,
                'creatureCmc': creatureCmc, 'manaSymbols': manaSymbols, 'simpleTypes': simpleTypes, 'avgCmc': avgCmc}

    def filterNonPlayableCards(self):
        return PCardList([card for card in self.cards if card.isFrontSide() and card.layout not in
                         ['token', 'plane', 'scheme', 'phenomenon', 'leveler', 'vanguard', 'Conspiracy']])

    def filterBasicLands(self):
        return PCardList([card for card in self.cards if not card.supertypes or 'Basic' not in card.supertypes])

    def filterDuplicateNames(self):
        temp = set()
        return PCardList([card for card in self.cards if card.name not in temp and (temp.add(card.name) or True)])

    def getPool(self):
        return self.filterBasicLands().filterDuplicateNames().filterNonPlayableCards()

    def toMwsStr(self):
        creatures = self.get(types=['Creature'], matchExactly=False)
        nonCreatures = sorted(self.get(types=['Creature'], matchExactly=False, invert=True)
                              .get(types=['Land'], invert=True, matchExactly=False), key=lambda c: c.name)
        lands = sorted(self.get(types=['Land'], matchExactly=False), key=lambda c: c.name)
        print(creatures)
        print(creatures.sorted(lambda c: c.id))

        mwsStr = '// Deck file for Magic Workstation (http://www.magicworkstation.com)\n\n// Lands\n'

        for k, v in groupby(lands, key=lambda card: card.id):
            lst = list(v)
            card = lst[0]
            num = len(lst)
            mwsStr += '{} [{}] {}\n'.format(num, card.set, card.name)

        mwsStr += '\n// Creatures\n'

        for k, v in groupby(creatures, key=lambda card: card.id):
            card = list(v)[0]
            num = len(lst)
            mwsStr += '{} [{}] {}\n'.format(num, card.set, card.name)

        mwsStr += '\n// Non-Creatures\n'

        for k, v in groupby(nonCreatures, key=lambda card: card.id):
            lst = list(v)
            card = lst[0]
            num = len(lst)
            mwsStr += '{} [{}] {}\n'.format(num, card.set, card.name)

        return mwsStr

    def toJSON(self):
        return json.dumps({'cards': [card.__dict__ for card in self.cards]}, sort_keys=True, indent=4)

    def prettyPrint(self):
        for card in self.cards:
            print('{:40s} {:30s} {:25s} {:10s}'.format(str(card.name), str(card.types),
                                                       str(card.mana_cost), str(card.rarity)))

    def sorted(self, func):
        return PCardList(sorted(self.cards, key=func))


