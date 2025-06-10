# -*- coding: utf-8 -*-
"""
engine module

This module provides functionality for manipulation of 3D coordinates.
It incluedes a projection function and functions for handling yaw, pitch
and roll rotations

Functions:
- transform_coord: Converts a 3D coordinate into a 2D coordinate
- rotation: Decorator which automatically handles angle to sin and cos conversion
- rotate_x: Performs a yaw rotation on the given coordinate
- rotate_y: Performs a pitch rotation on the given coordinate
- rotate_z: Performs a roll rotation on the given coordinate
"""


import math

from typing import List
from typing import Tuple
from typing import Callable


class TransformationError(Exception):
    """Raised when theres an error related to transforming coordinates"""


def transform_coord(
    vert: List[float | int],
    scale_factor: int = 25,
) -> List[float]:
    """Converts a 3D coordinate into a 2D coordinate

    Uses weak perspective projection to convert a 3D coordinate
    into its 2D representation (assumes the distance between the
    camera has already been accounted for)

    Args:
        vert (List[float | int]): the 3D coordinate that is being transformed
            into its 2D representation
        scale_factor (int): how much the coordinate will be scaled, defaults to 25

    Returns:
        List[float]: the 2D representation of the given 3D coordinate

    Raises:
        TransformationError if the z coord is less than or equal to zero
    """

    x, y, z = vert

    if z <= 0:
        raise TransformationError(
            "cannot transform a coordinate thats behind the camera"
        )

    transformed_x = (x / z * 15) * scale_factor
    transformed_y = (y / z * 15) * scale_factor

    return [transformed_x, transformed_y]


def rotation(func: Callable) -> Callable:
    """Decorator which automatically handles angle to sin and cos conversion

    This decorator automatically converts the angle to its sin and cos representation
    and passes those two values into the wrapped rotation function

    Args:
        func (Callable): the original rotation function

    Returns:
        Callable: the function with the passed in cos and sin values
    """

    def wrapper(
        vert: List[float | int],
        center: List[float | int],
        angle: float | int,
    ) -> Callable:
        """Calculates the sin and cos and forwards them to the function

        Args:
            vert (List[float | int]): the 3D coordinate (x, y, z) that will be rotated
            center (List[float | int]): the point at which the specified coordinate
                will be rotated around
            angle (float | int): the angle used in the rotation

        Returns:
            Callable: the rotated coordinate
        """

        sin = math.sin(math.radians(angle))
        cos = math.cos(math.radians(angle))

        return func(vert, center, cos, sin)

    return wrapper


@rotation
def rotate_x(
    vert: List[float | int],
    center: List[float | int],
    cos: float | int = 0,
    sin: float | int = 0,
) -> Tuple[float | int, float | int, float | int]:
    """Performs a yaw rotation on the given coordinate

    Rotates the given coordinate around the point
    center by the specified angle (x axis)

    Args:
        vert (List[float | int]): the 3D coordinate (x, y, z) that will be rotated
        center (List[float | int]): the point at which the specified coordinate
            will be rotated around
        cos (float | int): the cosine of the angle used for rotation, defaults to 0
        sin (float | int): the sine of the angle used for rotation, defaults to 0

    Returns:
        Tuple[float | int, float | int, float | int]: the rotated coordinate
    """

    x = vert[0] - center[0]
    z = vert[2] - center[2]

    rotated_x = x * cos - z * sin + center[0]
    rotated_y = vert[1]
    rotated_z = z * cos + x * sin + center[2]

    return rotated_x, rotated_y, rotated_z


@rotation
def rotate_y(
    vert: List[float | int],
    center: List[float | int],
    cos: float | int = 0,
    sin: float | int = 0,
) -> Tuple[float | int, float | int, float | int]:
    """Performs a pitch rotation on the given coordinate

    Rotates the given coordinate around the point
    center by the specified angle (y axis)

    Args:
        vert (List[float | int]): the 3D coordinate (x, y, z) that will be rotated
        center (List[float | int]): the point at which the specified coordinate
            will be rotated around
        cos (float | int): the cosine of the angle used for rotation, defaults to 0
        sin (float | int): the sine of the angle used for rotation, defaults to 0

    Returns:
        Tuple[float | int, float | int, float | int]: the rotated coordinate
    """

    y = vert[1] - center[1]
    z = vert[2] - center[2]

    rotated_x = vert[0]
    rotated_y = y * cos - z * sin + center[1]
    rotated_z = z * cos + y * sin + center[2]

    return rotated_x, rotated_y, rotated_z


@rotation
def rotate_z(
    vert: List[float | int],
    center: List[float | int],
    cos: float | int = 0,
    sin: float | int = 0,
) -> Tuple[float | int, float | int, float | int]:
    """Performs a roll rotation on the given coordinate

    Rotates the given coordinate around the point
    center by the specified angle (z axis)

    Args:
        vert (List[float | int]): the 3D coordinate (x, y, z) that will be rotated
        center (List[float | int]): the point at which the specified coordinate
            will be rotated around
        cos (float | int): the cosine of the angle used for rotation, defaults to 0
        sin (float | int): the sine of the angle used for rotation, defaults to 0

    Returns:
        Tuple[float | int, float | int, float | int]: the rotated coordinate
    """

    x = vert[0] - center[0]
    y = vert[1] - center[1]

    rotated_x = x * cos - y * sin + center[0]
    rotated_y = y * cos + x * sin + center[1]

    return rotated_x, rotated_y, vert[2]
