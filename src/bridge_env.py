import networkx as nx
import random

class BridgeEnvironment:
    """
    Simulates a bridge structure as a graph where nodes are inspection points.
    """
    def __init__(self, num_nodes=20, connection_prob=0.2):
        self.graph = nx.fast_gnp_random_graph(num_nodes, connection_prob, seed=42)
        # Ensure the graph is connected for navigation
        if not nx.is_connected(self.graph):
            components = list(nx.connected_components(self.graph))
            for i in range(len(components) - 1):
                u = random.choice(list(components[i]))
                v = random.choice(list(components[i+1]))
                self.graph.add_edge(u, v)
        
        # Add metadata to nodes
        self.node_data = {}
        for node in self.graph.nodes():
            self.node_data[node] = {
                "inspected": False,
                "urgency": random.uniform(0, 1),
                "type": random.choice(["VISUAL", "THERMAL", "ACOUSTIC"]),
                "last_drone": None
            }
            
    def get_neighbors(self, node):
        return list(self.graph.neighbors(node))
    
    def mark_inspected(self, node, drone_id):
        self.node_data[node]["inspected"] = True
        self.node_data[node]["last_drone"] = drone_id
        
    def get_uninspected_nodes(self):
        return [node for node, data in self.node_data.items() if not data["inspected"]]

    def get_node_info(self, node):
        return self.node_data[node]
