from PyQt5.QtWidgets import QApplication
from interface.interface import EncryptionApp

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EncryptionApp()
    window.show()
    sys.exit(app.exec_())