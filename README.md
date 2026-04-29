# dhurandhar-oracle

> **Multi-agent AI system for Indian intelligence operatives in the Dhurandhar universe**

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

The Dhurandhar Oracle is a decision-support system that computes optimal intelligence strategies using advanced game theory, operations research, and probabilistic reasoning algorithms. Built with [LangGraph](https://langchain-ai.github.io/langgraph/) for agent orchestration.

## What It Computes

Given a character and a turning point in their mission, the oracle provides:

| Computation | Algorithm | Output |
|-------------|-----------|--------|
| **Optimal next action** | POMDP (Point-Based Value Iteration) | Best policy under uncertainty |
| **What could have been done faster** | CPM/PERT critical path analysis | Time-saving opportunities |
| **Which intelligence to gather next** | Value of Information (VoI) | Ranked intel priorities |
| **How adversaries will respond** | Stackelberg equilibrium | Leader-follower game outcome |
| **Who is hiding something** | HMM belief gap analysis | Mole detection alerts |
| **Most valuable asset** | Shapley values | Coalition contribution scores |
| **Mission success probability** | Monte Carlo simulation | Success/failure confidence intervals |

## Quick Start

```bash
# Clone the repository
git clone https://github.com/sreme19/dhurandhar-oracle.git
cd dhurandhar-oracle

# Install dependencies
pip install -e ".[dev]"

# Run the oracle
dhurandhar-oracle run hamza dakait-first-meeting

# List available characters
dhurandhar-oracle list-characters

# List turning points for an operative
dhurandhar-oracle list-turning-points hamza
```

## Installation

Requires Python 3.11 or higher.

```bash
pip install dhurandhar-oracle
```

Or install from source:

```bash
git clone https://github.com/sreme19/dhurandhar-oracle.git
cd dhurandhar-oracle
pip install -e ".[dev]"
```

## Usage

### CLI Commands

```bash
# Run full oracle pipeline for an operative at a turning point
dhurandhar-oracle run <operative> <turning-point> [OPTIONS]

# Options:
#   --action TEXT        Force a specific action (counterfactual)
#   --no-narrative       Skip Claude narrative (structured output only)
#   --json               Emit raw JSON state

# Show only the POMDP strategy table (fast)
dhurandhar-oracle show-strategy <operative> <turning-point>

# List available turning points for an operative
dhurandhar-oracle list-turning-points <operative>

# List all Indian-side operatives
dhurandhar-oracle list-characters
```

### Example Output

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ POMDP — Optimal Policy                           ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃ Action          ┃ Q(b,a)  ┃ Note                 ┃
┣━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┫
┃ deepen_cover    ┃ 0.847   ┃ ← OPTIMAL            ┃
┃ gather_intel    ┃ 0.721   ┃                      ┃
┃ direct_contact  ┃ 0.534   ┃                      ┃
┗━━━━━━━━━━━━━━━━━┷━━━━━━━━━┷━━━━━━━━━━━━━━━━━━━━━━┛
  V(b) = 7.42 | P(mission success) = 68.4% | P(cover intact) = 82.1%

Critical Path (CPM/PERT)
  infiltrate_network → build_trust → extract_intel → exfil_data
  Total: 45d  →  Optimal: 32d  (save 13d)
  Bottleneck: build_trust
  Parallelisable: gather_comms‖bribe_contact

Value of Information
  #1: jamali_location (VoI: 2.34 bits) — Priority gather
  #2: dakait_schedule (VoI: 1.87 bits) — Monitor channels
  #3: mole_identity   (VoI: 0.92 bits) — Defer
```

## Architecture

### Agent Pipeline (LangGraph)

```
START → state_node ──┬──► intel_network_node ──┐
                     │                          ├──► belief_node → voi_node
                     └──► coalition_node ───────┘                                    ↓
                                                                           adversary_node (Stackelberg)
                                                                                ↓
                                                                           strategy_node (POMDP)
                                                                                ↓
                                                                           critical_path_node (CPM)
                                                                                ↓
                                                                           simulator_node (Monte Carlo)
                                                                                ↓
                                                                     ┌──────────┴──────────┐
                                                                     ▼                     ▼
                                                              narrator_node ───────────► END
```

### Key Algorithms

| Algorithm | Domain | Purpose |
|-----------|--------|---------|
| **POMDP (PBVI)** | Partially Observable Markov Decision Process | Planning under uncertainty when the operative doesn't know the full world state |
| **Stackelberg** | Sequential game theory | Handler commits to strategy first, operative responds, adversary follows |
| **CPM/PERT** | Operations research | Mission scheduling and parallelisation opportunities |
| **Value of Information** | Information theory | Rank intelligence targets by expected entropy reduction |
| **HMM (Viterbi)** | Hidden Markov Models | Mole detection via hidden loyalty state inference |
| **Shapley Values** | Cooperative game theory | Fair attribution of coalition value to individual assets |

### Operative State (5-dimensional)

```python
class OperativeState:
    cover_integrity:    float  # 0-10, false identity intactness
    trust_capital:      float  # 0-10, target network trust
    intelligence_depth: float  # 0-10, quality of intel gathered
    network_strength:   float  # 0-10, handler/asset support quality
    exposure_risk:      float  # 0-10, discovery probability
```

## Data Model

### Character Profile

Characters include Indian operatives, Pakistani adversaries, and assets. Only `side="indian"` characters can be queried as operatives.

```json
{
  "id": "hamza",
  "name": "Hamza",
  "nationality": "Indian",
  "side": "indian",
  "role": "RAW undercover operative",
  "films": [1, 2],
  "cover_identity": "Karachi criminal operative",
  "real_life_inspiration": "Ravindra Kaushik"
}
```

### Turning Point

The fundamental query unit. One per key scene/decision across both films.

```json
{
  "id": "dakait-first-meeting",
  "operative": "hamza",
  "film": 1,
  "act": 2,
  "description": "First contact with Rehman Dakait",
  "state_vector": { ... },
  "available_actions": ["deepen_cover", "gather_intel", ...],
  "mission_tasks": [ ... ],
  "adversaries": [ ... ],
  "intelligence_targets": [ ... ]
}
```

## Project Structure

```
dhurandhar-oracle/
├── dhurandhar_oracle/
│   ├── agents/           # LangGraph node implementations
│   │   ├── state_node.py
│   │   ├── strategy_node.py      # POMDP (PBVI)
│   │   ├── adversary_node.py     # Stackelberg equilibrium
│   │   ├── critical_path_node.py # CPM/PERT
│   │   ├── voi_node.py           # Value of Information
│   │   ├── belief_node.py        # HMM belief gaps
│   │   ├── coalition_node.py     # Shapley values
│   │   ├── intel_network_node.py # SNA centrality
│   │   ├── simulator_node.py     # Monte Carlo
│   │   └── narrator_node.py      # Claude narrative
│   ├── optimisation/     # Core algorithms
│   │   ├── pomdp.py      # Point-Based Value Iteration
│   │   ├── stackelberg.py
│   │   ├── cpm.py        # Critical Path Method
│   │   ├── voi.py        # Value of Information
│   │   ├── hmm.py        # Hidden Markov Models
│   │   ├── shapley.py
│   │   └── network.py    # SNA metrics
│   ├── io/
│   │   └── loader.py     # JSON data loaders
│   ├── data/             # Encyclopedia data
│   │   ├── characters/   # Character profiles
│   │   ├── adversaries/  # Adversary models
│   │   ├── context/      # Historical context
│   │   └── timeline/     # Mission chronology
│   ├── schemas.py        # Pydantic data models
│   ├── state.py          # LangGraph state definitions
│   ├── graph.py          # Agent pipeline graph
│   └── cli.py            # Typer CLI interface
├── tests/
│   ├── test_pipeline.py
│   └── test_optimisation.py
├── pyproject.toml
└── README.md
```

## Development

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=dhurandhar_oracle

# Linting
ruff check dhurandhar_oracle/
ruff format dhurandhar_oracle/
```

## Algorithmic Heritage

This project is the third in a series exploring AI decision systems:

| Project | Techniques Introduced |
|---------|----------------------|
| [ipl-oracle](https://github.com/sreme19/ipl-oracle) | MILP, MDP, Monte Carlo, Bayesian networks, LangChain |
| [got-oracle](https://github.com/sreme19/got-oracle) | CFR, HMM, Prospect Theory, Shapley values, SNA, LangGraph |
| **dhurandhar-oracle** | **POMDP (PBVI), CPM/PERT, Value of Information, Stackelberg** |

## Why These Algorithms?

### POMDP vs MDP
Intelligence operations are the canonical POMDP domain — the operative never knows the full world state. Is the handler compromised? Does Dakait suspect Hamza? POMDP planning operates over a *belief state* (probability distribution over possible world states), producing policies that account for uncertainty.

### Stackelberg vs CFR
In Dhurandhar, the RAW handler *commits* to a strategy before the operative acts, and the operative acts before adversaries can respond. This sequential leader-follower dynamic is captured by Stackelberg equilibrium, not simultaneous-move Nash equilibrium.

### CPM/PERT
The "what could have been done faster" question is literally a project scheduling problem. PERT three-point estimation (optimistic, most-likely, pessimistic) captures task duration uncertainty.

## Hard Constraints

- **Indian-side characters only.** The oracle refuses queries for Pakistani adversaries (Rehman Dakait, Jameel Jamali, etc.). Those characters exist only as adversary models in the computation.
- The `side` field is validated at CLI entry and at `state_node` load time.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Acknowledgments

- Built with [LangGraph](https://langchain-ai.github.io/langgraph/) for agent orchestration
- CLI powered by [Typer](https://typer.tiangolo.com/) and [Rich](https://rich.readthedocs.io/)
- Pydantic for data validation
- NetworkX for social network analysis
- NumPy/SciPy for numerical computation

---

**Disclaimer:** This is a fictional decision-support system for narrative analysis. All characters and scenarios are drawn from the Dhurandhar film universe.
