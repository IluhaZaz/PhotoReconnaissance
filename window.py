import sys

from PyQt5.QtWidgets import QApplication

from base import DetectionProbabilityCounter, DPCinitUI


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = DetectionProbabilityCounter()
    setupUI = DPCinitUI()
    setupUI.initUI(main_window)
    main_window.show()
    sys.exit(app.exec_())
