# Welcome to the dhurandhar-oracle wiki

`dhurandhar-oracle` is a multi-agent decision-support system for Indian intelligence operatives. It combines POMDP, Stackelberg game theory, HMM, Shapley values, CPM/PERT, Value of Information, and Monte Carlo simulation in a LangGraph pipeline, with Claude generating war-room briefings from the quantitative outputs.

---

## Documentation Index

### Start Here

| Page | Audience | What you'll learn |
|---|---|---|
| [Models Guide (Beginner Friendly)](Models-Guide) | New to these algorithms | Plain-language explanation of all 7 models — what each one answers and why it's needed |
| [CLI Usage](CLI-Usage) | Everyone | Every command, every flag, runnable examples for all three modes |
| [Glossary](Glossary) | Everyone | Domain terms, algorithm shorthand, intelligence-ops concepts |

### Technical Deep-Dives

| Page | Audience | What you'll learn |
|---|---|---|
| [Technical Reference](Technical-Reference) | Algorithm / ML engineers | Typed inputs/outputs, mathematical formulation, "why this algorithm" rationale, cross-algorithm dependency chain — all 9 algorithms including career MDP and arc chain |
| [Architecture](Architecture) | System architects, contributors | Layer stack, module dependency map, data flow diagram, three execution modes, error propagation, Indian-side gate |
| [Multi-Agent System](Multi-Agent-System) | LangGraph / agent engineers | All three pipeline topologies (Mermaid diagrams), full `DhurandharState` key contract, parallel fan-out/fan-in, routing functions, Claude narrator integration |

### Data and Schema

| Page | Audience | What you'll learn |
|---|---|---|
| [Schema Reference](Schema-Reference) | Data engineers, contributors | Every Pydantic schema with all fields annotated, JSON data file formats with examples, how to add new operatives / turning points / macro-arcs |

---

## Quick Links

- [Run your first query](CLI-Usage#examples----turning-point-mode)
- [Understand the pipeline topology](Multi-Agent-System#mode-1-turning-point-pipeline-oracle_graph)
- [See the POMDP math](Technical-Reference#1-pomdp--point-based-value-iteration-pbvi)
- [Add a new operative](Schema-Reference#adding-new-operatives-and-turning-points)
- [Understand DhurandharState keys](Multi-Agent-System#dhurandharstate--full-key-contract)

---

## Project Summary

| Aspect | Detail |
|---|---|
| Execution modes | Turning-point (Mode 1), Forward Projection (Mode 2), Arc Rewrite (Mode 3) |
| Algorithms | POMDP/PBVI, Stackelberg, HMM, Shapley, VoI, SNA, CPM/PERT, Monte Carlo, Career MDP, Arc Chain |
| Orchestration | LangGraph StateGraph with parallel fan-out and conditional routing |
| Narrative synthesis | Anthropic Claude (`claude-sonnet-4-6` / `claude-haiku-4-5-20251001`) |
| Data validation | Pydantic v2, 40+ schemas |
| Operative gate | Indian-side characters only (`side="indian"`) |
| CLI | Typer with Rich output |
| Python | 3.11+ |
