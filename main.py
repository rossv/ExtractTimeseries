
import sys
from PyQt5 import QtWidgets, QtGui
from gui import ExtractorWindow, apply_dark_palette, ICON_DIR

def main():
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QtGui.QIcon(str(ICON_DIR / "extract_timeseries.ico")))
    apply_dark_palette(app)
    win = ExtractorWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
