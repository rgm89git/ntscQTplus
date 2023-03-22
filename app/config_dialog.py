from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets, QtCore, QtGui

from ui import configExportDialog

from pathlib import Path
from app.logs import logger

class ConfigDialog(QDialog, configExportDialog.Ui_TemplateConfigDialog):
    def __init__(self, parent=None):
        super(ConfigDialog, self).__init__(parent)
        self.setupUi(self)
        print("Connect buttons")  # gives the expected output

        # self.connect(self.pushButton_Ok, SIGNAL("clicked()"), self.clickedOk)
        # self.connect(self.pushButton_Cancel, SIGNAL("clicked()"), self.clickedCancel)

        # Alternativly I have tríed the following without improvement:
        # self.pushButton_Ok.clicked.connect(self.clickedOk)
        # QObject.connect(self.pushButton_Cancel, SIGNAL("clicked()"), self.clickedCancel)

        # self.buttonBox.accepted.connect(self.clickedOk)
        self.copyConfigButton.clicked.connect(self.clickedCopy)
        self.openConfigButton.clicked.connect(self.clickedOpen)
        self.exportConfigButton.clicked.connect(self.clickedExport)

    @QtCore.pyqtSlot()
    def clickedCopy(self):
        self.configJsonTextField.selectAll()
        self.configJsonTextField.copy()
    
    @QtCore.pyqtSlot()
    def clickedOpen(self):
        openFile = QtWidgets.QFileDialog.getOpenFileName(self, caption="Open JSON", directory=".", filter="JSON (*.json)")
        if openFile:
            if openFile[0] != "":
                path = Path(openFile[0])
        
                logger.debug(f"Opening preset: {path}")
                with open(path, "r") as f:
                    fileContents = f.read()
                    self.configJsonTextField.setPlainText(fileContents)
                logger.debug(f"Preset loaded!")
            else:
                return None
        else:
            return None
    
    @QtCore.pyqtSlot()
    def clickedExport(self):
        exportFile = QtWidgets.QFileDialog.getSaveFileName(self, caption="Export JSON", directory=".", filter="JSON (*.json)")
        if exportFile:
            if exportFile[0] != "":
                path = Path(exportFile[0])

                logger.debug(f"Exporting preset to {path}")
                fileContents = self.configJsonTextField.toPlainText()
                with open(path, "w") as f:
                    f.write(fileContents)
                logger.debug(f"Preset exported!")
            else:
                return None
        else:
            return None

    @QtCore.pyqtSlot()
    def clickedOk(self):
        print("Ok")  # Question: Why is nothing happening here?
