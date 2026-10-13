# Verification record

The final branch was verified locally with:

```bash
python scripts/generate_demo_data.py
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python scripts/run_evaluation.py
```

The historical failure is preserved in [`reports/debug/timestamp-window-failure.txt`](../reports/debug/timestamp-window-failure.txt). It comes from commit `67882c0`, where the diagnosis window used a strict `< end` boundary. The fix is in commit `ce2f441`, where the endpoint uses `<= end` and the regression test remains in the final branch.
