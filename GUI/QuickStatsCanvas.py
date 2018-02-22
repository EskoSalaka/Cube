"""QuickStatsCanvas class module."""
from __future__ import unicode_literals

import numpy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib as mpl

from Base.StatisticsAnalyzer import StatisticsAnalyzer


################################################################################
class QuickStatsCanvas(FigureCanvas):
    """
    An implementation of the Matplotlib figure canvas, which is also
    a PyQt4 widget. It displays quick statistics of the deck.
    """

#-------------------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        
        self._figure = Figure(facecolor='0.94')
        FigureCanvas.__init__(self, self._figure)
        
        self._colorDistPie = self._figure.add_subplot(142)
        self._manaCostBar = self._figure.add_subplot(141)
        self._manaSymbolsBar = self._figure.add_subplot(143)
        self._typesPie = self._figure.add_subplot(144)
        
        mpl.rcParams['legend.fontsize'] = 9
        mpl.rcParams['font.size'] = 10
        
        self._figure.tight_layout(rect=[0.0, 0.2, 1, 0.9])
        
        self._statsAnalyzer = StatisticsAnalyzer()
        
        self.Update()

#==========================================================================#
#                              Configuration                               #
#==========================================================================#

#-------------------------------------------------------------------------------
    def removeCardData(self, card):
        """Removes the given cards data from the dictionaries. Not fail safe."""
        
        self._statsAnalyzer.removeCard(card)
        

#-------------------------------------------------------------------------------
    def addCardData(self, card):
        """Adds the given cards data to the stats dictionaries."""
        
        self._statsAnalyzer.addCard(card)

#-------------------------------------------------------------------------------
    def Update(self):
        """Updates and repaints the graphs. """
        
        self._statsAnalyzer.colorDistPie(self._colorDistPie)
        self._statsAnalyzer.manaCostsBar(self._manaCostBar)
        self._statsAnalyzer.manaSymbolsBar(self._manaSymbolsBar)
        self._statsAnalyzer.simpleTypesDistributionPie(self._typesPie)
        self._figure.canvas.draw()
        
#-------------------------------------------------------------------------------
    def clear(self):
        """Clears the list of all data."""
        
        self._statsAnalyzer.clear()
        self.Update()

# -------------------------------------------------------------------------------
    def draw(self, statsDict):

        self._typesDistPie.clear()
        self._typesDistPie.set_title('Type Distribution')

        colors = []
        fracs = []
        labels = []

        if 'Land' in statsDict:
            fracs.append(self._simpleTypes['Land'])
            colors.append('y')
            labels.append('Lands')

        if 'Non-Creature' in statsDict:
            fracs.append(self._simpleTypes['Non-Creature'])
            colors.append('#F0E68C')
            labels.append('Other')

        if 'Creature' in statsDict:
            fracs.append(self._simpleTypes['Creature'])
            colors.append('#FF8C00')
            labels.append('Creatures')

        def autoPct(pct):
            val = int(round(pct * sum(fracs) / 100.0))
            return '{p:.0f}%  ({v:d})'.format(p=pct, v=val)

        self._typesDistPie.pie(fracs, autopct=autoPct, colors=colors, shadow=True)

        if labels:
            self._typesDistPie.legend(labels, loc=(-0.25, -0.22), columnspacing=0.5, frameon=False)

        title = 'Manasymbols'

        yTickLabels = []
        xTickLabels = []
        manaSymbols = []
        sortedColors = []

        self._manaSymbolsBar.clear()

        for (color, num) in self._manaSymbols.items():
            if color == 'C':
                continue

            yTickLabels.append(color)
            manaSymbols.append(num)
            sortedColors.append(self._matplotlibColors[color])

        indices = numpy.arange(0, 5)
        width = 0.7

        rects = self._manaSymbolsBar.barh(indices + width / 2, manaSymbols, width, color=sortedColors)

        self._manaSymbolsBar.set_yticks(indices + width)
        self._manaSymbolsBar.set_xticklabels(xTickLabels)
        self._manaSymbolsBar.set_yticklabels(yTickLabels)
        self._manaSymbolsBar.set_title(title)
        self._manaSymbolsBar.set_ylim([0, 5.5])
        self._manaSymbolsBar.set_xlim([0, max(manaSymbols) + 2])

        for rect in rects:
            self._manaSymbolsBar.text(0.9 + rect.get_width(),
                                      rect.get_y() + width / 2,
                                      '%d' % int(rect.get_width()),
                                      horizontalalignment='center',
                                      verticalalignment='center',
                                      )

        self._manaCostBar.clear()

        title = 'Manacosts'
        xlabel = 'Avg casting cost: ({avgCC})'.format(avgCC=self.getAverageCastingCost())

        xTickLabels = ('0', '1', '2', '3', '4', '5', '6+')
        yTickLabels = ()

        creatureManaCosts = [self._creatureManaCosts[index] for index in range(7)]
        otherManaCosts = [self._nonCreatureManaCosts[index] for index in range(7)]
        totals = [sum(total) for total in zip(creatureManaCosts, otherManaCosts)]

        indices = numpy.arange(0, 7)
        width = 0.7

        rects1 = self._manaCostBar.bar(indices + width / 2, creatureManaCosts, width, color='#FF8C00')

        rects2 = self._manaCostBar.bar(indices + width / 2, otherManaCosts,  width, color='#F0E68C',
                                       bottom=creatureManaCosts)

        self._manaCostBar.set_xticks(indices + width)
        self._manaCostBar.set_xticklabels(xTickLabels)
        self._manaCostBar.set_yticklabels(yTickLabels)
        self._manaCostBar.set_title(title)
        self._manaCostBar.set_xlabel(xlabel)
        self._manaCostBar.set_xlim([0, 7.5])
        self._manaCostBar.set_ylim([0, max(totals) + 2])

        for rect, rect2 in zip(rects1, rects2):
            height = rect.get_height() + rect2.get_height() + 0.2

            self._manaCostBar.text(rect.get_x() + rect.get_width() / 2.0,
                                   0.4 + height,
                                   '%d' % int(height),
                                   horizontalalignment='center',
                                   verticalalignment='center',
                                   )

        self._manaCostBar.legend(['Creatures', 'Other'], loc=(1.0, -0.2), columnspacing=0.5, frameon=False)
