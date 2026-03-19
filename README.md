# BridgeGuard-AI: Autonomous Multi-Agent Inspection Swarm

![Title](https://raw.githubusercontent.com/aniket-work/BridgeGuard-AI/main/images/title_diagram.png)

> **Autonomous multi-agent inspection system for critical infrastructure using graph-based navigation and dynamic auctions.**

## Overview

BridgeGuard-AI is an experimental Proof-of-Concept (PoC) demonstrating how a swarm of autonomous drones can coordinate the inspection of complex structural environments like bridges. By representing the structure as a mathematical graph and employing a dynamic auction-based task allocation system, the swarm can optimize for efficiency, battery usage, and sensor compatibility without centralized control.

![Architecture](https://raw.githubusercontent.com/aniket-work/BridgeGuard-AI/main/images/architecture_diagram.png)

## Key Features

1. **Graph-Based Navigation**: Structural points are represented as nodes in a graph, allowing drones to calculate optimized flight paths using shortest-path algorithms.
2. **Dynamic Auctions**: Task allocation is handled via a decentralized bidding system where drones compete for inspection points based on proximity, battery life, and sensor availability.
3. **Multi-Sensor Coordination**: Different nodes require specific sensors (Thermal, Visual, Acoustic). The auction system ensures the right agent is assigned to the right task.
4. **Real-Time Visualization**: Transparent simulation logging for monitoring swarm behavior and structural coverage status.

## System Architecture

![Sequence](https://raw.githubusercontent.com/aniket-work/BridgeGuard-AI/main/images/sequence_diagram.png)

The system consists of three primary components:
- **Bridge Environment**: A simulated structural graph with heterogenous inspection requirements.
- **Drone Agents**: Intelligent units with local decision-making capabilities.
- **Auction House**: A middleware for non-centralized task distribution.

## Workflow

![Flow](https://raw.githubusercontent.com/aniket-work/BridgeGuard-AI/main/images/flow_diagram.png)

1. Initial structural scan creates the graph.
2. Drones initialize at designated docking points.
3. Uninspected nodes are auctioned to the local fleet.
4. Drones move, inspect, and update the global state.

## Installation

```bash
git clone https://github.com/aniket-work/BridgeGuard-AI.git
cd BridgeGuard-AI
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python simulation.py
```

## Visual Results

![Simulation Results](https://raw.githubusercontent.com/aniket-work/BridgeGuard-AI/main/images/title-animation.gif)

---
*Disclaimer: This project is an experimental PoC. It is intended for educational and research purposes and is not certified for real-world infrastructure safety inspections.*
