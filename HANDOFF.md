# Handoff — running dhurandhar-oracle on your laptop

This is a step-by-step guide to getting the new `project-forward`,
`rewrite-arc`, and `suggest` commands running locally. Run each step in
order. If a step fails, stop and tell me the error.

The branch with the new code is `claude/redefine-project-objective-ngE54`.

---

## Prerequisites

You need:
- Python 3.11 or higher (`python --version` to check)
- `git`
- A rotated Anthropic API key (do **not** reuse the one you pasted earlier)

---

## Step 1 — Clone the repo and check out the branch

```bash
cd ~                                   # or wherever you keep code
git clone https://github.com/sreme19/dhurandhar-oracle.git
cd dhurandhar-oracle
git checkout claude/redefine-project-objective-ngE54
```

Verify you're on the right branch:

```bash
git branch --show-current
# expected output: claude/redefine-project-objective-ngE54
```

---

## Step 2 — Create a virtual environment (recommended)

```bash
python -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .\.venv\Scripts\activate         # Windows PowerShell
```

You should see `(.venv)` at the start of your prompt.

---

## Step 3 — Install the package

```bash
pip install -e ".[dev]"
```

This takes ~30 seconds. Last line should look like
`Successfully installed dhurandhar-oracle-0.1.0 ...`.

Verify the CLI is on PATH:

```bash
dhurandhar-oracle --help
```

You should see a list of commands including `run`, `project-forward`,
`rewrite-arc`, `suggest`.

---

## Step 4 — Run the unit tests (no API key needed)

```bash
python -m pytest tests/test_career_mdp.py tests/test_forward_pipeline.py -v
```

Expected: **8 passed**. If anything fails, stop and tell me.

---

## Step 5 — Smoke-test without an API key

The app falls back to a template narrative when `ANTHROPIC_API_KEY` isn't
set. This confirms the solver pipelines work end-to-end before we wire in
Claude.

```bash
dhurandhar-oracle suggest --mode forward
dhurandhar-oracle project-forward hamza --no-narrative
```

You should see a ranked operative table (suggest) and a trajectory
comparison table with `Δ score: +1.70` for Hamza.

---

## Step 6 — Set the rotated API key

For **just this terminal session** (forgotten when you close the
terminal — safest for testing):

```bash
export ANTHROPIC_API_KEY="sk-ant-…paste-your-rotated-key…"
```

Verify it's set without echoing the key itself:

```bash
[ -n "$ANTHROPIC_API_KEY" ] && echo "set, length $(printf %s "$ANTHROPIC_API_KEY" | wc -c)" || echo "not set"
```

You should see e.g. `set, length 108`.

If you want it persistent across terminals, add the same `export` line
to `~/.zshrc` (zsh, default on macOS) or `~/.bashrc` (bash on Linux),
then `source ~/.zshrc`. Don't put the key into the repo.

---

## Step 7 — Run the live forward-projection on Hamza

This is the LinkedIn-grade narrative.

```bash
dhurandhar-oracle project-forward hamza --markdown
```

Expected runtime: ~10–15 seconds (one Sonnet 4.6 call).
Expected output: trajectory comparison table + a Markdown-formatted
strategic brief in a Rich panel.

To capture just the Markdown body for pasting into LinkedIn:

```bash
dhurandhar-oracle project-forward hamza --markdown --json \
  | python -c "import sys, json; print(json.load(sys.stdin)['narrative'])"
```

---

## Step 8 — Try the other operatives

```bash
dhurandhar-oracle project-forward rizwan_shah --markdown
dhurandhar-oracle project-forward ajay_sanyal --markdown
dhurandhar-oracle project-forward ks_bhullar  --markdown
dhurandhar-oracle project-forward sushant_bansal --markdown
dhurandhar-oracle project-forward dgp_prashant_kumar --markdown   # speculative banner
```

---

## Step 9 — Counterfactual rewrite-arc on Hamza

This one is slow (~90 seconds — runs the POMDP solver once per
turning point across all 18 of Hamza's TPs).

```bash
dhurandhar-oracle rewrite-arc hamza --markdown
```

Expected output: per-TP Q-delta table + Markdown-formatted rewrite
narrative. Cumulative ΔQ should be around +29 with `mission_yield Δ ≈ +3.0`.

---

## Step 10 — Optional flags worth knowing

```bash
# Shorter narrative via Haiku
dhurandhar-oracle project-forward hamza --markdown --brief

# Cap the horizon
dhurandhar-oracle project-forward hamza --until 2026-02-28 --markdown

# Force one event's prescribed action (counterfactual exploration)
dhurandhar-oracle project-forward hamza \
  --force-event-response e4_pahalgam_massacre:accept_extraction_to_india \
  --markdown

# Same idea for rewrite-arc
dhurandhar-oracle rewrite-arc hamza \
  --force-tp dakait-first-meeting:accelerate_dakait_trust \
  --markdown

# Raw JSON output for either mode
dhurandhar-oracle project-forward hamza --json | jq .forward_projection.scalar_score_delta
```

---

## Step 11 — When you're done

Deactivate the virtual environment:

```bash
deactivate
```

If you set the key only via `export` (Step 6 short-form), it's already
gone — the key dies with the terminal session.

---

## If something breaks

Tell me which step number failed and paste the last 10–20 lines of
output. The likely culprits are:

- **Step 3 install fails on `langgraph`** → upgrade pip first:
  `pip install --upgrade pip` then retry Step 3.
- **Step 4 tests fail** → unexpected; paste the failure output.
- **Step 7 returns "ANTHROPIC_API_KEY not set" warning** → Step 6 didn't
  take effect. Re-run the verify command in Step 6.
- **Step 7 returns 401 / authentication error** → key is wrong or not
  rotated. Re-rotate.
- **Step 7 hangs > 60 seconds** → network blocking, kill with Ctrl-C and
  check connectivity to api.anthropic.com.
