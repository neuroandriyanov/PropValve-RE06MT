# Measurements

[Русский](README.md) | **English**

`2026-10-27/` contains unchanged records from the original `output/meter/`. Final series: `output_calibration_verification.json`, `feedback_final_verification.json`, `voltage_input_verify.json`. Intermediate series are also retained for reproducibility, including results before corrections and without clamps.

All files here are historical. Old acquisition times, HWND/PID, window parameters and values refer to the calibration bench. Individual channels were calibrated before the last integration of the control path. Later, in a message dated 31.10.2026, the author confirmed that the board was already operating on the machine, had passed tests and was not heating up. These older series are retained as original calibration data.

Write current logs to `output/` (excluded from Git), then transfer a confirmed series to a separate dated directory with a description of the board, load, connections, project version and measurement conditions. Do not overwrite the original series.
