#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import ctypes

try:
    from PyQt4 import QtCore,QtGui
    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
except ImportError as error:
    from PySide import QtCore,QtGui
    QtGui.QFileDialog.getOpenFileNameAndFilter = QtGui.QFileDialog.getOpenFileName
    
from mainwindowui import Ui_MainWindow
from model import MatchController

class Communicate(QtCore.QObject): 
    episodelistempty = QtCore.Signal(bool)
    episodelistanyselected = QtCore.Signal(bool)
    stateChanged = QtCore.Signal(int)

class MainWindow(QtGui.QMainWindow):
    
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.icon = QtGui.QIcon('icons/subs.ico')
        self.setWindowIcon(self.icon)
        homeDir = QtGui.QDesktopServices.storageLocation(QtGui.QDesktopServices.HomeLocation)
        downloadDir = homeDir +'/Downloads'
        if os.path.exists(downloadDir): self.workdir = downloadDir
        else: self.workdir = homeDir
        self.c = Communicate()
        self.ui = Ui_MainWindow()
        self.controller = None
        self.entrylist = None
        self.setupUi()

    def setupUi(self):

        self.ui.setupUi(self)
        self.ui.dirselbutton.clicked.connect(self.selectdir)
        self.ui.gobutton.clicked.connect(self.renamesubs)
        self.ui.refreshbutton.clicked.connect(self.refresh)
        self.c.episodelistempty.connect(self.ui.selectallbutton.setDisabled)
        self.c.episodelistempty.connect(self.ui.deselectallbutton.setDisabled)
        self.c.episodelistanyselected.connect(self.ui.gobutton.setEnabled)
        self.refresh()
        self.show()

    def selectdir(self):
        newdir = QtGui.QFileDialog.getExistingDirectory(self, self.tr('Select Directory'), self.workdir)
        if len(newdir)>0:
            self.workdir = str(newdir)
            self.refresh()
            
    def refresh(self):
        self.controller = MatchController(self.workdir)
        self.ui.dirlineedit.setText(self.workdir)
        if self.entrylist: del self.entrylist
        self.entrylist = EpisodeList(self.c, self.controller, self)
        self.ui.selectallbutton.clicked.connect(self.entrylist.selectall)
        self.ui.deselectallbutton.clicked.connect(self.entrylist.deselectall)
        self.ui.scrollArea.setWidget(self.entrylist)
        matches = self.controller.getmatches()
        for episode,subtitle in matches:
            self.entrylist.add(episode,subtitle,self.workdir)
            
    def renamesubs(self):
        selection = self.entrylist.getselected()
        if len(selection)>0:
            count = self.controller.renamesubs(selection)
#             QtGui.QMessageBox.information(self,self.tr("Matching complete"), "{} {}".format(count, self.tr('episodes where matched with their subs')),QtGui.QMessageBox.Ok)
            QtGui.QMessageBox.information(self,self.tr("Matching complete"), self.tr('{} episodes where matched with their subs').format(count),QtGui.QMessageBox.Ok)
            self.refresh()
        
    def selectallaction(self): 
        if self.entrylist: self.entrylist.selectall()
        
    def deselectallaction(self): 
        if self.entrylist: self.entrylist.deselectall()
        

class EpisodeList(QtGui.QWidget):
    def __init__(self,comm,controller, parent=None):
        super(EpisodeList,self).__init__(parent)
        self.c = comm
        self.controller = controller
        self.episodeslayout = QtGui.QVBoxLayout(self)
        self.entries = []
        self.noentrieslabel = QtGui.QLabel(self)
        self.noentrieslabel.setText(self.tr('No episodes to match were found on this directory'))
        self.noentrieslabel.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.episodeslayout.addWidget(self.noentrieslabel)
        self.c.episodelistempty.emit(True)
        self.c.episodelistanyselected.emit(False)
        self.c.stateChanged.connect(self.stateChanged)
        
    def add(self,episode,subtitle=None,workdir=None):
        self.noentrieslabel.hide()
        self.c.episodelistempty.emit(False)
        entry=EpisodeEntry(self.c, self.controller, self, len(self.entries)+1,episode,subtitle,workdir)
        self.entries.append(entry)
        self.episodeslayout.addWidget(entry)
        self.c.episodelistanyselected.emit(True)

        
    def getselected(self):
        return [ entry.getepisode() for entry in self.entries if entry.isselected() ]
        
    def selectall(self): 
        for entry in self.entries: entry.select()     
        
    def deselectall(self): 
        for entry in self.entries: entry.deselect()
        
    def stateChanged(self,state):
        if state == QtCore.Qt.Checked:
            self.c.episodelistanyselected.emit(True)
        else:
            self.c.episodelistanyselected.emit(self.checkAnySelected())
        
    def checkAnySelected(self):
        return any([entry.isselected() for entry in self.entries])
            

class EpisodeEntry(QtGui.QGroupBox):
    
    BGCOLOURS = ('white','lightGrey')
    
    def __init__(self,comm,controller,parent,number,episode,subtitle=None,workdir=None):
        super(EpisodeEntry,self).__init__(parent)
        self.controller = controller
        self.episode = episode
        self.subtitle = subtitle
        self.parent = parent
        self.number = number
        self.c = comm
        if workdir: self.workdir = workdir
        else: self.workdir = os.getcwd()
        self.setupUi()
        
    def setupUi(self):
        self.setStyleSheet("QGroupBox {{ background-color: {} }}".format(EpisodeEntry.BGCOLOURS[self.number % 2]))
        self.layout = QtGui.QHBoxLayout(self)
        self.checkbox = QtGui.QCheckBox(self)
        self.checkbox.setText(os.path.basename(self.episode))
        self.layout.addWidget(self.checkbox)
        self.layout.addStretch()
        self.sublabel = QtGui.QLabel(self)
        self.layout.addWidget(self.sublabel)        

        self.subselect = QtGui.QPushButton(self.tr('Change'),self)
        self.subselect.clicked.connect(self.changesub)
        self.layout.addWidget(self.subselect)
        self.subunmatch = QtGui.QPushButton(self.tr('Unmatch'),self)
        self.subunmatch.clicked.connect(self.unmatchsub)
        self.layout.addWidget(self.subunmatch)
        self.updatecontent()
        
        self.show()
        
    def updatecontent(self):
        if self.subtitle:
            self.sublabel.setText(os.path.basename(self.subtitle))
            self.checkbox.setCheckable(True)
            self.checkbox.setChecked(True)
            self.subunmatch.setEnabled(True)
            self.checkbox.setStyleSheet("font-weight: bold; color: black;")
            self.sublabel.setStyleSheet("font-weight: bold; color: black;")
            self.subselect.setStyleSheet("color: black;")
        else :
            self.sublabel.setText(' (no matching subtitle)')
            self.checkbox.setStyleSheet("font-weight: bold; color: red;")
            self.sublabel.setStyleSheet("font-weight: bold; color: red;")
            self.subselect.setStyleSheet("color: red;")
            self.checkbox.setChecked(False)
            self.checkbox.setCheckable(False)
            self.subunmatch.setDisabled(True)
        self.checkbox.stateChanged.connect(self.stateChanged)

        
    def changesub(self):
        title = "{} {}".format(self.tr("Choose Subtitle for"),os.path.basename(self.episode))
        fltr = self.tr("Subtitle files (*.sub *srt)")
        newsub,_ = QtGui.QFileDialog.getOpenFileNameAndFilter(self, title, self.workdir,fltr,fltr, QtGui.QFileDialog.ReadOnly)
        newsub = str(newsub)
        if len(newsub)==0: return
        if self.controller.issubavailable(newsub):    
            self.subtitle = newsub
            self.controller.newmatch(self.episode,self.subtitle)
            self.updatecontent()
        else:
            QtGui.QMessageBox.warning(self,self.tr("Subtitle Already in Use"), self.tr("The subtitle selected was already matching another episode"),QtGui.QMessageBox.Ok)
            self.changesub()
            
    def unmatchsub(self):
        self.subtitle = ""
        self.controller.newmatch(self.episode,self.subtitle)
        self.updatecontent()
            
    def isselected(self): return self.checkbox.isChecked()
    
    def select(self): self.checkbox.setChecked(True)
    
    def deselect(self): self.checkbox.setChecked(False)

    def getepisode(self): return self.episode
    
    def stateChanged(self,state): self.c.stateChanged.emit(state)
    
if __name__ == '__main__':
    try: ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('GameLog')
    except: pass
        #Disable output on windows when using pythonw to avoid filling buffers
    if os.path.basename((sys.executable)) == "pythonw.exe":
        f=open(os.devnull,'w')
        sys.stdout=f
        sys.stderr=f    
        
    translator = QtCore.QTranslator()
    if not translator.load(QtCore.QLocale.system().name(),'i18n/'):
        translator.load('i18n/es_ES')
    app = QtGui.QApplication(sys.argv)
    app.installTranslator(translator)
    mw = MainWindow()
    sys.exit(app.exec_())