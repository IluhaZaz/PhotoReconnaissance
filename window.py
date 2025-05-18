import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from base import DetectionProbabilityCounter, DPCinitUI


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icons\\icon.ico"))
    main_window = DetectionProbabilityCounter()
    setupUI = DPCinitUI()
    setupUI.initUI(main_window)
    main_window.showMaximized()
    sys.exit(app.exec_())
