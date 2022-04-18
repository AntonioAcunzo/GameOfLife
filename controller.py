from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from model import GolModel
from view import GolView
import numpy as np

class GolController:
    """
        Controller class for Game of Life
        Composed by:
        - cells for evolution of the game
        - layout for the part where costruct the grid

        RULES of the Game

         - If a cell is ON and has fewer than two neighbors that are ON, it turns OFF
         - If a cell is ON and has either two or three neighbors that are ON, it remains ON.
         - If a cell is ON and has more than three neighbors that are ON, it turns OFF.
         - If a cell is OFF and has exactly three neighbors that are ON, it turns ON.

    """



    # Signal definition
    changeStateSignal = QtCore.pyqtSignal(object)

    def __init__(self, application: QApplication, model: GolModel, view: GolView):
        self._application = application
        # load the model and the view
        self._model = model
        self._view = view

        # set timer for simulation
        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.nextStep)

        # connect all the elements on the view to the controller
        self._view.buttonPlay(self.play)
        self._view.buttonPause(self.pause)
        self._view.buttonStep(self.nextStep)
        self._view.buttonClear(self.clear)
        self._view.sliderSpeed(self.modifyFps)
        self._view.comboSizeGridText(self.modifyGridSize)
        self._view.grid.changeStateSignal.connect(self.modifyGrid)


    def play(self):
        """
        Start the game
        """
        self._model.setRunning(not self._model.isRunning())
        if self._model.isRunning():
            interval = 1000 / self._model.getFps()
            self._timer.setInterval(interval)
            self._timer.start()


    def pause(self):
        """
        Stop the game
        """
        self._model.setRunning(False)
        self._timer.stop()

    def nextStep(self):
        """
        Do next step of the game
        """
        print("next Step")
        self._model.setStep(self._model.getStep()+1)

        grid = self._model.getGrid()
        newGrid = np.zeros((grid.shape[0],grid.shape[1]), dtype=np.uint8)
        for i in range(grid.shape[0]):
            for j in range(grid.shape[1]):
                # If a cell is OFF and has exactly three neighbors that are ON, it turns ON
                if grid[i, j] == 0 and self._neighbors(i, j) == 3:
                    newGrid[i, j] = 1

                elif grid[i, j] >= 1:
                    # If a cell is ON and has <2 or >3 neighbors that are ON, it turns OFF
                    if self._neighbors(i, j) < 2 or self._neighbors(i, j) > 3:
                        newGrid[i, j] = 0
                    else:
                    # If a cell is ON and has exactly 2 or 3 neighbors that are ON, it remains ON
                    # The value assigned is based on the number of steps in which the cell is ON
                        newGrid[i, j] = grid[i, j] + 1
                        if grid[i, j] == 255:
                            newGrid[i, j] = grid[i, j]

        self._model.setGrid(newGrid)


    def clear(self):
        """
        Clear the grid and stop the simulation
        """
        self._model.setRunning(False)
        self._timer.stop()
        self._model.setStep(0)
        self._model.clearGrid()

    def modifyFps(self,fps):
        """
        Modify the speed of simulation
        """
        self._model.setFps(fps)

    def _neighbors(self, i, j):
        """
        Find the number of neighbors of cell i,j
        """
        grid = self._model.getGrid()
        # Filter for the conv 3x3
        indexes = []
        indexes.append([i - 1, j - 1])
        indexes.append([i, j - 1])
        indexes.append([i + 1, j - 1])

        indexes.append([i - 1, j])
        indexes.append([i + 1, j])

        indexes.append([i - 1, j + 1])
        indexes.append([i, j + 1])
        indexes.append([i + 1, j + 1])

        indexes = self._checkPadding(indexes, grid.shape[0], grid.shape[1])
        neighbours = 0
        for cell in indexes:
            if grid[cell[0], cell[1]] > 0:
                neighbours += 1
        return neighbours

    def _checkPadding(self, indexes, maxRows, maxCols):
        """
        Control the paddings cell
        """
        notPadding = []
        for index in indexes:
            if index[0] >= 0 and index[1] >= 0 and index [0] < maxRows and index[1] < maxCols:
                notPadding.append(index)
        return notPadding

    def modifyGrid(self, coord_click):
        """
        Modify the cell of grid where the user clicked
        """
        grid = self._model.getGrid()
        click_x = coord_click[0]
        click_y = coord_click[1]
        print("cliccato in ", click_x, " - ", click_y)
        right_click = (grid.shape[0] - self._model.getGridSizeSelected()[0])//2
        grid[right_click + click_x][right_click + click_y] = 1 if grid[right_click + click_x][right_click + click_y] == 0 else 0
        #for i in range(grid.shape[0]):
            #print(grid[i])
        self._model.setGrid(grid)

    def modifyGridSize(self, size_text):
        """
        Modify the size of the grid
        """
        print("E' cambiata la size della griglia nella combobox ")
        print("Nuova size : " , size_text)

        row, col = int(size_text[0:int(size_text.rfind("x"))]), int(size_text[int(size_text.rfind("x")) + 1:5])

        self._model.setGridSizeSelected(size_text)



    def _populateGrid(self, row, col):
        """
        Create a new grid with new size and populate this with the elements of the previous grid
        """
        print("Populate grid ", row, "x", col)
        new_grid = np.zeros((row, col), dtype=np.uint8)
        old_grid = self._model.getGrid()

        if row >= old_grid.shape[0] and col >= old_grid.shape[1]:
            zoom_out = True
            row_min, col_min = old_grid.shape[0],old_grid.shape[1]
        else:
            zoom_out = False
            row_min, col_min = row, col

        diff_row = abs(old_grid.shape[0] - new_grid.shape[0])//2
        diff_col = abs(old_grid.shape[1] - new_grid.shape[1])//2

        for i in range(row_min):
            for j in range(col_min):
                if zoom_out:
                    new_grid[i+diff_row][j+diff_col] = old_grid[i][j]
                else:
                    new_grid[i][j] = old_grid[i+diff_row][j+diff_col]

        self._model.setGrid(new_grid)


