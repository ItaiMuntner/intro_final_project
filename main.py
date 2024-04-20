#######################
# Author: Itai Muntner
# ID: 211491634
# Login: itai_muntner
#######################

###########
# IMPORTS #
###########

import os
from typing import List, Tuple, Dict
import matplotlib.pyplot as plt
import argparse
from simulation import run_simulation
from utils import parse_portal_coordinates, parse_obstacle_coordinates, parse_weights

ACCEPTABLE_WALKER_TYPES = {1, 2, 3, 4}
GRAPH_SIZE = (10, 6)
STATS = ['Avg Distance from x-axis', 'Avg Distance from y-axis', 'Avg Distance from Origin']


def plot_graph(multi_simulation_stats: List[Tuple[int, Dict[str, float], List[Tuple[int, Dict[str, float]]]]],
               folder, export_graphs):
    """
    Function to plot the graphs based on the simulation statistics.

    Parameters:
    multi_simulation_stats (List[Tuple[int, Dict[str, float],
     List[Tuple[int, Dict[str, float]]]]]): List of simulation statistics.
    folder (str): The folder where the graphs will be saved if export_graphs is True.
    export_graphs (bool): If True, the graphs will be saved in the specified folder.
     If False, the graphs will be displayed.

    Returns:
    None
    """

    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Initialize total_stats as a list of dictionaries
    total_stats = [{'Avg Distance from x-axis': 0, 'Avg Distance from y-axis': 0, 'Avg Distance from Origin': 0} for _
                   in range(len(multi_simulation_stats[0][2]))]

    # Loop over each simulation
    for _, _, simulation_stats in multi_simulation_stats:
        # Loop over each step in simulation_stats
        for i, stats in simulation_stats:
            # Loop over each statistic in stats and add the statistic value
            # to the corresponding statistic in total_stats
            for stat_name in stats:
                total_stats[i-1][stat_name] += stats[stat_name]

    # Calculate the average statistics.
    avg_stats = [{stat_name: stat_dict[stat_name] / len(multi_simulation_stats) for stat_name in stat_dict}
                 for stat_dict in total_stats]

    # Plot each statistic separately
    for i, stat_name in enumerate(STATS):
        plot_simulation_graphs(stat_name, avg_stats)
        if export_graphs:
            # Save the graph to a file
            plt.savefig(os.path.join(folder, f'graph{i+1}.png'))
        else:
            plt.show()

    if len(multi_simulation_stats) > 1:

        # Plot the graph for average number of steps to get out of the 10-unit radius
        plot_exiting_10_unit_radius_graph(multi_simulation_stats)
        if export_graphs:
            plt.savefig(os.path.join(folder, 'graph5.png'))
        else:
            plt.show()

        # Plot the graph for average number the y-axis was crossed/touched
        plot_y_axis_crossings_graph(multi_simulation_stats)
        if export_graphs:
            plt.savefig(os.path.join(folder, 'graph6.png'))
        else:
            plt.show()


def plot_simulation_graphs(stat_name: str, avg_stats: List[Dict[str, float]]) -> None:
    """
    Function to plot the graph for a specific statistic.
    :param stat_name: stat to plot.
    :param avg_stats: list of statistics.
    :return: None.
    """
    plt.figure(figsize=GRAPH_SIZE)
    plt.plot([i for i, _ in enumerate(avg_stats)], [stat[stat_name] for stat in avg_stats],
             marker='o', label=stat_name)
    plt.title(f'{stat_name} vs Number of Steps')
    plt.xlabel('Number of Steps')
    plt.ylabel(stat_name)
    plt.legend()


def plot_exiting_10_unit_radius_graph(
        multi_simulation_stats: List[Tuple[int, Dict[str, float], List[Tuple[int, Dict[str, float]]]]]) -> None:
    """
    Function to plot the graph for the average number of steps to get out of the 10-unit radius.

    Parameters:
    multi_simulation_stats (List[Tuple[int, Dict[str, float],
     List[Tuple[int, Dict[str, float]]]]]): List of simulation statistics.

    Returns:
    None
    """

    plt.figure(figsize=GRAPH_SIZE)
    plt.plot([i for i, _, _ in multi_simulation_stats],
             [stat['Number of steps to exit 10-unit radius'] for _, stat, _ in multi_simulation_stats],
             marker='o', label='Steps Outside Radius')
    plt.title('Steps Outside Radius vs Number of Simulations')
    plt.xlabel('Number of Simulations')
    plt.ylabel('Steps Outside Radius')
    plt.legend()
    plt.show()


def plot_y_axis_crossings_graph(multi_simulation_stats:
                                List[Tuple[int, Dict[str, float], List[Tuple[int, Dict[str, float]]]]]) -> None:
    """
    Function to plot the graph for the average number of times the y-axis was crossed/touched.
    :param multi_simulation_stats: 
    :return: 
    """
    plt.figure(figsize=GRAPH_SIZE)
    plt.plot([i for i, _, _ in multi_simulation_stats],
             [stat['Number of times crossed y-axis'] for _, stat, _ in multi_simulation_stats],
             marker='o', label='Y-Axis Crosses')
    plt.title('Y-Axis Crosses vs Number of Simulations')
    plt.xlabel('Number of Simulations')
    plt.ylabel('Y-Axis Crosses')
    plt.legend()


def parser_args():
    """
    Function to parse the command line arguments.
    Returns: argparse.Namespace
    """

    parser = argparse.ArgumentParser(description='A simulation of a Random Walker.')

    parser.add_argument('walker_type', type=int, choices=ACCEPTABLE_WALKER_TYPES,
                        help='Type of the walker (integer between 1 and 4).')
    parser.add_argument('steps', type=int, help='Number of steps the walker will take.')
    parser.add_argument('simulations', type=int, help='Number of simulations to run.')
    parser.add_argument('n_steps', type=int,
                        help='Number of steps the distance statistics will be taken from.')
    parser.add_argument('--portals', type=parse_portal_coordinates,
                        help='Comma-separated list of portal coordinates in the format "x1,y1,x2,y2,x3,y3".')
    parser.add_argument('--obstacles', type=parse_obstacle_coordinates,
                        help='Comma-separated list of obstacle coordinates in the format "x1,y1,x2,y2".')
    parser.add_argument('--weights', type=parse_weights,
                        help='Comma-separated list of weights in the format "w1,w2,w3,w4,w5" for type 4 walker.')
    parser.add_argument('--export-graphs', action='store_true', help='Export the graphs to files.')
    return parser.parse_args()


def main() -> None:
    """
    Main function to run the simulation.
    Returns: None
    """

    # Parse the command line arguments
    args = parser_args()

    # Check if the number of steps to take statistics from is valid (between 1 and the total number of steps).
    if args.n_steps not in range(1, args.steps + 1):
        print(f"Invalid number of steps to take statistics from: {args.n_steps}")
        return

    multi_simulation_stats = run_simulation(args)
    plot_graph(multi_simulation_stats, './graphs', args.export_graphs)


if __name__ == "__main__":
    main()
