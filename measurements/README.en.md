# Measurements

[Русский](README.md) | English

`2026-10-27/` contains unchanged records from the original `output/meter/`. The final series are `output_calibration_verification.json`, `feedback_final_verification.json` and `voltage_input_verify.json`. Intermediate series are also retained for reproducibility, including results before corrections and without limiters.

Every file here is historical. Old reception timestamps, HWND/PID, window parameters and values refer to the calibration bench. Individual channels were calibrated before the final control-path integration. In a later message on 31 October 2026, the author confirmed that the board was operating on the machine, had passed testing and was not heating up. The older series remain as original calibration data.

Write current logs to `output/` (excluded from Git), then transfer a confirmed series to a separate dated directory with a description of the board, load, connections, project version and measurement conditions. Do not overwrite original series.

## Reading the records in English

JSON/JSONL keys, block identifiers, quantities and units are retained because they are also consumed by tools. The [multimeter protocol guide](../tools/meter/ИНСТРУКЦИЯ.en.md) explains `quantity`, `volts`, `amps`, `received_unix`, `checksum_valid` and `calibration_usable`. The [English calibration reports](../проект_сигма/README.en.md#english-calibration-records) translate the experiment conditions, table meanings and numeric verification results. `docs/STATUS.en.md` distinguishes command error, DSP-versus-meter difference and unsupported claims of absolute accuracy.
