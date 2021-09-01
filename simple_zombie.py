# Code to make a spot wander about:
import numpy as np
import matplotlib.pyplot as plt
import random
import os
from math import sin, cos, pi, sqrt


def plot_points(x, y, zombie_status, filename):
    fig = plt.figure(figsize=(8, 8), dpi=200)
    ax = fig.add_subplot(111)
    S = 10
    n_creatures = len(zombie_status)
    zombie_x = [x[i] for i in range(n_creatures) if zombie_status[i]]
    zombie_y = [y[i] for i in range(n_creatures) if zombie_status[i]]
    human_x = [x[i] for i in range(n_creatures) if not zombie_status[i]]
    human_y = [y[i] for i in range(n_creatures) if not zombie_status[i]]
    ax.scatter(zombie_x, zombie_y, c="red", s=S, marker="o")
    ax.scatter(human_x, human_y, c="blue", s=S, marker="o")
    plt.title("Zombie Spread")
    plt.tight_layout(pad=0)
    plt.savefig(filename, dpi=100)


def main():
    # create result directory if it does not exist
    result_directory = "zombie_movie_frames"
    if not os.path.isdir(result_directory):
        os.mkdir(result_directory)

    # set up parameters for simulation
    n_creatures = 100
    velocity = 5
    step_n = 1000
    distance_threshold = 25.0
    grid_size = 512

    # initialise x, y, and zombie_status
    x = []
    y = []
    zombie_status = []
    for i in range(n_creatures):
        x.append(random.uniform(0, grid_size))
        y.append(random.uniform(0, grid_size))
        zombie_status.append(False)

    # initial single infection
    zombie_status[0] = True

    # time step loop
    for step in range(step_n):
        print(f"working on step {step}")
        # update positions
        for i in range(n_creatures):
            direction = random.uniform(0, 2 * pi)
            x[i] += velocity * cos(direction)
            y[i] += velocity * sin(direction)
        # check pairs of creatures for infection potential
        # note this double loop i,j is a computational bottle neck - find a better way
        for i in range(0, n_creatures - 1):
            for j in range(i + 1, n_creatures):
                # do creatures have different statuses ? (we can ignore otherwise)
                if zombie_status[i] ^ zombie_status[j]:
                    # compute distance between creatures - Pythagoras
                    dist = sqrt((x[i] - x[j]) ** 2.0 + (y[i] - y[j]) ** 2.0)
                    # distance below infection threshold ?
                    if dist < distance_threshold:
                        zombie_status[i] = True  # one of these is redundant but OK
                        zombie_status[j] = True
        frame_number = str(step).zfill(6)
        filename = f"zombie_spread_2d_{frame_number}.png"
        full_path = os.path.join(result_directory, filename)
        plot_points(x, y, zombie_status, full_path)


if __name__ == "__main__":
    main()
