# dhurandhar-oracle Handoff

## 1) Pull latest code

```bash
cd /Users/performek5/Desktop/Code/dhurandhar-oracle
git fetch origin
git checkout main
git pull origin main
```

## 2) Verify Python

Project requires Python 3.11+.

```bash
python --version
```

## 3) Install dependencies before running tests

```bash
pip install -e ".[dev]"
```

If you skip this step, tests can fail with:

- `ModuleNotFoundError: No module named 'langgraph'`

## 4) Run tests

```bash
pytest tests
```

Expected result after install: tests pass.

To skip slow tests:

```bash
pytest tests -m "not slow"
```

## 5) CLI smoke test without API key

```bash
dhurandhar-oracle project-forward hamza --markdown
```

## 6) Run with API key for full output

```bash
export ANTHROPIC_API_KEY="<your-rotated-key>"
dhurandhar-oracle project-forward hamza --markdown
dhurandhar-oracle rewrite-arc hamza --markdown
```

`rewrite-arc` may take around 90 seconds.

## 7) Troubleshooting

- If `langgraph` import fails after install:
  - confirm interpreter alignment:
    - `which python`
    - `which pytest`
  - ensure both point to the environment where `pip install -e ".[dev]"` was run.
- If you need fast validation only:
  - `pytest tests -m "not slow"`
