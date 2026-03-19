import sys
import os
import json
import time

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from bridge_env import BridgeEnvironment
from drone_agent import InspectionDrone
from auction_system import AuctionHouse

def run_simulation(steps=100):
    env = BridgeEnvironment(num_nodes=30, connection_prob=0.15)
    auction_house = AuctionHouse()
    
    drones = [
        InspectionDrone(1, pos=0, sensors=["VISUAL", "THERMAL"]),
        InspectionDrone(2, pos=0, sensors=["VISUAL", "ACOUSTIC"]),
        InspectionDrone(3, pos=15, sensors=["THERMAL", "ACOUSTIC"]),
        InspectionDrone(4, pos=29, sensors=["VISUAL", "THERMAL", "ACOUSTIC"])
    ]
    
    history = []
    
    print(f"--- BridgeGuard-AI: Resilient Infrastructure Swarm Simulation ---")
    print(f"Total Inspection Points: {len(env.graph.nodes())}")
    print(f"Active Drones: {len(drones)}")
    print("-" * 50)
    
    for t in range(steps):
        uninspected = env.get_uninspected_nodes()
        if not uninspected:
            print(f"Step {t}: All nodes inspected!")
            break
            
        # Try to auction uninspected nodes
        for node in uninspected:
            # Check if anyone is already targeting it
            already_targeted = any(d.target_node == node for d in drones)
            if not already_targeted:
                node_info = env.get_node_info(node)
                winner_id = auction_house.run_auction(node, node_info, drones, env.graph)
                if winner_id:
                    print(f"Step {t}: Node {node} ({node_info['type']}) won by Drone {winner_id}")

        # Update drones
        for d in drones:
            if d.status == "MOVING":
                d.move_towards_target(env.graph)
            elif d.status == "ARRIVED":
                d.perform_inspection()
                env.mark_inspected(d.pos, d.drone_id)
                print(f"Step {t}: Drone {d.drone_id} completed inspection of Node {d.pos}")
        
        # Log state
        state = {
            "step": t,
            "drones": [
                {"id": d.drone_id, "pos": int(d.pos), "status": d.status, "battery": round(d.battery, 1)}
                for d in drones
            ],
            "inspected_nodes": [int(n) for n in env.get_uninspected_nodes() == []]
        }
        history.append(state)
        
    # Final statistics
    print("-" * 50)
    print("Simulation Summary:")
    for d in drones:
        print(f"Drone {d.drone_id}: {d.total_inspections} inspections | Final Battery: {d.battery}%")
        
    return history

if __name__ == "__main__":
    run_simulation(steps=200)
