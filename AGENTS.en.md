# Instructions for engineering assistants

[Русский](AGENTS.md) | English

## Purpose and sources

This project is a remote ADAU1701 control board for a Parker RE06M*T valve. It processes DC signals; conventional assumptions about audio paths, AC coupling and DC removal do not apply. A TL494 analog loop regulates current; no digital PID is implemented.

The author confirmed the operating status on 31 October 2026: **the board is already working on the machine, has passed tests and shows no observed heating**. Do not repeat the obsolete conclusion that the combined system has not yet been tested. This report concerns one operating unit; numerical temperatures and test conditions were not specified and must not be invented.

At the start, read `README.md`, `docs/STATUS.md`, `docs/SETUP.md`, `схема_плата/README.md` (or their `.en.md` companions), then the material relevant to the task. Paths below are relative to the repository root. Do not reuse absolute paths, usernames, HWNDs, PIDs or coordinates from an earlier session.

Working project: `проект_сигма/Design1_parker_v0.dspproj`. Snapshot: `Design1_parker_transfer_2026-10-27.dspproj`. At packaging, their SHA256 hashes matched:
`68473e7fcdd412021ea5be6c9a44e739b82610bf1e1b24db6d04dc68e22826e7`.
`*_io_calibrated`, `*_current_calibrated`, `*before*` and `*preliminary*` belong to earlier stages.

Schematic: `схема_плата/схема.pdf`. The current PDF already shows R42/R43 as 10 kΩ, while XLSX and photographs retain the old 180 Ω values. DA7.2 bears the author's “error” annotation; a wire modification is visible near DA7 in the photograph. These are reproduction notes, not a claim that the working board is faulty. The author excluded `.dip`, `.dch`, DipTrace libraries and the duplicate Gerber ZIP. Do not restore them from adjacent source directories without a task to do so. The package contains PDF, unpacked Gerber and XLSX. Enclosure image: `корпус/RUICHI A09.jpg`.

The historical description in `archive/НАЧАТЬ_ЗДЕСЬ_ПЕРЕНОС_ПРОЕКТА.txt` provides context. Its old paths, CAD inventory, suggestion that the PDF might still show 180 Ω, and pending-test status are superseded by newer documents and the author's report. Hardware permissions from earlier sessions do not carry over to another bench.

## Initial checks without equipment

```powershell
py -3 tools/check_project.py
py -3 tools/sigma/inspect_project.py
py -3 -m unittest discover -s tools/meter -p "test_*.py" -v
```

These commands do not access USB or SigmaStudio. Python 3.11+ standard library is sufficient. If `py` is absent, use a suitable `python`/`python3` and check its version. `check_project.py` compares the package with its delivery manifest and tables with the saved project; it is not a hardware test.

Use the data-only `tools/sigma/nrbf_project.py` parser for `.dspproj`. It supports the NRBF subset found in this project. Do not use .NET BinaryFormatter to load the file for analysis. Investigate unsupported records explicitly; do not bypass failures by deserializing executable objects.

## Saved-project invariants

- SigmaStudio 4.7, Fs = 96 kHz; DSP is `IC 1`, EEPROM is `IC 2`.
- X4 / ADC0: 0–10 V → `VIN_LPF_20Hz` → `VIN_TABLE_0_10V` → `VIN_LIMIT_MIN/MAX` → command 0–1.
- Command → `CURRENT_0_3A` → `ZERO_OFF` → DAC0; through enabled `Inv1` → DAC1.
- `ZERO_CONSTANT=0`. The nonzero first table coefficient compensates analog offset. A separate `ZERO_OFF` handles zero shutdown.
- ADC1 → `CURRENT_LPF_20Hz` → `FB_LIMIT_MIN/MAX` (−0.78 / +0.70) → `I_FEEDBACK_0_1` → `Interpolator1` → DAC3 → X3.
- `DC2_3=0` drives DAC2. Negative `Interpolator1` coefficients are correct for the output-stage polarity.
- `VIN_MEAS_0_1 × 10` = input volts; `I_MEAS_0_1 × 3` = actual amperes. X3 represents actual current, not a copy of the command.
- Manual sources `CURRENT_INPUT_0_1` and `DC2_4` were removed from the working version. Older scripts addressing them require adaptation.
- R42 = R43 = 10 kΩ for the current tables. Coefficients belong to the measured board.

## Bench work

First establish the actual valve version, permissible coil current, connections and power state. The 3 A scale is a result of the earlier bench, not a universal limit for the valve series. Before a loaded run, confirm that the X3–X4 calibration jumper is absent: in the final circuit it creates positive feedback.

Carry out work already authorized by the user without repeatedly asking the same questions. If the task is file analysis, do not energize a load, load the DSP or write EEPROM. Resolve missing connected-load information before actions that change its current. DSP limiters are not hardware overcurrent protection.

The file on disk, DSP RAM and EEPROM are three different states. The calibration log of 27 October 2026 says EEPROM was not written at that time. The author later confirmed operation on the machine but did not separately report current EEPROM contents. Do not project the earlier EEPROM note onto current operation as an established fact. For another unit, verify the code to be loaded; `archive/eeprom-unverified/` is not ready-made verified firmware.

Before using the API, build the bridge according to `docs/SETUP.en.md`. `SIGMASTUDIO_DIR` specifies the installed environment; EXE is built locally in `tools/bin/`. The API can change the schematic and hardware parameters: inspect the method and arguments first. `capture_node.sample_node` also writes, selecting the capture-register point even though it does not change the current command.

After schematic edits, recompile and check consistency with the loaded project. `trap.dat` and `spi_map.dat` must come from that compilation: addresses and program counters are not constant. Saved maps are historical material, not proof of current addresses. Disable GUI continuous readback (Ctrl+F12) before batch capture; restore readbacks with Ctrl+F11. The tested way to update binding is the native F7 in SigmaStudio on a prepared bench.

Readback: 3 bytes, signed 5.19, divisor 524288. Control parameters generally use 5.23; do not confuse the formats. Capture used 2074 (0x081A); 2075 produced timeouts.

Multimeter: UNI-T UT61D+, tested CH9329 transport `1A86:E429`. CP2110 is implemented but untested on the original bench. For calibration, obtain a fresh reading with `ok`, `checksum_valid` and `calibration_usable`; check `quantity`, mode, units and `received_unix` (guideline: no older than 3 s). Old JSON is not a live reading. Current mode needs a series current input; voltage mode needs a parallel V/COM connection.

## Changes and reporting

Do not batch-run `archive/legacy-tools/` or import its modules: many act immediately on import. It retains one-off scripts with obsolete windows, block names and commands up to 3 A/10 V. Read and adapt the required fragment to the current task first.

Preserve original snapshots and historical measurements. Put new logs in ignored `output/` and temporary files in `tmp/`. For a new confirmed result, create a separate dated `measurements/` directory and describe its configuration. Do not overwrite original records with calculated results.

After Python changes, run relevant offline checks. For `.dspproj` changes, additionally verify tables, constants, connections and a fresh netlist. Parser checks do not replace compilation checks and physical testing. State exactly what was checked: file, compilation, RAM, EEPROM, current or hydraulics.

`docs/manifest.json` records checksums of the current prepared package; `docs/INVENTORY.md` records its history. Differences during development are expected; do not automatically update hashes to hide a change. Review the diff and document the new version first. Do not publish the repository or send materials externally without a user task.
