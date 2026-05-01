# Architecture

This page describes the overall system structure of `dhurandhar-oracle` from four angles: the layer stack, module dependencies, runtime data flow, and the three execution modes. For the LangGraph pipeline internals see [Multi-Agent System](Multi-Agent-System). For algorithm details see [Technical Reference](Technical-Reference).

---

## Layer Stack

The system is organised into five horizontal layers. Data flows strictly upward — lower layers do not import from higher layers.

```
┌─────────────────────────────────────────────────────┐
│                    CLI  (cli.py)                     │
│  Typer commands — run / project-forward / rewrite-   │
│  arc / suggest / show-strategy / audit-data          │
├─────────────────────────────────────────────────────┤
│          LangGraph Orchestration                     │
│  graph.py          oracle_graph  (turning-point)     │
│  forward_graph.py  forward_graph (Mode 2)            │
│  rewrite_graph.py  rewrite_graph (Mode 3)            │
├─────────────────────────────────────────────────────┤
│              Agent Nodes  (agents/)                  │
│  state_node  intel_network_node  coalition_node      │
│  belief_node  voi_node  adversary_node               │
│  strategy_node  critical_path_node  simulator_node   │
│  narrator_node  forward_state_node  forward_proj…    │
│  realworld_context_node  arc_rewrite_node            │
├─────────────────────────────────────────────────────┤
│          Optimisation Algorithms (optimisation/)     │
│  pomdp.py  stackelberg.py  hmm.py  shapley.py        │
│  voi.py  network.py  cpm.py  career_mdp.py           │
│  arc_chain.py                                        │
├─────────────────────────────────────────────────────┤
│     Data Models + I/O  (schemas.py / io/loader.py)  │
│  40+ Pydantic models — type contracts between nodes  │
├─────────────────────────────────────────────────────┤
│              Data Layer  (data/)                     │
│  characters/  adversaries/  turning_points/          │
│  outcomes/  context/  post_d2_arc/  timeline/        │
└─────────────────────────────────────────────────────┘
```

---

## Module Dependency Map

```
cli.py
  ├── graph.py (oracle_graph)
  │     └── agents/*_node.py
  │           └── optimisation/*.py
  │                 └── schemas.py
  │                 └── io/loader.py
  │                       └── data/ (JSON files)
  ├── forward_graph.py (forward_graph)
  │     └── agents/forward_state_node.py
  │     └── agents/realworld_context_node.py
  │     └── agents/forward_projection_node.py
  │           └── optimisation/career_mdp.py
  │     └── agents/narrator_node.py  (reused)
  └── rewrite_graph.py (rewrite_graph)
        └── agents/arc_rewrite_node.py
              └── optimisation/arc_chain.py
                    └── graph.py  (oracle_graph — invoked per TP)
        └── agents/narrator_node.py  (reused)

state.py  ←  DhurandharState TypedDict + routing helpers
schemas.py ←  all Pydantic data models (40+ classes)
io/loader.py ←  JSON → Pydantic deserialisation
```

Key dependency to note: `arc_chain.py` (Mode 3) imports and invokes `oracle_graph` (Mode 1) once per turning point. This means the rewrite-arc pipeline is a meta-loop over the full turning-point pipeline.

---

## Data Flow — Turning-Point Mode

This diagram follows a single query from CLI invocation to printed output.

```
User: dhurandhar-oracle run hamza dakait-first-meeting
         │
         ▼
      cli.py: run()
         │  initial_state = {operative, turning_point, mode, errors: [], warnings: []}
         ▼
   oracle_graph.invoke(initial_state)
         │
         ▼
   state_node
   ├── load_character("hamza")  →  CharacterProfile (side="indian" gate ✓)
   ├── load_turning_point("dakait-first-meeting")  →  TurningPoint JSON
   └── writes: state_vector, available_actions, causal_dag, adversaries,
               alliance_snapshot, mission_tasks, intelligence_targets,
               initial_belief_state, turning_point_description
         │
         ├──────────────────────────────────┐
         ▼ (parallel)                        ▼ (parallel)
  intel_network_node               coalition_node
  NetworkX SNA analysis            Shapley values
  writes: centrality,              writes: shapley
          threat_scores,
          high_threat_actors
         │                                  │
         └──────────────┬───────────────────┘
                        ▼ (fan-in)
                   belief_node
                   HMM per high-threat actor
                   writes: hmm_results, belief_gaps
                        │
                        ▼
                    voi_node
                    Shannon entropy ranking
                    writes: voi_result
                        │
                        ▼
                 adversary_node
                 Stackelberg equilibrium
                 writes: stackelberg
                        │
                        ▼
                  strategy_node
                  POMDP PBVI solver
                  writes: pomdp
                        │
                        ▼
              critical_path_node
              CPM + PERT scheduling
              writes: critical_path
                        │
                        ▼
                 simulator_node
                 Monte Carlo rollouts
                 writes: simulation_actual, simulation_optimal
                        │
                        ▼
             route_after_simulator()
             ├── errors present? → END (cli prints errors, exits 1)
             └── no errors?      → narrator_node
                                        │
                                        ▼
                                  narrator_node
                                  Claude API call (claude-sonnet-4-6)
                                  or template fallback (no API key)
                                  writes: narrative
                                        │
                                        ▼
                                       END
                                        │
         ▼
      cli.py: prints Rich tables + narrative panel
```

---

## Three Execution Modes

| | Mode 1: Turning-Point | Mode 2: Forward Projection | Mode 3: Arc Rewrite |
|---|---|---|---|
| **CLI command** | `run <op> <tp>` | `project-forward <op>` | `rewrite-arc <op>` |
| **Graph** | `oracle_graph` | `forward_graph` | `rewrite_graph` |
| **Question** | Optimal action at this scene | Career trajectory 2025–2026 | Counterfactual rewrite films 1+2 |
| **Core algorithm** | POMDP + 7-algorithm pipeline | Finite-horizon MDP (backward induction) | Arc chain (oracle_graph × N TPs) |
| **State input** | `TurningPoint` JSON | `MacroArc` JSON | All `TurningPoint` JSONs + `Outcome` JSONs |
| **Key output** | `pomdp`, `stackelberg`, `critical_path`, `simulation_*`, `narrative` | `forward_projection` (predicted vs prescribed) | `arc_rewrite` (cumulative Q-delta, 5d objective delta) |
| **Narrative model** | `claude-sonnet-4-6` (or Haiku with `--brief`) | `claude-sonnet-4-6` (or Haiku with `--brief`) | `claude-sonnet-4-6` (or Haiku with `--brief`) |
| **Real public figures** | Not applicable | Flagged `[SPECULATIVE]` if `is_speculative_real_figure=True` | Not applicable |

---

## Indian-Side Gate

**Every pipeline entry point validates operative side before any computation runs.**

```
state_node          → load_character(operative)
                      if char.side != "indian": errors.append(…); return early

forward_state_node  → same check for Mode 2

arc_rewrite_node    → same check for Mode 3
```

There is **no `--allow-adversary` flag**. Pakistani-side characters exist only as `AdversaryModel` objects inside algorithm inputs — they cannot be queried as protagonists. Any attempt returns an error and exits with code 1.

The gate is redundant by design: validated at the CLI before graph invocation, and again inside each mode's entry node.

---

## Error Propagation

Errors written to `state["errors"]` (an `Annotated[list, operator.add]` field) short-circuit the pipeline:

- **After `simulator_node`:** `route_after_simulator()` checks `state["errors"]`. If non-empty, routes to `END` (skips narrator). CLI prints errors and exits 1.
- **After `forward_projection_node`:** `_route_after_projection()` applies the same check.
- **After `arc_rewrite_node`:** `_route()` applies the same check.

Warnings (`state["warnings"]`) are appended similarly but do not stop execution — they are printed to the terminal before output.

---

## Anthropic API Integration

The `narrator_node` is the only component that calls the Anthropic API.

| Condition | Model used | Token budget |
|---|---|---|
| `--brief` flag | `claude-haiku-4-5-20251001` | 1024 |
| Default | `claude-sonnet-4-6` | 2048 |

If `ANTHROPIC_API_KEY` is not set, `narrator_node` falls back to a Rich-formatted template with the same structure — all quantitative outputs are still rendered, only the narrative synthesis is replaced.

The system prompt instructs Claude to write as a RAW war-room analyst briefing the NSA, in a clipped classified-document tone. If `--markdown` is passed, the prompt appends a Markdown/LinkedIn formatting instruction.

---

## Data Directory Structure

```
data/
├── characters/          CharacterProfile JSON — one file per operative/character
│   └── hamza.json       (see Schema Reference for field list)
├── adversaries/         Raw adversary intelligence files (~50 files)
├── turning_points/      TurningPoint JSON — one per key scene
│   └── dakait-first-meeting.json
├── outcomes/            OutcomeEntry JSON — actual action taken at each TP
│   └── dakait-first-meeting.json
├── context/             Real-world geopolitical event context files
│   └── pahalgam-2025.json
├── post_d2_arc/         MacroArc JSON — per operative for Mode 2
│   └── hamza.json
├── timeline/            Chronological mission timeline
└── encyclopedia_index.json   Index of all data entities
```

All JSON files are loaded and validated against Pydantic models at runtime. See [Schema Reference](Schema-Reference) for the exact field specifications and [CLI Usage](CLI-Usage) for the `audit-data` command that checks coverage.
