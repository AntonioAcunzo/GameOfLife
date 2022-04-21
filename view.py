import os
import numpy as np
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog

from main_window_ui import Ui_MainWindow

from model import GolModel
from grid import GolGrid

CURRENT_DIR = os.path.dirname(os.path.abspath('__file__'))

class GolView(QMainWindow, Ui_MainWindow):
    """
        View class for Game of Life
        Composed by:
        - cells for evolution of the game
        - layout for the part where costruct the grid
    """

    def __init__(self, model:GolModel):
        super().__init__()

        self.setupUi(self)

        self.connectSignalsSlots()

        # Observe the Game of Life Model
        self._model = model
        self._model.register(self._updateView)

        self.grid = GolGrid(self, self._model, self.getLayoutGrid())


    def getGrid(self):
        return self.grid

    def getLayoutGrid(self):
        return self.gridLayoutWidget


    def connectSignalsSlots(self):
        # Create action for menu operation
        self.action_Open.triggered.connect(self._open)
        self.action_Save.triggered.connect(self._save)
        self.action_Exit.triggered.connect(QApplication.exit)

        self.action_Rules.triggered.connect(self.rules)
        self.action_How_to_play.triggered.connect(self.how_to_play)

    def _open(self):
        """
        Action connected to load menu item
        Load a grid configuration from file
        """
        if(not self._model.isRunning()):
            print('Open pattern')
            try:
                path = QFileDialog.getOpenFileName(directory=CURRENT_DIR)
                if path[0] != '':
                    print("Path file : " , path)

                    grid, originalRows, originalCols = self._gridFromFile(path[0])

                    self._model.setGrid(grid)

                    size_text = '{}x{}'.format(originalRows, originalCols)

                    self.gridComboBox.setCurrentIndex(4)




            except Exception:
                print('File opening failed')
                QMessageBox.about(self, "Load Error", "File selected is not valid!")

        else:
            #print("Messaggio Errore")
            QMessageBox.about(self, "Load Error", "Stop the simulation for load a configuration!")


    def _gridFromFile(self,path):
        """
        Read a configuration from file selected and create a grid
        """
        print("Grid From File")
        config = []
        with open(path, 'r') as file:
            lines = file.readlines()
            rows = 0
            cols = 0
            for line in lines:
                #print("Line : ",line)

                if not line.startswith('!') and line != "":
                    rows += 1

                    if cols <= len(line)-1:
                        cols = len(line)-1
                    row = []

                    for symbol in reversed(line):
                        #print("symbol : ", symbol)
                        if symbol == '.':
                            row.append(0)
                        if symbol == 'O':
                            row.append(1)

                    config.append(row)

            for row in config:
                for i in range(cols-len(row)):
                    row.insert(0,0)

        grid = np.zeros((self._model.getGridSize()[0], self._model.getGridSize()[1]), dtype=np.uint8)

        # print(rows)
        # print((self._model.getGridSize()[0] - rows))
        # print((self._model.getGridSize()[0] - rows) // 2)

        for i in range(rows):
            for j in range(cols):
                print(i + (self._model.getGridSize()[0] - rows) // 2 , " - " , j + (self._model.getGridSize()[1] - cols)//2)
                grid[i + (self._model.getGridSize()[0] - rows)//2][j + (self._model.getGridSize()[1] - cols)//2] = config[i][j]


        return grid, rows, cols

    def _save(self):
        """
        Action connected to save menu item
        Save the grid configuration on file
        """
        if (not self._model.isRunning()):
            print('save pattern')
            try:
                path = QFileDialog.getSaveFileName(directory=CURRENT_DIR)
                if path[0] != '':
                    print(path)
                    self._gridOnFile(path,self._model.getGrid())

            except Exception:
                print('File saving failed')
                QMessageBox.about(self, "Save Error", "Error while saving the file!")

        else:
            # print("Messaggio Errore")
            QMessageBox.about(self, "Save Error", "Stop the simulation for save the configuration!")

    def _gridOnFile(self, path, grid):
        """
        Write the current configuration on file
        """
        with open(path[0], 'w') as file:
            file.write("!Name: "+ path[0] + "\n")
            for row in grid:
                for element in row:
                    file.write("0" if element == 1 else ".")
                file.write("\n")

    def rules(self):
        """
        QMessageBox with rules of the game
        """
        QMessageBox.about(
            self,
            "Rules",
            "<p><b>GAME OF LIFE RULES :</b></p>"
            "<p>1) If a cell is ON and has fewer than two neighbors that are ON, it turns OFF </p>"
            "<p>2) If a cell is ON and has either two or three neighbors that are ON, it remains ON </p>"
            "<p>3) If a cell is ON and has more than three neighbors that are ON, it turns OFF </p>"
            "<p>4) If a cell is OFF and has exactly three neighbors that are ON, it turns ON </p>"
        )

    def how_to_play(self):
        """
            QMessageBox with instructions on how to use the program
        """
        QMessageBox.about(
            self,
            "How to play",
            "<p><b>HOW TO PLAY :</b></p>"
            "<p> - Load default configuration or create a custom one by clicking on the grid to make a cell dead or alive. </p>"
            "<p> - Save the grid configuration with the action in the menù file. </p>"
            "<p><b>CONTROLS :</b></p>"
            "<p> - Click play button to start the simulation of the game. </p>"
            "<p> - Click next step button to do a single iteration of game. </p>"
            "<p> - Click pause button to stop the simulation of the game. </p>"
            "<p> - Click clear button for clear the grid (all cell are dead). </p>"
            "<p><b>SETTINGS :</b></p>"
            "<p> - Move speed slider for set the speed of the simulation. </p>"
            "<p> - Change the size of grid by selecting it in the combo box. </p>",
        )

    def _updateView(self):
        """
        Update the buttons, the speed label and the step label if the simulation is running
        """
        print("Update View")
        self.speedLabel.setText(f"Fps : {self._model.getFps()} ")
        self.stepLabel.setText(f"Step : {self._model.getStep()} ")
        if self._model.isRunning():
            self.playButton.setDisabled(True)
            self.stepButton.setDisabled(True)
            self.pauseButton.setDisabled(False)
            self.speedSlider.setDisabled(True)
        else:
            self.playButton.setDisabled(False)
            self.stepButton.setDisabled(False)
            self.pauseButton.setDisabled(True)
            self.speedSlider.setDisabled(False)

    def buttonPlay(self, slot):
        """
        Slot of button play
        """
        self.playButton.clicked.connect(slot)

    def buttonStep(self, slot):
        """
        Slot of button single step
        """
        self.stepButton.clicked.connect(slot)

    def buttonPause(self, slot):
        """
        Slot of button pause
        """
        self.pauseButton.clicked.connect(slot)

    def buttonClear(self, slot):
        """
        Slot of button reset
        """
        self.clearButton.clicked.connect(slot)

    def sliderSpeed(self, slot):
        """
        Slot of slider speed
        """
        self.speedSlider.valueChanged.connect(slot)

    def comboSizeGridText(self, slot):
        """
        Slot of grid size comboBox
        """
        self.gridComboBox.currentTextChanged.connect(slot)







