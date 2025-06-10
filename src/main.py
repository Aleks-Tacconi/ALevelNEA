# -*- coding: utf-8 -*-
"""
main module

This module acts as an entry point for the application and 
handles all the logic between the interaction of modules

Functions:
- main: the entry point for the application
"""

from gui import GUI

from graphics import render_shape
from graphics import get_sorted_shapes
from graphics import Cube
from graphics import ALL_SHAPES
from graphics import ALL_CUBES

from rubix_cube import RubixCube
from rubix_cube import Rubix2D

CAMERA_POS = [0, 0, -7]


def main() -> None:
    """Handles the logic behind the application

    This function is the entry point of the application and
    is responsible for handling all the logic between the interation
    of the modules

    Returns:
        None
    """
    # creates the 3D representation of the rubix cube
    Cube(0, 0, 0, ["black", "black", "black", "black", "black", "black"])
    Cube(0, 0, 1, ["black", "orange", "black", "black", "black", "black"])
    Cube(0, 0, -1, ["red", "black", "black", "black", "black", "black"])
    Cube(1, 0, 0, ["black", "black", "black", "blue", "black", "black"])
    Cube(1, 0, 1, ["black", "orange", "black", "blue", "black", "black"])
    Cube(1, 0, -1, ["red", "black", "black", "blue", "black", "black"])
    Cube(-1, 0, 0, ["black", "black", "black", "black", "black", "green"])
    Cube(-1, 0, 1, ["black", "orange", "black", "black", "black", "green"])
    Cube(-1, 0, -1, ["red", "black", "black", "black", "black", "green"])
    Cube(0, 1, 0, ["black", "black", "black", "black", "white", "black"])
    Cube(1, 1, 0, ["black", "black", "black", "blue", "white", "black"])
    Cube(1, 1, -1, ["red", "black", "black", "blue", "white", "black"])
    Cube(1, 1, 1, ["black", "orange", "black", "blue", "white", "black"])
    Cube(0, 1, -1, ["red", "black", "black", "black", "white", "black"])
    Cube(-1, 1, -1, ["red", "black", "black", "black", "white", "green"])
    Cube(0, 1, 1, ["black", "orange", "black", "black", "white", "black"])
    Cube(-1, 1, 1, ["black", "orange", "black", "black", "white", "green"])
    Cube(-1, 1, 0, ["black", "black", "black", "black", "white", "green"])
    Cube(1, -1, 0, ["black", "black", "yellow", "blue", "black", "black"])
    Cube(1, -1, 1, ["black", "orange", "yellow", "blue", "black", "black"])
    Cube(1, -1, -1, ["red", "black", "yellow", "blue", "black", "black"])
    Cube(-1, -1, 0, ["black", "black", "yellow", "black", "black", "green"])
    Cube(-1, -1, 1, ["black", "orange", "yellow", "black", "black", "green"])
    Cube(-1, -1, -1, ["red", "black", "yellow", "black", "black", "green"])
    Cube(0, -1, 0, ["black", "black", "yellow", "black", "black", "black"])
    Cube(0, -1, 1, ["black", "orange", "yellow", "black", "black", "black"])
    Cube(0, -1, -1, ["red", "black", "yellow", "black", "black", "black"])

    # creates the gui
    gui = GUI(title="RubixCubeNEA")
    rubix_2d = Rubix2D()
    rubix_cube = RubixCube(ALL_CUBES, ALL_SHAPES, rubix_2d)

    while True:
        gui.canvas.delete("all")

        # draws all cubes on the canvas
        for face in get_sorted_shapes(ALL_SHAPES, CAMERA_POS):
            render_shape(gui.canvas, face, CAMERA_POS)

        rubix_cube.mainloop(gui.canvas)

        # renders a new frame (updates window)
        gui.update()
        gui.update_idletasks()


if __name__ == "__main__":
    main()
