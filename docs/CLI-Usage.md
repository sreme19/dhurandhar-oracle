# CLI Usage

`dhurandhar-oracle` exposes a Typer CLI with six main commands. All commands require the package to be installed (see the README Quick Start) and `ANTHROPIC_API_KEY` set in the environment for narrative output.

---

## Installation

```bash
pip install -e .
# or
uv pip install -e .
```

Verify:

```bash
dhurandhar-oracle --help
```

---

## Global Help

```
Usage: dhurandhar-oracle [OPTIONS] COMMAND [ARGS]...

  Dhurandhar intelligence oracle — POMDP, CPM, VoI, Stackelberg

Options:
  --help  Show this message and exit.

Commands:
  run                   Run the oracle (turning-point, forward, or rewrite mode)
  show-strategy         Show only the POMDP strategy table (fast — skips narrator)
  list-turning-points   List available turning points for an operative
  list-characters       List all Indian-side characters available to query
  project-forward       Project an operative's career forward against real events
  rewrite-arc           Counterfactually rewrite an operative's arc across films 1+2
  suggest               List ranked operatives suitable for the chosen mode
  audit-data            Run data quality audit for turning points / outcomes
  backfill-outcomes     Create placeholder outcome files for TPs that have none
```

---

## `run` — Main Oracle Command

The unified entry point. Prompts interactively for mode and output format if not provided as flags.

```
Usage: dhurandhar-oracle run [OPTIONS] OPERATIVE [TURNING_POINT]

Arguments:
  OPERATIVE       Operative ID  e.g. hamza, rizwan-shah                [required]
  TURNING_POINT   Turning point ID for turning-point mode              [optional — prompted if omitted]

Options:
  --mode, -m TEXT              Oracle mode: turning-point | forward | rewrite
  --format, -f TEXT            Output format: narrative | rich | json
  --action TEXT                Force a specific action (counterfactual)
  --until TEXT                 Forward mode horizon (YYYY-MM-DD); default = today
  --force-event-response TEXT  Forward mode override: event_id:action_id
  --force-tp TEXT              Rewrite mode override: turning_point_id:action_id
  --brief                      Use Haiku model for shorter narrative
  --markdown                   Render narrative as Markdown (LinkedIn-paste-friendly)
  --no-narrative               Skip Claude narrative (structured output only)
  --json                       Emit raw JSON state (equivalent to --format json)
  --help
```

### Mode aliases

| Input | Canonical mode |
|---|---|
| `turning-point`, `turning_point`, `turning`, `tp` | `turning-point` |
| `forward`, `project-forward`, `project_forward` | `forward` |
| `rewrite`, `arc-rewrite`, `rewrite-arc`, `rewrite_arc` | `rewrite` |

### Output format aliases

| Input | Canonical format |
|---|---|
| `narrative`, `story`, `linkedin`, `post` | `narrative` — Claude briefing only, Markdown |
| `rich`, `terminal`, `tables`, `structured` | `rich` — Rich-formatted tables + narrative panel |
| `json`, `raw` | `json` — raw JSON state dump |

### Examples — Turning-Point Mode

Run the full pipeline for Hamza at the first Dakait meeting:

```bash
dhurandhar-oracle run hamza dakait-first-meeting
```

Skip the narrative (faster — structured output only):

```bash
dhurandhar-oracle run hamza dakait-first-meeting --no-narrative
```

Force a specific action to evaluate counterfactually:

```bash
dhurandhar-oracle run hamza dakait-first-meeting --action extract_intel_now
```

Get Claude narrative only, formatted as Markdown:

```bash
dhurandhar-oracle run hamza dakait-first-meeting --format narrative
```

Emit raw JSON (for downstream processing):

```bash
dhurandhar-oracle run hamza dakait-first-meeting --json
```

Shorter narrative with Haiku:

```bash
dhurandhar-oracle run hamza dakait-first-meeting --brief --markdown
```

Prompt interactively for mode and format (if `--mode` and `--format` both omitted):

```bash
dhurandhar-oracle run hamza
# Oracle mode (turning-point, forward, rewrite) [turning-point]:
# Output format (narrative, rich, json) [narrative]:
```

### Examples — Forward Projection Mode (via `run`)

```bash
dhurandhar-oracle run hamza --mode forward --until 2026-03-31
```

Force a specific response to one event:

```bash
dhurandhar-oracle run hamza --mode forward --force-event-response pahalgam-2025:pivot_offshore
```

### Examples — Rewrite-Arc Mode (via `run`)

```bash
dhurandhar-oracle run hamza --mode rewrite
```

Force a specific action at one turning point:

```bash
dhurandhar-oracle run hamza --mode rewrite --force-tp dakait-first-meeting:extract_intel_now
```

---

## `project-forward` — Forward Projection Mode

Dedicated command for Mode 2. Equivalent to `run <op> --mode forward`.

```
Usage: dhurandhar-oracle project-forward [OPTIONS] OPERATIVE

Arguments:
  OPERATIVE   Indian-side operative with an authored post-D2 macro-arc  [required]

Options:
  --until TEXT                 ISO date horizon (YYYY-MM-DD); default = today
  --force-event-response TEXT  Override: event_id:action_id
  --brief                      Use Haiku for shorter narrative
  --markdown                   Render as Markdown
  --no-narrative               Skip Claude narrative
  --json                       Emit raw JSON
  --help
```

### Examples

```bash
# Project Hamza's career to end of 2026
dhurandhar-oracle project-forward hamza --until 2026-12-31

# Short Markdown narrative, no tables
dhurandhar-oracle project-forward hamza --brief --markdown

# Force Hamza's response to a specific event
dhurandhar-oracle project-forward hamza \
  --force-event-response sindoor-2025:deep_strike_response \
  --until 2026-06-30
```

---

## `rewrite-arc` — Counterfactual Arc Rewrite

Dedicated command for Mode 3. Equivalent to `run <op> --mode rewrite`.

```
Usage: dhurandhar-oracle rewrite-arc [OPTIONS] OPERATIVE

Arguments:
  OPERATIVE   Indian-side operative with authored turning points across films 1+2  [required]

Options:
  --force-tp TEXT      Force override: turning_point_id:action_id
  --brief              Use Haiku for shorter narrative
  --markdown           Render as Markdown
  --no-narrative       Skip Claude narrative
  --json               Emit raw JSON
  --help
```

### Examples

```bash
# Rewrite Hamza's entire arc
dhurandhar-oracle rewrite-arc hamza

# Force a specific turning point prescription
dhurandhar-oracle rewrite-arc hamza --force-tp 26-11-celebration-revelation:immediate_exfil

# JSON output for downstream analysis
dhurandhar-oracle rewrite-arc hamza --json | jq '.arc_rewrite.cumulative_q_delta'
```

---

## `show-strategy` — Fast POMDP Table

Runs only up to `strategy_node` and prints the POMDP action-value table. Skips the full pipeline and narrator — useful for quick action ranking without the computational overhead of Monte Carlo or narrative generation.

```
Usage: dhurandhar-oracle show-strategy OPERATIVE TURNING_POINT

Arguments:
  OPERATIVE       Operative ID   [required]
  TURNING_POINT   Turning point ID  [required]
```

### Example

```bash
dhurandhar-oracle show-strategy hamza dakait-first-meeting
```

Output:

```
POMDP — Optimal Policy
 Action                    Q(b,a)   Note
 build_trust_slow          4.821    ← OPTIMAL
 gather_street_intel       3.412
 extract_intel_now         1.983
 abort_mission             0.441

  V(b) = 4.82 | P(mission success) = 71.3% | P(cover intact) = 88.4%
```

---

## `list-turning-points` — List Available Turning Points

```
Usage: dhurandhar-oracle list-turning-points OPERATIVE

Arguments:
  OPERATIVE   Operative ID  [required]
```

### Example

```bash
dhurandhar-oracle list-turning-points hamza
```

Output: Rich table with columns ID, Film, Act, Description (truncated to 70 chars).

---

## `list-characters` — List Queryable Operatives

Lists all Indian-side characters available to query (i.e., `side="indian"`).

```
Usage: dhurandhar-oracle list-characters
```

Output: Rich table with columns ID, Name, Role, Films, Cover identity.

---

## `suggest` — Find Operatives Ready for a Mode

```
Usage: dhurandhar-oracle suggest [OPTIONS]

Options:
  --mode TEXT   forward | rewrite  [default: forward]
  --help
```

### Forward mode output groups

| Group | Condition |
|---|---|
| Ready | Has an authored `data/post_d2_arc/<id>.json` |
| Fictional — needs macro-arc | Indian operative without a post-D2 arc file |
| Real public figures — projection is speculative | `is_speculative_real_figure=True` |

### Rewrite mode output groups

| Group | Condition |
|---|---|
| Eligible | Has at least one authored turning point |
| No turning points authored | Indian operative with no TP files |

### Examples

```bash
dhurandhar-oracle suggest --mode forward
dhurandhar-oracle suggest --mode rewrite
```

---

## `audit-data` — Data Quality Check

Scans all turning points and outcomes and reports:
- Total counts of turning points and outcomes
- Turning points with missing outcome files
- Turning points or outcomes missing `source_refs`
- Causal edges with confidence < 0.5
- Invalid (schema-failing) turning points or outcomes

```bash
dhurandhar-oracle audit-data
```

Sample output:

```
Data Coverage turning_points=24 outcomes=18
Missing outcomes (6): sindoor-response, ...
Turning points missing source_refs (3).
Low-confidence causal edges (<0.5): 7
```

---

## `backfill-outcomes` — Create Outcome Placeholders

Creates template outcome JSON files for any turning points that have no corresponding outcome file. Templates have `actual_action` set to the first available action and `confidence=0.1` — these should be reviewed and updated with correct values.

```bash
dhurandhar-oracle backfill-outcomes
```

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | For narrative output | Enables Claude API calls in `narrator_node`. Without this, a Rich template fallback is used. |

---

## Output Formats in Detail

### `rich` (default for `run`)

Prints a sequence of Rich tables to the terminal:

1. **POMDP — Optimal Policy** — all actions ranked by Q(b,a), optimal highlighted
2. **Critical Path (CPM/PERT)** — critical path, total/optimal duration, bottleneck, parallelisable pairs
3. **Value of Information** — ranked intelligence targets with VoI bits, effort, recommendation
4. **Stackelberg Equilibrium** — handler commitment, operative response, adversary counter, commitment value
5. **Belief Gaps — HMM Mole Detection** — actor, believed state, inferred state, gap, mole alert flag
6. **Shapley Values — Asset Coalition** — actor, φᵢ, defection incentive, risk level
7. **Monte Carlo Simulation** — actual vs optimal P(success), 95% CI, Δ if optimal path taken
8. **War-Room Briefing panel** — Claude narrative (or template fallback)

### `narrative` (LinkedIn-paste)

Outputs only the Claude narrative as Markdown. Implicitly sets `--markdown`. No tables.

### `json`

Dumps the full `DhurandharState` as JSON. All Pydantic models are serialised via `model_dump()`. Useful for downstream processing:

```bash
# Extract POMDP optimal action
dhurandhar-oracle run hamza dakait-first-meeting --json | jq '.pomdp.optimal_action'

# Get all Q-values
dhurandhar-oracle run hamza dakait-first-meeting --json | jq '.pomdp.action_values'

# Monte Carlo delta
dhurandhar-oracle run hamza dakait-first-meeting --json \
  | jq '.simulation_optimal.p_mission_success - .simulation_actual.p_mission_success'
```

---

## Exit Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Oracle errors (check stderr for `ERROR:` lines) |
| 2 | Invalid CLI arguments (bad mode, bad format, bad `--force-*` syntax) |
