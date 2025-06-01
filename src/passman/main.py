from PySide6 import QtUiTools, QtWidgets


def main():
    app = QtWidgets.QApplication([])
    ui_file = "main.ui"
    loader = QtUiTools.QUiLoader()
    win = loader.load(ui_file)
    win.show()
    app.exec()


if __name__ == "__main__":
    main()
