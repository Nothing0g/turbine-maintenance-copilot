# Synthetic maintenance evidence

## PROC-LUBE-001 | Bearing lubrication inspection
Inspect lubrication flow, oil pressure, filter differential pressure, and bearing temperature sensor connections when a bearing temperature trend moves outside its recent operating envelope. Do not return equipment to normal service until the cause is reviewed by an authorized maintenance engineer.

## PROC-VIB-002 | Vibration cross-check
Use vibration readings as a supporting signal for rotating-equipment diagnosis. A temperature-only anomaly should be treated as a review trigger, not as proof of mechanical failure. Check sensor health and compare against the last accepted baseline.

## PROC-DATA-003 | Historian data quality
Before using telemetry for maintenance inference, verify timestamp ordering, expected units, duplicate records, null values, and data freshness. If required channels are missing or stale, abstain and request a data-quality check.

## WORK-2026-014 | Synthetic prior work order
A previous LP bearing review found elevated temperature alongside reduced lubrication flow. The work order outcome was filter inspection and sensor verification. This synthetic record is included to test evidence retrieval and must not be treated as a plant instruction.
