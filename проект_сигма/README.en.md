# SigmaStudio projects

[Русский](README.md) | English

Open `Design1_parker_v0.dspproj`. It contains the combined working path for an external command and actual-current monitoring. `Design1_parker_transfer_2026-10-27.dspproj` is the identical snapshot made during package preparation.

`Design1_parker_io_calibrated.dspproj` contains all individual calibrations but predates the final reconnections. Other `calibrated`, `preliminary` and `before*` copies are retained for history and comparison. The older text reports likewise describe their own stage; they may refer to manual sources that were later removed.

`IC 1_Design1_parker_v0/` contains saved compilation output. It is useful for connection analysis, but live address reads require a new compilation of the exact project loaded in the DSP. Renaming a `.dspproj` changes compiler-output paths.

The TXT tables contain only the values of evenly spaced knots. Obtain Min/Max, filters, conditions, branches and constants from `.dspproj` and JSON. Do not replace negative output coefficients with positive ones or truncate the input table to 0…1: separate blocks limit the normalized signal.

Offline check without SigmaStudio: `py -3 tools/sigma/inspect_project.py` from the package root. Main instructions and status: [README](../README.en.md), [SETUP](../docs/SETUP.en.md), [STATUS](../docs/STATUS.en.md).

## English calibration records

These are translations of historical records, not new measurements or instructions to energize a bench:

- [Current calibration before replacing R43](Калибровка_тока_до_замены_R43.en.md).
- [Current and feedback calibration, 27 October 2026](Калибровка_тока_2026-10-27.en.md).
- [0–10 V input calibration, 27 October 2026](Калибровка_входа_0_10В_2026-10-27.en.md).

The numerical TXT coefficient exports are language-neutral and remain unchanged. File paths, block names and protocol identifiers remain identical in both language versions.
