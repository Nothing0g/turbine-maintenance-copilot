# Debugging note: timestamp-window boundary bug

## Symptom

The first diagnosis prototype classified the degraded LP bearing as `insufficient_data` when the requested window was exactly 24 hours. The CSV contained the boundary observation, but the service returned one fewer observation than expected.

## Root cause

The prototype used a half-open interval:

```python
window = asset[(asset["timestamp"] >= start) & (asset["timestamp"] < end)]
```

That is often correct for interval joins, but it was incorrect for this endpoint because `hours=24` means “include the latest observation and the 24-hour boundary.” The final sample was discarded before the anomaly scorer ran.

## Fix

The final implementation uses an inclusive upper bound:

```python
window = asset[(asset["timestamp"] >= start) & (asset["timestamp"] <= end)]
```

The regression test retained in the project checks the user-visible result rather than only the internal row count: the degraded asset must reach `review_required`, and the healthy asset must remain `normal`.

## Lesson

Time-window semantics need to be part of the API contract. A timestamp filter can silently change model behavior even when the model itself is unchanged.
