###########
# IMPORTS #
###########

import time
from typing import List, Tuple, Dict
from argparse import Namespace
from plane import Plane, Portal, Obstacle
from walker import Walker
from utils import has_possible_moves


def run_simulation(args: Namespace) -> List[Tuple[int, Dict[str, float], List[Tuple[int, Dict[str, float]]]]]:
    # Initialize an empty list to store the statistics
    multi_simulation_stats = []

    # Run the simulation

    total_distance_from_origin = 0
    total_exit_time = 0
    total_distance_from_x_axis = 0
    total_distance_from_y_axis = 0
    total_y_axis_cross_count = 0
    total_steps_to_exit = 0
    total_y_axis_crosses = 0
    total_unsuccessful_moves = 0

    plane = Plane()

    if args.portals:
        for start, end, destination in args.portals:
            plane.add_portal(Portal(start, end, destination))

    if args.obstacles:
        for start, end in args.obstacles:
            plane.add_obstacle(Obstacle(start, end))

    for i in range(args.simulations):

        simulation_stats = []
        simulation_distance_from_origin = 0
        simulation_enter_time = time.time()
        simulation_exit_time = None
        simulation_distance_from_x_axis = 0
        simulation_distance_from_y_axis = 0
        simulation_y_axis_cross_count = 0
        simulation_steps_to_exit = 0
        simulation_unsuccessful_moves = 0

        if args.walker_type == 4 and args.weights is not None:
            walker = Walker(args.walker_type, args.weights)
        else:
            walker = Walker(args.walker_type)

        plane.add_walker(walker)

        for step in range(args.steps):
            # Check if there are any possible moves
            if not has_possible_moves(walker, plane):
                break
            previous_position = walker.get_position()
            next_position = walker.get_next_move()
            intersection = plane.check_intersection(previous_position, next_position)
            if isinstance(intersection[1], (Portal, Obstacle)):
                # intersection[1] is a Portal or Obstacle instance
                if intersection[0] == 'portal':
                    walker.set_position(*intersection[1].get_destination())
                else:
                    # If the move was unsuccessful due to an obstacle, increment the unsuccessful_moves counter
                    simulation_unsuccessful_moves += 1
            else:
                # intersection[1] is a tuple of coordinates
                walker.move(*intersection)

            # Check if the walker's position has changed
            if walker.get_position() != previous_position:

                simulation_distance_from_origin += walker.get_distance()
                position = walker.get_position()
                simulation_distance_from_x_axis += abs(position[1])  # y-coordinate
                simulation_distance_from_y_axis += abs(position[0])  # x-coordinate

                if (previous_position[0] * position[0] < 0 or
                        (previous_position[0] * position[0] == 0 and
                         previous_position[0] * walker.get_path()[-2][0] != 0)):  # crossed y-axis
                    simulation_y_axis_cross_count += 1

                if simulation_exit_time is None and walker.get_distance() > 10:
                    simulation_exit_time = time.time() - simulation_enter_time
                    simulation_steps_to_exit = walker.get_steps()

                if args.n_steps == step + 1:
                    total_distance_from_origin += simulation_distance_from_origin
                    total_distance_from_x_axis += simulation_distance_from_x_axis
                    total_distance_from_y_axis += simulation_distance_from_y_axis

            avg_distance_from_x_axis = simulation_distance_from_x_axis / (step + 1)
            avg_distance_from_y_axis = simulation_distance_from_y_axis / (step + 1)
            avg_distance_from_origin = simulation_distance_from_origin / (step + 1)

            simulation_stats.append(((step + 1), {
                'Avg Distance from x-axis': avg_distance_from_x_axis,
                'Avg Distance from y-axis': avg_distance_from_y_axis,
                'Avg Distance from Origin': avg_distance_from_origin
            }))

        total_exit_time += simulation_exit_time or 0
        total_steps_to_exit += simulation_steps_to_exit
        total_y_axis_crosses += simulation_y_axis_cross_count
        total_unsuccessful_moves += simulation_unsuccessful_moves
        multi_simulation_stats.append(((i+1), {'Number of steps to exit 10-unit radius': simulation_steps_to_exit,
                                               'Time to exit 10-unit radius': simulation_exit_time,
                                               'Number of times crossed y-axis': simulation_y_axis_cross_count,
                                               'Avg distance from origin after N steps':
                                                   total_distance_from_origin / (i + 1),
                                               'Avg distance from x-axis after N steps':
                                                   total_distance_from_x_axis / (i + 1),
                                               'Avg distance from y-axis after N steps':
                                                   total_distance_from_y_axis / (i + 1),
                                               'Number of unsuccessful moves due to obstacles':
                                                   total_unsuccessful_moves},
                                       simulation_stats))
        plane.remove_walker(walker)

    print(f"Average distance from origin: {total_distance_from_origin / (args.steps * args.simulations)}")
    print(f"Average distance from x-axis: {total_distance_from_x_axis / (args.steps * args.simulations)}")
    print(f"Average distance from y-axis: {total_distance_from_y_axis / (args.steps * args.simulations)}")
    if plane.get_obstacles() is not None:
        print(f"Average number of unsuccessful moves due to obstacles: {total_unsuccessful_moves / args.simulations}")
    if args.simulations > 1:
        print(f"Average number of steps to exit 10-unit radius: {total_steps_to_exit / args.simulations}")
        print(f"Average time to exit 10-unit radius: {total_exit_time / args.simulations}")
        print(f"Average number of times crossed y-axis: {total_y_axis_crosses / args.simulations}")

    return multi_simulation_stats
