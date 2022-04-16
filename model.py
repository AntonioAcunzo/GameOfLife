import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal

# Observable class for observe value changed in model
class Observable(QObject):
    value_changed = pyqtSignal(object)

    def __init__(self):
        super().__init__()

    # Register observers
    def register(self, slot):
        self.value_changed.connect(slot)

    # Notify the change
    def notify(self):
        self.value_changed.emit(self)

class GolModel(Observable):
    """
    Model class for Game of life
    Composed by:
    - grid for evolution of the game
    - flag relative to the run action
    - number of step of simulation
    - speed (fps) of simulation
    """

    def __init__(self):
        super().__init__()

        self._running = False
        self._step = 0
        self._fps = 1
        self._gridSize = [50,50]
        self._gridSizeSelected = [10,10]
        self._grid = np.zeros((self._gridSize[0],self._gridSize[1]), dtype=np.uint8)

    # Getter and setter method

    def getStep(self):
        return self._step

    def setStep(self, step):
        self._step = step
        self.notify()

    def getFps(self):
        return self._fps

    def setFps(self, speed):
        self._fps = speed
        self.notify()

    def isRunning(self):
        return self._running

    def setRunning(self, bool):
        self._running = bool
        self.notify()

    def getGrid(self):
        return self._grid

    def setGrid(self, grid):
        self._grid = grid
        self.notify()

    def getGridSizeSelected(self):
        return self._gridSizeSelected

    def setGridSizeSelected(self, size_text):
        self._gridSizeSelected[0] = int(size_text[0:2])
        self._gridSizeSelected[1] = int(size_text[3:5])
        self.notify()

    def getGridSize(self):
        return self._gridSize

    def clearGrid(self):
        print("Clear Grid")
        self._grid = np.zeros((self._gridSize[0], self._gridSize[1]), dtype=np.uint8)
        self.notify()

    def changeStateCell(self, row , col):
        print("changeStateCell")
        self._grid[row][col] = 1 if self._grid[row][col] == 0 else 0
        self.notify()