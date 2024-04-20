###########
# IMPORTS #
###########

import math
import random
from typing import List, Tuple
from plane import Plane, Obstacle
from walker import Walker

AMOUNT_OF_WEIGHTS = 5
AMOUNT_OF_OBSTACLE_COORDINATES = 4
AMOUNT_OF_PORTAL_COORDINATES = 6
UP = (0, 1)
DOWN = (0, -1)
RIGHT = (1, 0)
LEFT = (-1, 0)
X_COORDINATE = 0
Y_COORDINATE = 1


def has_possible_moves(walker: Walker, plane: Plane) -> bool:
    """
    Checks if the walker has any possible moves on the plane.

    Parameters
    ----------
    walker : Walker
        The walker whose possible moves are to be checked.
    plane : Plane
        The plane on which the walker is moving.

    Returns
    -------
    bool
        True if the walker has at least one possible move, False otherwise.

    Notes
    -----
    For DISCRETE_WALKER and UNEVEN_DISTRIBUTION_WALKER, the possible moves are UP, DOWN, RIGHT, LEFT, and the opposite of the current position.
    For NORMAL_WALKER and UNEVEN_STEP_WALKER, a number of random directions are checked.
    A move is considered possible if the new position does not intersect with an obstacle.
    """
    # Define the possible moves for DISCRETE_WALKER and UNEVEN_DISTRIBUTION_WALKER
    possible_moves = [UP, DOWN, RIGHT, LEFT,
                      (-walker.get_position()[X_COORDINATE], -walker.get_position()[Y_COORDINATE])]

    # Get the current position of the walker
    current_position = walker.get_position()

    # Check each possible move
    for move in possible_moves:
        # Calculate the new position
        new_position = (current_position[X_COORDINATE] + move[X_COORDINATE], current_position[Y_COORDINATE] + move[Y_COORDINATE])

        # Check if the new position is a valid move
        intersection = plane.check_intersection(current_position, new_position)
        if not isinstance(intersection, tuple) or not isinstance(intersection[1], Obstacle):
            return True

    # For NORMAL_WALKER and UNEVEN_STEP_WALKER, check a number of random directions
    if walker.get_walker_type() in [1, 2]:
        for _ in range(100):  # A large number of random directions to check
            angle = random.uniform(0, 2*math.pi)
            dx = math.cos(angle)
            dy = math.sin(angle)
            new_position = (current_position[0] + dx, current_position[1] + dy)
            intersection = plane.check_intersection(current_position, new_position)
            if not isinstance(intersection, tuple) or not isinstance(intersection[1], Obstacle):
                return True

    # If no valid moves were found, return False
    return False


def parse_portal_coordinates(coord_str: str) -> List[Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]]:
    """
    Parse a string of coordinates in the format "x1,y1,x2,y2,x3,y3" for portals.
    :param coord_str: The string of coordinates.
    :return: A list of tuples, each containing three tuples representing a portal's start, end, and destination.
    """
    coords = list(map(float, coord_str.split(',')))
    if len(coords) % AMOUNT_OF_PORTAL_COORDINATES != 0:
        raise ValueError("Portal coordinates must be in the format 'x1,y1,x2,y2,x3,y3'")
    return [((coords[i], coords[i+1]), (coords[i+2], coords[i+3]), (coords[i+4], coords[i+5])) for i in range(0, len(coords), AMOUNT_OF_PORTAL_COORDINATES)]


def parse_obstacle_coordinates(coord_str: str) -> List[Tuple[Tuple[float, float], Tuple[float, float]]]:
    """
    Parse a string of coordinates in the format "x1,y1,x2,y2" for obstacles.
    :param coord_str: The string of coordinates.
    :return: A list of tuples, each containing two tuples representing an obstacle's start and end.
    """
    coords = list(map(float, coord_str.split(',')))
    if len(coords) % AMOUNT_OF_OBSTACLE_COORDINATES != 0:
        raise ValueError("Obstacle coordinates must be in the format 'x1,y1,x2,y2'")
    return [((coords[i], coords[i+1]), (coords[i+2], coords[i+3])) for i in range(0, len(coords), AMOUNT_OF_OBSTACLE_COORDINATES)]


def parse_weights(weight_str: str) -> tuple[int, ...]:
    """
    Parse a string of weights in the format "w1,w2,w3,w4,w5" for type 4 walker.
    :param weight_str: The string of weights.
    :return: A tuple of integers representing the weights.
    """
    weights = list(map(int, weight_str.split(',')))
    if len(weights) != AMOUNT_OF_WEIGHTS:
        raise ValueError("Weights must be in the format 'w1,w2,w3,w4,w5'")
    return tuple(weights)

