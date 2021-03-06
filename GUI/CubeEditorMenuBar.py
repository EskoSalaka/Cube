"""The MainWindowMenuBar class module."""

from PyQt5 import QtGui, QtWidgets

################################################################################
class CubeEditorMenuBar(QtWidgets.QMenuBar):
    """menubar for the CubeEditor."""

#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent):
        """"""
        
        super(CubeEditorMenuBar, self).__init__(parent)
        self._mainFrameParent = mainFrameParent
        
        #------------------------
        fileMenu = QtGui.QMenu('&File', self)
        
        exitAction = QtWidgets.QAction('&Quit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self._quit)
        
        newCubeAction = QtWidgets.QAction('&New cube', self)
        newCubeAction.setStatusTip('New cube')
        newCubeAction.triggered.connect(self._newCube)
        
        saveCubeAction = QtWidgets.QAction('&Save cube as', self)
        saveCubeAction.setStatusTip('Save cube as')
        saveCubeAction.triggered.connect(self._saveCubeAs)
        
        openCubeAction = QtWidgets.QAction('&Open a cube', self)
        openCubeAction.setStatusTip('Open a cube')
        openCubeAction.triggered.connect(self._openCube)
        
        fileMenu.addActions([newCubeAction, openCubeAction, saveCubeAction])
        fileMenu.addSeparator()
        fileMenu.addActions([exitAction])
        
        #------------------------
        toolsMenu = QtWidgets.QMenu('&Tools', self)
        
        readFromTxtAction = QtWidgets.QAction('&Read a cube from a text file', self)
        readFromTxtAction.triggered.connect(self._readFromTxtFile)
        
        readFromMwsAction = QtWidgets.QAction('&Read a cube from a MWS deck file', self)
        readFromMwsAction.triggered.connect(self._readFromMwsFile)
        
        cubeToTxtFileAction = QtWidgets.QAction('&Write the cube in a text file as a sorted list', self)
        cubeToTxtFileAction.triggered.connect(self._cubeToSortedTxtFile)
        
        toolsMenu.addActions([readFromTxtAction, readFromMwsAction, cubeToTxtFileAction])
        
        
        #------------------------
        self.addMenu(fileMenu)
        self.addMenu(toolsMenu)
        
       

#==========================================================================#
#                              Actions                                     #
#==========================================================================#

#-------------------------------------------------------------------------------
    def _quit(self):
        """Exits program."""

#-------------------------------------------------------------------------------
    def _newCube(self):
        """Starts a new cube."""
        
        self._mainFrameParent.newCube()
        
#-------------------------------------------------------------------------------
    def _saveCubeAs(self):
        """"""
        
        self._mainFrameParent.configure(currentCubePath='', currentCubeSaved=False)
        self._mainFrameParent.saveCubeAs()
        
#-------------------------------------------------------------------------------
    def _openCube(self):
        """Opens a .cube file  and loads the cards in correct lists."""
        
        self._mainFrameParent.openCube()

#-------------------------------------------------------------------------------
    def _readFromTxtFile(self):
        """Reads cube data from a list in a text file."""
        
        self._mainFrameParent.readFromTxtFile()

#-------------------------------------------------------------------------------
    def _readFromMwsFile(self):
        """Reads cube data from a list in a text file."""
        
        self._mainFrameParent.readFromMwsFile()

#-------------------------------------------------------------------------------
    def _cubeToSortedTxtFile(self):
        """Writes the cube given to a sorted textFile."""
        
        self._mainFrameParent.cubeToTxtFile()
        


        