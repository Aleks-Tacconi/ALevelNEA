# -*- coding: utf-8 -*-
"""
rubix_cube module

This module handles the interaction between the 3D objects
that make up the rubix cube and the 2D representation of the 
rubix cube

Classes:
- RubixCube
"""

import time
import threading
import tkinter as tk

from typing import List
from typing import Callable

import keyboard

from rubix_cube.rubix_2d import Rubix2D
from rubix_cube.rubix_2d import rotate_side

from rubix_cube.rubix_solver import breath_first_search

from graphics.cube import Cube
from graphics.cube import filter_cubes

from graphics.shape import Shape
from graphics.shape import rotate_shapes

from graphics.engine import rotate_x
from graphics.engine import rotate_y
from graphics.engine import rotate_z


class RubixCube:
    """Class that combines the manipulation of the 3D objects that
    make up the rubix cube, with the 2D representation of the cube
    """

    def __init__(
        self,
        cubes: List[Cube],
        shapes: List[Shape],
        rubix_2d: Rubix2D,
    ) -> None:
        """Constructor for the rubix cube class

        Args:
            cubes: (List[Cube]): List of cubes which make up the rubix cube
            shapes: (List[Shape]): List of shapes which make up the cubes
                that make up the rubix cube
            rubix_2d (Rubix2D): object representing a 2D rubix cube

        Returns:
            None
        """

        self.cubes = cubes
        self.shapes = shapes
        self.rubix_2d = rubix_2d

        self.rotating = False
        self.solving = False

        self.commands = []

    def rotate_cubes(
        self, axis: int, filter_: int, rotate: Callable, angle: int = 1
    ) -> None:
        """Rotates a side of the 3D rubix cube

        This function slowly rotates a side of the rubix cube, this should be run
        in a seperate thread so that the gui can be updated whilst the side is rotating
        which results in a nice animation

        Args:
            axis (int): the axis thats being considered when filtering the cubes
            filter_ (int): the expected location of the cube on the given axis
            rotate (Callable): the function used for the rotation of the cube
                this will either be rotate_x, rotate_y or rotate_z
            angle (int): the angle of rotation, either 1 or -1, defaults to 1

        Returns:
            None
        """

        cubes = list(filter(lambda cube: filter_cubes(cube, axis, filter_), self.cubes))

        for _ in range(90):
            for cube in cubes:
                for shape in cube.cube:
                    shape.poly = [rotate(vert, [0, 0, 0], angle) for vert in shape.poly]

            time.sleep(0.01)

        self.rotating = False

    def bfs(self) -> None:
        """Uses a breath-first-search to solve the cube

        This runs a breath-first-search in an attempt to find the solution
        to the rubix cube, this should be run in a seperate thread whilst
        constantly updating the tkinter window so that it dosent crash

        Returns:
            None
        """

        self.commands = breath_first_search(
            self.rubix_2d.top,
            self.rubix_2d.front,
            self.rubix_2d.left,
            self.rubix_2d.right,
            self.rubix_2d.back,
            self.rubix_2d.bottom,
        )
        self.commands.reverse()

        self.solving = False

    def solve(self, canvas: tk.Canvas) -> None:
        """Solves the rubix cube

        Starts the solving of the rubix cube in a separate thread whilst
        updating the specified canvas (so it dosent crash) in the main thread

        Args:
            canvas (tk.Canvas): the tkinter canvas

        Returns:
            None
        """

        self.solving = True

        threading.Thread(target=self.bfs).start()

    def mainloop(self, canvas: tk.Canvas) -> None:
        """Captures keystrockes and rotates shapes accordingly

        Captures the users keyboard inputs and rotates the shapes
        based on what the user has pressed

        Args:
            canvas (tk.Canvas): the tkinter canvas

        Returns:
            None
        """

        if keyboard.is_pressed("w"):
            rotate_shapes(self.shapes, 0, -1)
        if keyboard.is_pressed("a"):
            rotate_shapes(self.shapes, -1, 0)
        if keyboard.is_pressed("s"):
            rotate_shapes(self.shapes, 0, 1)
        if keyboard.is_pressed("d"):
            rotate_shapes(self.shapes, 1, 0)

        if self.rotating or self.solving:
            return None

        if keyboard.is_pressed("x") and not self.commands:
            self.solve(canvas)

        command = self.commands.pop() if self.commands else -1

        thread = None

        # fmt: off
        if (keyboard.is_pressed("1") and command == -1) or command == 1:
            thread = threading.Thread(target=self.rotate_cubes, args=(1, 1, rotate_x))
            rotate_side(1, self.rubix_2d)
        if (keyboard.is_pressed("2") and command == -1) or command == 2:
            thread = threading.Thread(target=self.rotate_cubes, args=(1, 0, rotate_x))
            rotate_side(2, self.rubix_2d)
        if (keyboard.is_pressed("3") and command == -1) or command == 3:
            thread = threading.Thread(target=self.rotate_cubes, args=(1, -1, rotate_x))
            rotate_side(3, self.rubix_2d)

        if (keyboard.is_pressed("4") and command == -1) or command == 4:
            thread = threading.Thread(target=self.rotate_cubes, args=(0, -1, rotate_y))
            rotate_side(4, self.rubix_2d)
        if (keyboard.is_pressed("5") and command == -1) or command == 5:
            thread = threading.Thread(target=self.rotate_cubes, args=(0, 0, rotate_y))
            rotate_side(5, self.rubix_2d)
        if (keyboard.is_pressed("6") and command == -1) or command == 6:
            thread = threading.Thread(target=self.rotate_cubes, args=(0, 1, rotate_y))
            rotate_side(6, self.rubix_2d)

        if (keyboard.is_pressed("7") and command == -1) or command == 7:
            thread = threading.Thread(target=self.rotate_cubes, args=(2, 1, rotate_z))
            rotate_side(7, self.rubix_2d)
        if (keyboard.is_pressed("8") and command == -1) or command == 8:
            thread = threading.Thread(target=self.rotate_cubes, args=(2, 0, rotate_z))
            rotate_side(8, self.rubix_2d)
        if (keyboard.is_pressed("9") and command == -1) or command == 9:
            thread = threading.Thread(target=self.rotate_cubes, args=(2, -1, rotate_z))
            rotate_side(9, self.rubix_2d)

        if (keyboard.is_pressed("i") and command == -1) or command == 10:
            thread = threading.Thread(target=self.rotate_cubes, args=(1, 1, rotate_x, -1))
            rotate_side(10, self.rubix_2d)
        if (keyboard.is_pressed("o") and command == -1) or command == 11:
            thread = threading.Thread(target=self.rotate_cubes, args=(1, 0, rotate_x, -1))
            rotate_side(11, self.rubix_2d)
        if (keyboard.is_pressed("p") and command == -1) or command == 12:
            thread = threading.Thread(target=self.rotate_cubes, args=(1, -1, rotate_x, -1))
            rotate_side(12, self.rubix_2d)

        if (keyboard.is_pressed("j") and command == -1) or command == 13:
            thread = threading.Thread(target=self.rotate_cubes, args=(0, -1, rotate_y, -1))
            rotate_side(13, self.rubix_2d)
        if (keyboard.is_pressed("k") and command == -1) or command == 14:
            thread = threading.Thread(target=self.rotate_cubes, args=(0, 0, rotate_y, -1))
            rotate_side(14, self.rubix_2d)
        if (keyboard.is_pressed("l") and command == -1) or command == 15:
            thread = threading.Thread(target=self.rotate_cubes, args=(0, 1, rotate_y, -1))
            rotate_side(15, self.rubix_2d)

        if (keyboard.is_pressed("b") and command == -1) or command == 16:
            thread = threading.Thread(target=self.rotate_cubes, args=(2, 1, rotate_z, -1))
            rotate_side(16, self.rubix_2d)
        if (keyboard.is_pressed("n") and command == -1) or command == 17:
            thread = threading.Thread(target=self.rotate_cubes, args=(2, 0, rotate_z, -1))
            rotate_side(17, self.rubix_2d)
        if (keyboard.is_pressed("m") and command == -1) or command == 18:
            thread = threading.Thread(target=self.rotate_cubes, args=(2, -1, rotate_z, -1))
            rotate_side(18, self.rubix_2d)
        # fmt: on

        if thread is not None:
            self.rotating = True
            thread.start()
