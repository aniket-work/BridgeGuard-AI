import base64
import requests
import os

def generate_diagrams():
    diagrams = {
        "title_diagram": """
graph TB
    subgraph "BridgeGuard-AI: Resilient Infrastructure"
        A[Structural Node A] --- B[Truss B]
        B --- C[Joint C]
        C --- D[Support D]
        E[Drone Swarm] -.-> B
        E -.-> C
    end
    style A fill:#f9f,stroke:#333,stroke-width:4px
    style E fill:#00ff00,stroke:#333,stroke-width:2px
""",
        "architecture_diagram": """
graph LR
    subgraph "Edge Components"
        A[Bridge Environment]
        B[Inspection Drones]
    end
    subgraph "Orchestration"
        C[Auction House]
        D[Path Planner]
    end
    A <--> C
    B <--> C
    B <--> D
    D <--> A
""",
        "sequence_diagram": """
sequenceDiagram
    participant B as Bridge Environment
    participant A as Auction House
    participant D as Drone Agent
    B->>A: Uninspected Node Alert
    A->>D: Request Bids
    D->>A: Submit Bid (Dist, Batt, Sensor)
    A->>D: Assign Winner
    D->>B: Inspect Node
    B->>B: Mark Complete
""",
        "flow_diagram": """
flowchart TD
    Start[Initialization] --> Scan[Scan Bridge Graph]
    Scan --> Find[Identify Uninspected Nodes]
    Find --> Auction{Auction Required?}
    Auction -- Yes --> Bid[Drone Bidding]
    Bid --> Assign[Assign Winner]
    Assign --> Move[Move to Node]
    Move --> Inspect[Perform Inspection]
    Inspect --> Update[Update Status]
    Update --> Find
    Auction -- No --> End[Mission Complete]
"""
    }

    if not os.path.exists("images"):
        os.makedirs("images")

    for name, code in diagrams.items():
        encoded = base64.b64encode(code.encode()).decode()
        url = f"https://mermaid.ink/img/{encoded}"
        print(f"Generating {name}...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"images/{name}.png", 'wb') as f:
                f.write(response.content)
            print(f"Successfully saved images/{name}.png")
        else:
            print(f"Failed to generate {name}: {response.status_code}")

if __name__ == "__main__":
    generate_diagrams()
