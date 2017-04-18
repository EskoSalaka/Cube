"""CardPile-class module."""

from PyQt4 import QtCore, QtGui 

################################################################################
class CardPile:
    """
    A class representing a pile of cards in the visual mode canvas. It has
    useful methods of keeping cards in order on top of each other.
    """

#-------------------------------------------------------------------------------
    def __init__(self, parentCanvas):
    
        #------------------------------------
        self._cardLabels = []
        self._topLeft = (0, 0)

        #------------------------------------
        

        #------------------------------------

#==========================================================================#
#                              Public methods                              #
#==========================================================================#
#-------------------------------------------------------------------------------
    def addCardLabel(self, cardLabel, index):
        """
        Adds a cardlabel to the pile in a given position.
        """
        
        cardLabel.move(self._topLeft[0], self._topLeft[1] + 20 * index)
        
        self._cardLabels.insert(index, cardLabel)
        cardLabel._pile = self
        
        self._moveSectionDown(index + 1)
            
    
#-------------------------------------------------------------------------------
    def removeCardLabel(self, cardLabel):
        """
        Removes a cardlabel to the pile.
        """
        
        cardLabelIndex = self.cardLabelPosition(cardLabel)
        self._cardLabels.remove(cardLabel)
        self._moveSectionUp(cardLabelIndex)
    
#-------------------------------------------------------------------------------
    def cardLabelPosition(self, cardLabel):
        """
        Returns the position of the cardLabel in the pile
        """
        
        return self._cardLabels.index(cardLabel)
    
#-------------------------------------------------------------------------------
    def movePile(self, x, y):
        """
        Moves the whole pile an offset of (x, y).
        """
        
        for label in self._cardLabels:
            label.move(x,y)
        
        self._topLeft = (self._topLeft[0] + x, self._topLeft[1] + y)
        
#-------------------------------------------------------------------------------
    def getRect(self, cardLabel):
        """
        Returns the rect of the pile. Basically the rects coordinates are the
        top ones of the highest card and bottom ones of the lowest.
        """
        
        if not self._cardLabels:
            return QtCore.QRect()
        
        topRect = self._cardLabels[0].rect()
        bottomRect = self._cardLabels[-1].rect()
        
        QtCore.QRect(topRect.left(), topRect.top(), 
                     topRect.right(), bottomRect.bottom)
    
#-------------------------------------------------------------------------------
    def intersects(self, rect):
        """
        Adds a cardlabel to the pile.
        """
        
        pass

#-------------------------------------------------------------------------------
    def sortByName(self):
        """
        Sorts the pile's cards by name.
        """
        
        pass
#==========================================================================#
#                              Private methods                             #
#==========================================================================#

#-------------------------------------------------------------------------------
    def _moveSectionUp(self, sectionIndex):
        """
        Moves a section of the pile upwards to replace an empty spot. Used 
        after a card is removed somewhere from the pile. Given section
        index tells which section to move.
        """
        
        for label in self._cardLabels[sectionIndex:]:
            label.move(label.pos().x(), label.pos().y() - 20)
            label.raise_()
            

#-------------------------------------------------------------------------------
    def _moveSectionDown(self, sectionIndex):
        """
        Moves a section of the pile downwards to make an empty spot. Used 
        after a card is inserted somewhere in the pile. Given section
        index tells which section to move.
        """
        
        for label in self._cardLabels[sectionIndex:]:
            label.move(label.pos().x(), label.pos().y() + 20)
            label.raise_()

#==========================================================================#
#                              Internal methods                            #
#==========================================================================#

#==========================================================================#
#                              Properties                                  #
#==========================================================================#