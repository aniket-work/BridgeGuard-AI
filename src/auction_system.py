class AuctionHouse:
    """
    Handles task allocation using a bidding mechanism.
    """
    def __init__(self):
        self.active_auctions = {}

    def run_auction(self, node_id, node_info, drones, bridge_graph):
        bids = []
        for drone in drones:
            if drone.status == "IDLE":
                bid_value = drone.calculate_bid(node_id, node_info, bridge_graph)
                if bid_value > 0:
                    bids.append((bid_value, drone))
        
        if not bids:
            return None
            
        # Select winner (highest bid)
        bids.sort(key=lambda x: x[0], reverse=True)
        winner_bid, winner_drone = bids[0]
        
        winner_drone.target_node = node_id
        winner_drone.status = "MOVING"
        return winner_drone.drone_id
