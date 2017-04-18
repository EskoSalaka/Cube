"""The MainWindowMenuBar class module."""

from PyQt5 import QtWidgets
from .StandardGenerationDialog import Ui_Dialog as StandardGenerationDialog
from .BasicLandDialog import Ui_LandImageDialog as BasicLandDialog
from .SetNameEditorDialog import SetNameEditorDialog
from .UpdateDialog import UpdateDialog

################################################################################
class MainWindowMenuBar(QtWidgets.QMenuBar):
    """menubar for the mainWindow."""

#-------------------------------------------------------------------------------
    def __init__(self, parent, mainFrameParent):
        """"""
        print(100)
        
        super(MainWindowMenuBar, self).__init__(parent)
        print(100)
        self._mainFrameParent = mainFrameParent
        print(100)
        #------------------------
        fileMenu = QtWidgets.QMenu('&File', self)
        
        exitAction = QtWidgets.QAction('&Quit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self._quit)
        print(100)
        saveDeckAction = QtWidgets.QAction('&Save deck as', self)
        saveDeckAction.setStatusTip('Save deck as')
        saveDeckAction.triggered.connect(self._saveDeckAs)
        
        openDeckAction = QtWidgets.QAction('&Open a deck', self)
        openDeckAction.setStatusTip('Open a deck')
        openDeckAction.triggered.connect(self._openDeck)
        
        fileMenu.addActions([openDeckAction, saveDeckAction])
        fileMenu.addSeparator()
        fileMenu.addActions([exitAction])
        
        #------------------------
        sealedMenu = QtWidgets.QMenu('&Sealed deck generation', self)
        
        standardAction = QtWidgets.QAction('&Standard sealed deck', self)
        standardAction.setStatusTip('Generate a standard booster sealed deck')
        standardAction.triggered.connect(self._standardSealed)
        
        cubeMenu = QtWidgets.QMenu('&Sealed deck from a cube', self)
        sealedMenu.addMenu(cubeMenu)
        
        fromMWSDeckAction = QtWidgets.QAction('&.MWSDeck file', self)
        fromMWSDeckAction.setStatusTip('Generate a sealed deck from a custom cube in MWSDeck format')
        fromMWSDeckAction.triggered.connect(self._cubeSealedFromMWSDeck)
        
        fromCubeFileAction = QtWidgets.QAction('&.Cube file', self)
        fromCubeFileAction.setStatusTip('Generate a sealed deck from a custom cube in .cube file')
        fromCubeFileAction.triggered.connect(self._cubeSealedFromCubeFile)
        
        fromTextFileAction = QtWidgets.QAction('&.txt file', self)
        fromTextFileAction.setStatusTip('Generate a sealed deck from a custom cube in .txt file')
        fromTextFileAction.triggered.connect(self._cubeSealedFromTextFile)
        
        sealedMenu.addActions([standardAction])
        cubeMenu.addActions([fromMWSDeckAction, fromCubeFileAction, fromTextFileAction])
        
        #------------------------
        settingsMenu = QtWidgets.QMenu('&Settings', self)
        
        imageFolderAction = QtWidgets.QAction('&Set image folder', self)
        imageFolderAction.setStatusTip('Set the folder containing the card images')
        imageFolderAction.triggered.connect(self._imageFolder)
        
        landImageAction = QtWidgets.QAction('&Set images for basic lands', self)
        landImageAction.setStatusTip('Set the images for basic lands to use wit hMWS')
        landImageAction.triggered.connect(self._setBasicLandImages)
        
        autoUpdateStatsWidgetAction = QtWidgets.QAction('&Automatically update the statistics panel', self)
        autoUpdateStatsWidgetAction.setStatusTip('Update the database')
        autoUpdateStatsWidgetAction.toggled.connect(self._autoUpdateStatsWidgetAction)
        autoUpdateStatsWidgetAction.setCheckable(True)
        print(105)

        settingsMenu.addActions([imageFolderAction, landImageAction,
                                 autoUpdateStatsWidgetAction])
        print(105)
        #------------------------
        databaseMenu = QtWidgets.QMenu('&Database', self)
        
        updateAction = QtWidgets.QAction('&Update the database', self)
        updateAction.setStatusTip('Update the database')
        updateAction.triggered.connect(self._update)
        
        editSetNamesAction = QtWidgets.QAction('&Edit set names and codes', self)
        editSetNamesAction.setStatusTip('Edit set names and codes')
        editSetNamesAction.triggered.connect(self._editSetNames)
        
        setCodeFormatMenu = QtWidgets.QMenu('&Set predefined setcodes for all the sets', self)
        setCodeFormatMenu.setStatusTip('Set predefined setcodes for all the sets')
        
        mwsSetCodesAction = QtWidgets.QAction('&MWS setcodes', self)
        mwsSetCodesAction.setStatusTip('MWS setcodes')
        mwsSetCodesAction.triggered.connect(self._setMwsSetcodes)
        
        wizardsSetCodesAction = QtWidgets.QAction('&Wizards official setcodes', self)
        wizardsSetCodesAction.setStatusTip('Wizards official setcodes')
        wizardsSetCodesAction.triggered.connect(self._setWizardsSetcodes)
        
        editSetNamesAction = QtWidgets.QAction('&Edit set names and codes', self)
        editSetNamesAction.setStatusTip('Edit set names and codes')
        editSetNamesAction.triggered.connect(self._editSetNames)
        
        formatAction = QtWidgets.QAction('&Format the database', self)
        formatAction.setStatusTip('Format the database')
        formatAction.triggered.connect(self._format)
        print(101)
        
        setCodeFormatMenu.addActions([mwsSetCodesAction, wizardsSetCodesAction])
        databaseMenu.addActions([editSetNamesAction, updateAction, formatAction])
        databaseMenu.addMenu(setCodeFormatMenu)
        
        #------------------------
        self.addMenu(fileMenu)
        self.addMenu(sealedMenu)
        self.addMenu(settingsMenu)
        self.addMenu(databaseMenu)
       

#==========================================================================#
#                              Actions                                     #
#==========================================================================#

#-------------------------------------------------------------------------------
    def _quit(self):
        """Exits program."""

#-------------------------------------------------------------------------------
    def _standardSealed(self):
        """Opens a dialog for creating a standard booster sealed deck."""
        
        StandardGenerationDialog(self.parent(), self._mainFrameParent)
        
#-------------------------------------------------------------------------------
    def _imageFolder(self):
        """Sets the imagefolder"""
        
        caption = 'Choose the folder that contains the card images'
        path = QtWidgets.QFileDialog.getExistingDirectory(caption=caption)
        
        if path:
            self._mainFrameParent.configure(picsFolder=str(path))
            self._mainFrameParent.cardImageWidget._picsFolder = path

#-------------------------------------------------------------------------------
    def _setBasicLandImages(self):
        """Exits program."""
        
        BasicLandDialog(self.parent(), self._mainFrameParent)
        
#-------------------------------------------------------------------------------
    def _saveDeckAs(self):
        """"""
        
        self._mainFrameParent.configure(currentDeckPath='', currentDeckSaved=False)
        self._mainFrameParent.saveDeckAs()
        
#-------------------------------------------------------------------------------
    def _openDeck(self):
        """Opens a deck in mws format and loads the cards in correct lists."""
        
        self._mainFrameParent.openMWSDeck()
        

#-------------------------------------------------------------------------------
    def _cubeSealedFromMWSDeck(self):
        """
        Calls the mainwindows method for creating a cube sealed from an 
        mwsdeckfile.
        """
        
        self._mainFrameParent.cubeSealedFromMWSDeckFile()

#-------------------------------------------------------------------------------
    def _editSetNames(self):
        """
        Opens the set name editor dialog.
        """
        
        SetNameEditorDialog(self._mainFrameParent, 
                            self._mainFrameParent)
        
#-------------------------------------------------------------------------------
    def _update(self):
        """
        Updates the program database from online.
        """
        
        UpdateDialog(self._mainFrameParent, 
                     self._mainFrameParent)

#-------------------------------------------------------------------------------
    def _cubeSealedFromCubeFile(self):
        """
        Calls the mainwindows method for creating a cube sealed from a 
        cube file.
        """
        
        self._mainFrameParent.cubeSealedFromCubeFile()

#-------------------------------------------------------------------------------
    def _cubeSealedFromTextFile(self):
        """
        Calls the mainwindows method for creating a cube sealed from a 
        text file.
        """
        
        self._mainFrameParent.cubeSealedFromTextFile()

#-------------------------------------------------------------------------------
    def _autoUpdateStatsWidgetAction(self, toggled):
        """
        Checks if the option to autoupdate the statswidgetpanel is toggled
        and configures the setting.
        """
        
        if toggled:
            self._mainFrameParent.configure(autoUpdateStatsWidget=1)
        else:
            self._mainFrameParent.configure(autoUpdateStatsWidget='')

#-------------------------------------------------------------------------------
    def _format(self, toggled):
        """
        Formats the database.
        """
        
        title = 'Format database'
        msg = 'Really format the database? This cannot be undone.'
        
        reply = QtWidgets.QMessageBox.question(self, title, msg,
                                               QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.Cancel)
        
        if reply == QtWidgets.QMessageBox.Yes:
            db = self._mainFrameParent.getDatabase()
            db.format()
            self._mainFrameParent.saveDatabase(db)

#-------------------------------------------------------------------------------
    def _setWizardsSetcodes(self):
        """
        Sets the Wizards official setcodes to all the mtgsets in the database.
        """
        

#-------------------------------------------------------------------------------
    def _setMwsSetcodes(self):
        """
        Sets the MWS setcodes to all the mtgsets in the database.
        """
        
        mwsSetCodes = self._mainFrameParent.getMwsSetCodes()
        db = self._mainFrameParent.getDatabase()
        
        for (setName, setCode) in mwsSetCodes.iteritems():
            if db.hasMtgSet(mtgSetName=setName.title()):
                db.editSetName(origMtgSetName=setName.title(), 
                               newMtgSetCode=setCode.upper())
        
        self._mainFrameParent.saveDatabase(db)
        
        
