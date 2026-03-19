import networkx as nx

class InspectionDrone:
    """
    Represents an autonomous inspection drone (agent).
    """
    def __init__(self, drone_id, pos, sensors, battery=100.0):
        self.drone_id = drone_id
        self.pos = pos
        self.sensors = sensors  # List of supported types e.g., ["VISUAL", "THERMAL"]
        self.battery = battery
        self.status = "IDLE"  # IDLE, MOVING, INSPECTING
        self.target_node = None
        self.path = []
        self.total_inspections = 0
        
    def calculate_bid(self, node_id, node_info, bridge_graph):
        """
        Calculate a bid for a node based on distance, compatibility, and urgency.
        """
        if node_info["type"] not in self.sensors:
            return 0  # Incompatible sensor
            
        try:
            distance = nx.shortest_path_length(bridge_graph, self.pos, node_id)
        except nx.NetworkXNoPath:
            return 0
            
        # Fuel efficiency check
        if self.battery < (distance * 2 + 5):
            return 0
            
        # Bid formula: (Urgency * 100) / (Distance + 1)
        bid = (node_info["urgency"] * 100) / (distance + 1)
        return round(bid, 2)
        
    def move_towards_target(self, bridge_graph):
        if not self.path and self.target_node is not None:
            self.path = nx.shortest_path(bridge_graph, self.pos, self.target_node)[1:]
            
        if self.path:
            self.pos = self.path.pop(0)
            self.battery -= 1.0
            self.status = "MOVING"
            return True
        else:
            self.status = "ARRIVED"
            return False

    def perform_inspection(self):
        if self.status == "ARRIVED":
            self.battery -= 5.0
            self.total_inspections += 1
            self.status = "IDLE"
            self.target_node = None
            return True
        return False
