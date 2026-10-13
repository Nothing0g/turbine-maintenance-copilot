# Evaluation protocol

The evaluation is intentionally small but explicit. It is run by `python scripts/run_evaluation.py` and saved to `reports/evaluation.json`.

## Cases

- `LP-BRG-02`: synthetic degradation in the last six hours; expected `review_required`.
- `HP-BRG-01`: stable telemetry; expected `normal`.

## Assertions

- Telemetry quality passes before diagnosis.
- Degraded asset triggers human review.
- Healthy asset is not flagged.
- At least one relevant evidence record is retrieved.
- Structured output contains the required fields.
- Latency is reported.

## Next evaluation improvements

A larger version should include labelled historical windows, false-positive cost, channel dropout, sensor drift, retrieval recall@k, groundedness review by a domain expert, prompt/model regression tests, and load testing for the API.
