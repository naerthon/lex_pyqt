import shlex
from PyQt5.QtCore import QFile, QFileInfo, QSettings, Qt, QTextStream
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
        QMessageBox, QTextEdit)

from reservados import PaReservados

class MainWindow(QMainWindow, PaReservados):
    MaxRecentFiles = 5
    windowList = []

    def __init__(self):
        super(MainWindow, self).__init__()

        self.recentFileActs = []

        self.setAttribute(Qt.WA_DeleteOnClose)

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.statusBar()

        self.setWindowTitle('COMPY')
        self.setWindowIcon(QIcon('images/icon.png'))
        self.resize(800, 800)
        self.isUntitled = True

    def newFile(self):
        other = MainWindow()
        MainWindow.windowList.append(other)
        other.show()

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                "Choose a file name", '.', PaReservados.tipos)
        if fileName:
            self.loadFile(fileName)

    def save(self):
        if self.isUntitled:
            return self.saveAs()
        else:
            return self.saveFile(self.curFile)

    def saveAs(self):

        filename, _ = QFileDialog.getSaveFileName(self,
                "Choose a file name", '.', PaReservados.tipos)
        if fileName:
            self.saveFile(fileName)

    def run(self):
        if self.isUntitled:
            self.open()
            self.run()
        else:
            if self.curFile:
                self.fileO = self.curFile
                self.fileO = open(self.fileO, 'r')
                self.fileO = self.fileO.read()
                self.runFile(self.fileO)

    def openRecentFile(self):

        action = self.sender()
        if action:
            self.loadFile(action.data())

    def about(self):
        QMessageBox.about(self, "About Recent Files",
                "The <b>Recent Files</b> example demonstrates how to provide "
                "a recently used file menu in a Qt application.")

    def createActions(self):
        self.newAct = QAction(QIcon('images/file_new.png'),
            "&New", self,
            shortcut=QKeySequence.New,
            statusTip="Create a new file", triggered=self.newFile)

        self.openAct = QAction(QIcon('images/fileopen.png'),
            "&Open...", self,
            shortcut=QKeySequence.Open,
            statusTip="Open an existing file",
            triggered=self.open)

        self.saveAct = QAction(QIcon('images/save.png'),
            "&Save", self,
            shortcut=QKeySequence.Save,
            statusTip="Save the document to disk",
            triggered=self.save)

        self.saveAsAct = QAction("Save &As...", self,
            shortcut=QKeySequence.SaveAs,
            statusTip="Save the document under a new name",
            triggered=self.saveAs)

        for i in range(MainWindow.MaxRecentFiles):
            self.recentFileActs.append(
                    QAction(self, visible=False,
                            triggered=self.openRecentFile))

        self.exitAct = QAction(QIcon('images/exit.png'),
            "E&xit", self,
            shortcut="Ctrl+Q",
            statusTip="Exit the application",
            triggered=QApplication.instance().closeAllWindows)

        self.aboutAct = QAction("&About", self,
            statusTip="Show the application's About box",
            triggered=self.about)

        self.aboutQtAct = QAction("About &Qt", self,
            statusTip="Show the Qt library's About box",
            triggered=QApplication.instance().aboutQt)

        self.runAction = QAction(QIcon('images/run.png'), 'Run', self)
        self.runAction.setShortcut('F5')
        self.runAction.setStatusTip('Run application')
        self.runAction.triggered.connect(self.run)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.separatorAct = self.fileMenu.addSeparator()
        for i in range(MainWindow.MaxRecentFiles):
            self.fileMenu.addAction(self.recentFileActs[i])
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)
        self.updateRecentFileActions()

        self.menuBar().addSeparator()

        self.runMenu = self.menuBar().addMenu('&Run')
        self.runMenu.addAction(self.runAction)

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.toolbar = self.addToolBar("Tools")
        self.toolbar.addAction(self.openAct)
        self.toolbar.addAction(self.saveAct)

        self.toolbar = self.addToolBar("Tools")
        self.toolbar.addAction(self.runAction)

    def runFile(self, fileName):
        fileO = self.fileO
        if fileO:
            lexer = shlex.shlex(fileO)
            lexer.commenters = "//"
            lexer = list(lexer)
            i = 0
            Tokens = []
            for x in lexer:
                if x in PaReservados.reservados:
                    lexer.index(x) + 1
                    c = x
                    Tokens.append(c)
                else:
                    c = c = lexer.index(x) + 1, x
                    Tokens.append(c)

            self.textEdit.setText(str(Tokens))


    def loadFile(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Recent Files",
            "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        instr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        self.textEdit.setPlainText(instr.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = QFile(fileName)

        if not file.open(QFile.WriteOnly | QFile.Text):
            QMessageBox.warning(self, "MDI",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outstr = QTextStream(file)
        QApplication.setOverrideCursor(Qt.WaitCursor)
        outstr << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File saved", 2000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = QFileInfo(fileName).canonicalFilePath()
        self.isUntitled = False
        self.setWindowModified(False)
        if self.curFile:
            self.setWindowTitle("Recent Files %s" % self.strippedName(self.curFile))
        else:
            self.setWindowTitle("Recent Files")

        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        try:
            files.remove(fileName)
        except ValueError:
            pass

        files.insert(0, fileName)
        del files[MainWindow.MaxRecentFiles:]

        settings.setValue('recentFileList', files)

        for widget in QApplication.topLevelWidgets():
            if isinstance(widget, MainWindow):
                widget.updateRecentFileActions()

    def updateRecentFileActions(self):
        settings = QSettings('Trolltech', 'Recent Files Example')
        files = settings.value('recentFileList', [])

        numRecentFiles = min(len(files), MainWindow.MaxRecentFiles)

        for i in range(numRecentFiles):
            text = "&%d %s" % (i + 1, self.strippedName(files[i]))
            self.recentFileActs[i].setText(text)
            self.recentFileActs[i].setData(files[i])
            self.recentFileActs[i].setVisible(True)

        for j in range(numRecentFiles, MainWindow.MaxRecentFiles):
            self.recentFileActs[j].setVisible(False)

        self.separatorAct.setVisible((numRecentFiles > 0))

    def strippedName(self, fullFileName):
        return QFileInfo(fullFileName).fileName()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
