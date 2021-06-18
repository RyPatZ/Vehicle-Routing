import utility as utility
import loader as loader
import numpy as np


def main():
    # Paths to the data and solution files.
    vrp_file =  "vrp-data/n80-k10.vrp"
    sol_file =  "vrp-data/n80-k10.sol"

    vrp_file="vrp-data/n32-k5.vrp"
    sol_file="vrp-data/n32-k5.sol"

    # Loading the VRP data file.
    px, py, demand, capacity, depot = loader.load_data(vrp_file)

    # Displaying to console the distance and visualizing the optimal VRP solution.
    vrp_best_sol = loader.load_solution(sol_file)
    best_distance = utility.calculate_total_distance(vrp_best_sol, px, py, depot)
    print("Best VRP Distance:", best_distance)
    utility.visualise_solution(vrp_best_sol, px, py, depot, "Optimal Solution")

    # Executing and visualizing the nearest neighbour VRP heuristic.
    # Uncomment it to do your assignment!

    nnh_solution = nearest_neighbour_heuristic(px, py, demand, capacity, depot)
    nnh_distance = utility.calculate_total_distance(nnh_solution, px, py, depot)
    print("Nearest Neighbour VRP Heuristic Distance:", nnh_distance)
    utility.visualise_solution(nnh_solution, px, py, depot, "Nearest Neighbour Heuristic")

    # Executing and visualizing the saving VRP heuristic.
    # Uncomment it to do your assignment!

    sh_solution = savings_heuristic(px, py, demand, capacity, depot)
    sh_distance = utility.calculate_total_distance(sh_solution, px, py, depot)
    print("Saving VRP Heuristic Distance:", sh_distance)
    utility.visualise_solution(sh_solution, px, py, depot, "Savings Heuristic")


def nearest_neighbour_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for the nearest neighbour heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """

    # TODO - Implement the Nearest Neighbour Heuristic to generate VRP solutions.
    routes = []
    current_node = depot;
    index = np.arange(len(px))
    ids = [];
    for i in range(len(index)):
        ids.append(i)
    a = [];
    ids.remove(0)
    while len(ids)>0:
        no=[]
        for x in range(len(ids)):
            distance = 9999;
            id = 999;
            for j in ids:
                if j != current_node and j!=depot and j not in no :
                    d = utility.calculate_euclidean_distance(px, py, current_node, j)
                    if d < distance :
                        distance = d
                        id = j
            total_demand = demand[id];
            for i in a:
                total_demand+=demand[i]
            if total_demand <= capacity:
                a.append(id)
                current_node = id
                ids.remove(id)
            else:
                no.append(id)
        routes.append(a)
        a = []
        current_node = depot


    return routes


def savings_heuristic(px, py, demand, capacity, depot):
    """
    Algorithm for Implementing the savings heuristic to generate VRP solutions.

    :param px: List of X coordinates for each node.
    :param py: List of Y coordinates for each node.
    :param demand: List of each nodes demand.
    :param capacity: Vehicle carrying capacity.
    :param depot: Depot.
    :return: List of vehicle routes (tours).
    """

    # TODO - Implement the Saving Heuristic to generate VRP solutions.
    routes = []
    index = np.arange(len(px))
    ids = [];
    initial_merge = []
    for i in range(len(index)):
        ids.append(i)
    ids.remove(0)
    for i in ids:
        if i != depot:
            m = [i]
            initial_merge.append(m)
    c = capacity
    a = [];

    while len(initial_merge)>1:
        biggest_saving = 0
        mergeid1, mergeid2 = 999, 999
        merge = []
        for i in initial_merge:
            for j in initial_merge:
                if i != j:
                    cost1 = utility.calculate_euclidean_distance(px, py, depot, i[len(i)-1])
                    cost2 = utility.calculate_euclidean_distance(px, py, j[0],depot)
                    saving = cost1 + cost2 - utility.calculate_euclidean_distance(px,py,i[len(i) - 1], j[0])
                    if saving >=biggest_saving:
                        d=0
                        for a in i+j:
                            d+=demand[a]
                        if d <=c:
                            biggest_saving = saving
                            mergeid1 = i
                            mergeid2 = j
                            merge = i + j

        if mergeid1 == 999:
            break;
        else:
            initial_merge.remove(mergeid1)
            initial_merge.remove(mergeid2)
            initial_merge.append(merge)

    return initial_merge

if __name__ == '__main__':
    main()
