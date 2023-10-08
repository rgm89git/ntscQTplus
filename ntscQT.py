import os
import sys
from pathlib import Path
import traceback

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QLibraryInfo
from PyQt5.QtCore import QFile, QTextStream
from PyQt5 import QtGui
import darkdetect

import colorama
import qdarktheme

from app import NtscApp
from app import logger

import traceback
from halo import Halo

os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = QLibraryInfo.location(
    QLibraryInfo.PluginsPath
)

def crash_handler(etype, value, tb):
    logger.trace(value)
    traceback.print_exception(etype, value, tb)
    logger.error("Uncaught exception: {0}\n{1}".format(str(value), "\n".join(traceback.format_tb(tb))))
    sys.exit(1)

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# Install exception handler
sys.excepthook = crash_handler

def main():
    translator = QtCore.QTranslator()
    locale = QtCore.QLocale.system().name()

    cls()
    print("📼 ntscQT+")
    #print(f"by RGM, based on JargeZ's "+'\x1B[3m'+"ntscQT"+'\x1B[0m')
    #print("")

    spinner = Halo(text='',color='white')
    spinner.start()

    # if run by pyinstaller executable, frozen attr will be true
    if getattr(sys, 'frozen', False):
        # _MEIPASS contain temp pyinstaller dir
        base_dir = Path(sys._MEIPASS)
        locale_file = str((base_dir / 'translate' / f'{locale}.qm').resolve())
    else:
        base_dir = Path(__file__).absolute().parent
        locale_file = str((base_dir / 'translate' / f'{locale}.qm').resolve())

    #print(f"Try load {locale} locale: {locale_file}")

    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(QtGui.QPixmap("./icon.png")))
    app.installTranslator(translator)

    qdarktheme.setup_theme("dark",corner_shape="sharp")

    spinner.stop()
    print("Loaded.")

    if translator.load(locale_file):
        print(f'Localization loaded: {locale}')  # name, dir
    else:
        print("")
        print("Using default translation")

    window = NtscApp()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
