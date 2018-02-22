import ZODB, ZODB.FileStorage
import transaction
from mtgsdk import Set as mtgsdkSet, Card as mtgsdkCard
from persistent.list import PersistentList

from Base.PCardList import PCardList
from Base.PCard import PCard
from Base.PSet import PSet


class ZODBTools:

    def __init__(self):
        self.storage = ZODB.FileStorage.FileStorage('mydata.fs')
        self.db = ZODB.DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root

        try:
            self.cards = self.root.cards
        except AttributeError:
            self.root.cards = PersistentList()
            self.cards = self.root.cards

        try:
            self.sets = self.root.sets
        except AttributeError:
            self.root.sets = PersistentList()
            self.sets = self.root.sets

    def setNames(self): return [mtgSet.name for mtgSet in self.sets]

    def setCodes(self): return [mtgSet.code for mtgSet in self.sets]

    def setTypes(self): return [set([mtgSet.type for mtgSet in self.sets])]

    def blocks(self): return [set([mtgset.block for mtgset in self.sets])]

    def setTypes(self):
        return [set([mtgSet.type for mtgSet in self.sets])]

    def setCodeDict(self):
        setCodes = {}

        for mtgSet in list(self.sets):
            setCodes[mtgSet.name] = {'code': mtgSet.code, 'gatherer_code': mtgSet.gatherer_code,
                                     'old_code': mtgSet.old_code, 'magic_cards_info_code': mtgSet.magic_cards_info_code}

        return setCodes

    def getSet(self, **kwargs):
        if 'name' in kwargs.keys():
            return next([mtgSet for mtgSet in self.sets if mtgSet.name == kwargs['name']], None)
        elif 'code' in kwargs.keys():
            return next((mtgSet for mtgSet in self.sets if mtgSet.code == kwargs['code']), None)
        elif 'gatherer_code' in kwargs.keys():
            return next([mtgSet for mtgSet in self.sets if mtgSet.gatherer_code == kwargs['gatherer_code']], None)
        elif 'magic_cards_info_code' in kwargs.keys():
            return next([mtgSet for mtgSet in self.sets if
                         mtgSet.magic_cards_info_code == kwargs['magic_cards_info_code']], None)

    def getSets(self, **kwargs):
        if 'card' in kwargs.keys():
            return [mtgSet for mtgSet in self.sets if mtgSet.hasCard(name=kwargs['card'].name)], None
        if 'block' in kwargs.keys():
            return [mtgSet for mtgSet in self.sets if mtgSet.block == kwargs['block']], None
        if 'type' in kwargs.keys():
            return [mtgSet for mtgSet in self.sets if mtgSet.block == kwargs['type']], None

    def updateAll(self):
        psets = PersistentList()
        pcards = PCardList()

        for seti in mtgsdkSet.all():
            pset = PSet(seti)
            setCards = [PCard(card) for card in mtgsdkCard.where(set=seti.code).all()]
            pset.extend(setCards)
            psets.append(pset)
            pcards.extend(setCards)
            print(pset, len(pcards), len(psets))

        self.root.sets = psets
        self.root.cards = pcards
        transaction.commit()
        print(self.sets)
        print(self.cards)

    def reset(self):
        pass
