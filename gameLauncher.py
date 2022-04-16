import sys
from PyQt5.QtWidgets import QApplication
from controller import GolController
from model import GolModel
from view import GolView

if __name__ == '__main__':

    app = QApplication(sys.argv)

    # Create the model view controller object
    model = GolModel()
    view = GolView(model)
    controller = GolController(app, model, view)

    # Launch the application
    view.show()
    sys.exit(app.exec())
