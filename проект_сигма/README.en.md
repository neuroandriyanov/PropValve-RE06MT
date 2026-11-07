# SigmaStudio projects

[Русский](README.md) | **English**

Calibration reports: [0–10 V input](Калибровка_входа_0_10В_2026-10-27.en.txt) · [current](Калибровка_тока_2026-10-27.en.txt) · [current before replacing R43](Калибровка_тока_до_замены_R43.en.txt). Russian originals are linked from the Russian page.

Open `Design1_parker_v0.dspproj`. It contains the integrated working path for the external command and actual-current monitoring. `Design1_parker_transfer_2026-10-27.dspproj` was an identical snapshot when the package was prepared.

`Design1_parker_io_calibrated.dspproj` contains all individual calibrations but predates the final rewiring. Other `calibrated`, `preliminary` and `before*` copies are retained for history and comparison. Older text reports likewise describe their respective stages and may mention manual sources that were removed later. English translations of the calibration reports use the `.en.txt` suffix next to their Russian originals.

`IC 1_Design1_parker_v0/` contains saved compiler outputs. They are useful for analyzing connections, but live address reads require a fresh compilation of the exact project loaded into the DSP. Renaming the `.dspproj` changes compiler-output paths.

TXT tables contain only values at uniformly spaced nodes. Obtain Min/Max, filters, conditions, branches and constants from the `.dspproj` and JSON. Do not replace negative output coefficients with positive ones or truncate the input table to 0…1: separate blocks clamp the normalized signal.

Check without SigmaStudio: run `py -3 tools/sigma/inspect_project.py` from the package root. Main instructions and status: [README](../README.en.md), [SETUP](../docs/SETUP.en.md), [STATUS](../docs/STATUS.en.md).
