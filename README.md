# Conway's Game of Life

## Overview

The *Game of Life*, also known simply as *Life*, is a cellular automaton devised by the British mathematician John Horton Conway in 1970. 

It is a zero-player game, meaning that its evolution is determined by its initial state, requiring no further input. 
One interacts with the Game of Life by creating an initial configuration and observing how it evolves. 

For more information this is the [original article](http://ddi.cs.uni-potsdam.de/HyFISCH/Produzieren/lis_projekt/proj_gamelife/ConwayScientificAmerican.htm) of Game of Life with the relative [online community](https://www.conwaylife.com/). 

## Rules

 At each time step, the new board is computed from the previous one depending on the following rules:
 
Each grid location is either empty (cell dead) or populated (cell alive) by a single cell.
The concept of neighbor is very important. 
The eight grid locations surrounding a cell are considered neighbors of it.

At each time step, the new board is computed from the previous one depending on the following rules:

  1. Each populated location with one or zero neighbors dies (from loneliness).
  2. Each populated location with four or more neighbors dies (from overpopulation).
  3. Each populated location with two or three neighbors survives.
  4. Each unpopulated location that becomes populated if it has exactly three populated neighbors.

img (img/rules.png)

# About this implementation
This repository is a implementation of the *Game of Life* made in Python.
The implementation respects the Model-View-Controller pattern.

### Requirements
The project is developed with PyCharm and here is an interesting [guide](https://pythonpyqt.com/how-to-install-pyqt5-in-pycharm/) for integrate QTdesigner and PyUIC in the ide.

The following version of libraries are used:

| Software   | Version           |
| -----------|-------------------|
| **Python** | tested on v3.8    | 
| **PyQT5**  | tested on v5.15.6 |
| **Numpy**  | tested on v1.21.2 |

## Graphical User Interface
![Graphical User Interface of this implementation of Game of Life](img/simulazione-1.png "Graphical User Interface")

## Features
This implementation of Game of Life have the following features:
* A menu bar with load/save function for board and a guide to play.
* Load initial state from configurations encoded in Run Length Encoding (RLE)
* Editing of state on the board with the left click of the mouse. If users click on the board set to alive/death a single cell.
* Controls buttons: start and pause the simulation, do a single step, clear the board.
* A slider that allow to set the speed of the simulation when is not running.
* A label that shows the age of the simulation through the number of steps performed.
* A combo box that allow the user to change the grid size.
* The color of the cells changes according to how long it has been occupied, from light blue (newborn) to bright red (ancient).

### Usage
After installation of requirements [download](https://github.com/AntonioAcunzo/GameOfLife.git) the project and run it in a terminal.

```sh
$ cd GameOfLife
$ python gameLauncher.py
```

You can find RLE-encoded configurations at: https://www.conwaylife.com/wiki/Main_Page

