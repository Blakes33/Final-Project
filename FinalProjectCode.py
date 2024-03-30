#Keegan Gratton – 100857587
#Curtis Petersen – 100770951
#Chase Nosworthy-Blakeley – 100895860
#Arham Mehdi - 100889136
#Group Project: EV Charging Station Route Optimization Application

#Modules to import
import heapq   # Module for heap queue algorithm
import csv     # Module for reading CSV files

#These require pip3 installation. Used to plot a GUI representation of the node map
#Module for the creation, manipulation, and study of complex networks
import networkx as nx     
# Module for plotting functions
import matplotlib.pyplot as plt   

# Function to read a provided CSV file.
def read_csv(filename, num_columns):
    # Initialize an empty list to store the data
    data = []

    # Open the CSV file
    with open(filename, newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)
        # Skip the header row
        next(reader, None)
        for row in reader:
            if len(row) == num_columns:
                # Parse the row based on the number of columns
                if num_columns == 3:
                    node1, node2, weight = row
                    data.append((node1, node2, int(weight)))
                elif num_columns == 2:
                    node, charging = row
                    data.append((node, charging))
            else:
                print(f"Ignoring row {row}: Incorrect number of columns")

    return data

# Function to build the map from provided edges
def buildMap(edges):
    G = nx.Graph()
    G.add_weighted_edges_from(edges)

    # Draw the graph
    pos = nx.spring_layout(G, seed=42)   # Positions nodes using force-directed algorithm
    nx.draw(G, pos, with_labels=True, node_size=800, font_size=10, font_color='black', font_weight='bold')  # Draw nodes and edges of the graph
    labels = nx.get_edge_attributes(G, 'weight')   # Get edge weights
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)  # Draw edge labels
    
    plt.title("Weighted Graph")    # Set title of the plot
    plt.axis('off')   # Turn off the axis
    plt.show()    # Show the plot

# Function to implement Dijkstra's algorithm for finding shortest paths
def dijkstra(graph, start):
    # Initialize distances with infinity for all nodes except the start node
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    # Initialize a dictionary to keep track of the shortest paths
    shortest_paths = {node: [] for node in graph}
    # Priority queue to store nodes to visit, ordered by distance
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Ignore node if we've already found a shorter path
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            # Update distance if shorter path is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # Update shortest path to neighbor
                shortest_paths[neighbor] = shortest_paths[current_node] + [current_node]
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances, shortest_paths

# Function to find shortest paths to charging stations
def shortest_paths_to_charging_stations(nodes, charging_stations):
    # Convert nodes into a graph representation
    graph = {}
    for node1, node2, weight in nodes:
        graph.setdefault(node1, []).append((node2, weight))
        graph.setdefault(node2, []).append((node1, weight))
    
    shortest_paths = {}
    
    for station, is_charging in charging_stations:
        if is_charging:  # If the station is a charging station
            distances, paths = dijkstra(graph, station)
            shortest_paths[station] = (distances, paths)

    return shortest_paths

# Function to print shortest paths to charging stations
def print_shortest_paths(shortest_paths, start_node):
    desired_stations = ['H', 'K', 'Q', 'T']  # Define the charging stations
    
    min_distance = float('inf')
    closest_station = None
    
    for station in desired_stations:
        distance, path = shortest_paths[station][0][start_node], shortest_paths[station][1][start_node]
        print(f"\nCharging Station: {station}, Distance: {distance}, Path: {' -> '.join(path + [start_node])}")
        if distance < min_distance:
            min_distance = distance
            closest_station = station
    
    print(f"\nThe shortest distance is to Charging Station: {closest_station}, Distance: {min_distance}\n")

# Read nodes and charging stations from CSV files
nodes = read_csv('Nodes.csv', num_columns=3)
chargingStations = read_csv('ChargingStations.csv', num_columns=2)

# Get input from user for starting node
start_node = input("Enter your starting node (from A-W): ").upper()

# Call function to identify which nodes are charging stations
charging_stations = [(station, is_charging) for station, is_charging in chargingStations if is_charging]

# Call function to print paths and shortest path
shortest_paths = shortest_paths_to_charging_stations(nodes, charging_stations)
print_shortest_paths(shortest_paths, start_node)

# Build and display the map
buildMap(nodes)
