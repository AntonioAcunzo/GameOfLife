from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QFrame, QWidget
from model import GolModel
from functools import partial



class GolGrid(QWidget):
    """
        Grid class for Game of life
        Composed by:
        - cells for evolution of the game
        - layout for the part where costruct the grid
    """

    # Signal definition
    changeStateSignal = pyqtSignal(object)

    def __init__(self, parent: QtWidgets, model: GolModel, layout):
        QtWidgets.QGraphicsScene.__init__(self)

        # Connect to the model and show the initial grid
        self._model = model
        self._model.register(self._updateGrid)

        # Connect to the part of view where costruct the grid
        self._layout = layout

        # Create the grid with QFrame cells
        self._cells = []
        self._setupUi()
        self._updateGrid()



    def _setupUi(self):
        """
        Initializes ui that contains the cells
        """
        self.setMinimumSize(400, 200)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._initGrid(int(self._model.getGridSizeSelected()[0]),self._model.getGridSizeSelected()[1])

    def _initGrid(self, rows, cols):
        """
        Initializes grid with given rows and cols
        """
        print("Init grid")
        for i in range(rows):
            self._cells.append([])
            for j in range(cols):
                cell = QFrame(self)
                self._setupFrame(cell)
                cell.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
                cell.mousePressEvent = partial(self._cellClick, (i, j))
                self._cells[-1].append(cell)
                self._layout.addWidget(cell, i, j)


    def _setupFrame(self, frame):
        """
        Initialize cell frame
        """
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLineWidth(0.9)
        frame.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))
        frame.setAttribute(Qt.WA_StyledBackground, True)


    def _cellClick(self, _coords, _event):
        """
        Slot connected to QFrame cell clicked with given coordinates.
        """
        self.changeStateSignal.emit([_coords[0], _coords[1]])
        #self.controller.on_cell_clicked(_coords[0], _coords[1])

    def _clearLayout(self):
        """
        Clear all cells
        """
        self._cells.clear()
        self._cells = []
        for i in reversed(range(self._layout.count())):
            self._layout.itemAt(i).widget().setParent(None)

    def _updateGrid(self):
        """
        Update the grid when the size of grid changes or update the color of cells during simulation
        """
        print("Update Grid")

        grid = self._model.getGrid()

        # A different grid dimension has been selected with the combo box
        if self._model.getGridSizeSelected()[0] != self._getRows() and self._model.getGridSizeSelected()[1] != self._getCols():
            print("Size griglia cambiata: ",self._model.getGridSizeSelected()[0] , " - ", self._model.getGridSizeSelected()[1])
            self._clearLayout()
            self._initGrid(self._model.getGridSizeSelected()[0],self._model.getGridSizeSelected()[1])

        # Change cells color
        right_click = (grid.shape[0] - self._model.getGridSizeSelected()[0]) // 2
        for row in range(self._model.getGridSizeSelected()[0]):
            for col in range(self._model.getGridSizeSelected()[1]):

                if grid[right_click + row][right_click + col] == 0:
                    self._cells[row][col].setStyleSheet("background-color: rgb(255, 255, 255);" )
                else:
                    blue = 0
                    if grid[right_click + row][right_click + col] > 0 and grid[right_click + row][right_click + col] <= 150 :
                        blue = 255 - grid[right_click + row][right_click + col]
                        red = 0
                    elif grid[right_click + row][right_click + col] > 150 and grid[right_click + row][right_click + col] <= 255:
                        red = grid[right_click + row][right_click + col]
                    else:
                        red = 255
                    self._cells[row][col].setStyleSheet("background-color: rgb(" + str(red) + ",0," + str(blue) + ");")

    def _getRows(self):
        return self._cells.__len__()

    def _getCols(self):
        row = self._cells[0]
        return row[1]



