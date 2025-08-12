class WeightedGraph:
    def __init__(self, node_count):
        self.connection_matrix = [[0] * node_count for _ in range(node_count)]
        self.node_count = node_count
        self.node_labels = [''] * node_count

    def create_connection(self, node1, node2, cost):
        if 0 <= node1 < self.node_count and 0 <= node2 < self.node_count:
            self.connection_matrix[node1][node2] = cost
            self.connection_matrix[node2][node1] = cost  # Bidirectional connection

    def assign_label(self, node, label):
        if 0 <= node < self.node_count:
            self.node_labels[node] = label

    def compute_shortest_paths(self, source_label):
        source_node = self.node_labels.index(source_label)
        path_costs = [float('inf')] * self.node_count
        path_costs[source_node] = 0
        processed_nodes = [False] * self.node_count
        
        for _ in range(self.node_count):
            current_min = float('inf')
            current_node = None

            for i in range(self.node_count):
                if not processed_nodes[i] and path_costs[i] < current_min:
                    current_min = path_costs[i]
                    current_node = i

            if current_node is None:
                break

            processed_nodes[current_node] = True

            for neighbor in range(self.node_count):
                if self.connection_matrix[current_node][neighbor] > 0 and not processed_nodes[neighbor]:
                    new_cost = path_costs[current_node] + self.connection_matrix[current_node][neighbor]
                    if new_cost < path_costs[neighbor]:
                        path_costs[neighbor] = new_cost
        
        return path_costs

# Create a transportation network with 7 locations
transport_network = WeightedGraph(7)

transport_network.assign_label(0, 'Central')
transport_network.assign_label(1, 'North')
transport_network.assign_label(2, 'East')
transport_network.assign_label(3, 'West')
transport_network.assign_label(4, 'South')
transport_network.assign_label(5, 'Airport')
transport_network.assign_label(6, 'Harbor')

# Establish connections with travel times
transport_network.create_connection(3, 0, 4)  # West - Central, 4 mins
transport_network.create_connection(3, 4, 2)  # West - South, 2 mins
transport_network.create_connection(0, 2, 3)  # Central - East, 3 mins
transport_network.create_connection(0, 4, 4)  # Central - South, 4 mins
transport_network.create_connection(2, 4, 4)  # East - South, 4 mins
transport_network.create_connection(4, 6, 5)  # South - Harbor, 5 mins
transport_network.create_connection(2, 5, 5)  # East - Airport, 5 mins
transport_network.create_connection(2, 1, 2)  # East - North, 2 mins
transport_network.create_connection(1, 5, 2)  # North - Airport, 2 mins
transport_network.create_connection(6, 5, 5)  # Harbor - Airport, 5 mins

# Calculate shortest travel times from West station
print("Optimal travel times from West station:\n")
travel_times = transport_network.compute_shortest_paths('West')
for i, time in enumerate(travel_times):
    print(f"Minimum time from West to {transport_network.node_labels[i]}: {time}")