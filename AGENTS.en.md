# Instructions for an AI assistant

[Русский](AGENTS.md) | **English**

## Purpose and sources

This is a remote control-board project for Parker RE06M*T using ADAU1701. It processes DC signals; usual assumptions about audio paths, AC coupling and DC removal do not apply. The TL494 analog loop regulates current; no digital PID is implemented.

The author confirmed the current operational status on 31.10.2026: **the board already operates on the machine, has passed tests and shows no observed heating**. Do not repeat the old conclusion that the integrated system is still untested. This describes a working unit; numerical temperatures and test conditions were not provided and must not be invented.

Start by reading `README.en.md`, `docs/STATUS.en.md`, `docs/SETUP.en.md`, `схема_плата/README.en.md`, then the task-specific materials. All paths below are relative to the repository root. Do not reuse absolute paths, usernames, HWND, PID or coordinates from an older session.

Working project: `проект_сигма/Design1_parker_v0.dspproj`. Snapshot: `Design1_parker_transfer_2026-10-27.dspproj`. During package preparation their SHA256 hashes matched:
`68473e7fcdd412021ea5be6c9a44e739b82610bf1e1b24db6d04dc68e22826e7`.
`*_io_calibrated`, `*_current_calibrated`, `*before*` and `*preliminary*` belong to earlier stages.

Schematic: `схема_плата/схема.pdf`. The current PDF already shows R42/R43 as 10 kΩ; XLSX and photos retain the older 180 Ω values. DA7.2 carries the author's “ошибка” (“error”) annotation, and the photo shows wire rework near DA7. These are notes for reproduction from the materials, not a claim that the operating board is faulty. The author excluded `.dip`, `.dch`, DipTrace libraries and the duplicate Gerber ZIP. Do not restore them from a neighboring original folder without an assigned task. The package includes PDF, unpacked Gerber and XLSX. Enclosure photo: `корпус/RUICHI A09.jpg`.

The historical description in `archive/НАЧАТЬ_ЗДЕСЬ_ПЕРЕНОС_ПРОЕКТА.txt` is useful context; an English companion is alongside it. Its old paths, CAD-file inventory, suggestion that the PDF might still show 180 Ω and pending-test status have been clarified by newer documents and the author's report. Hardware permissions from previous sessions do not transfer to another bench.

## Initial checks without hardware

```powershell
py -3 tools/check_project.py
py -3 tools/sigma/inspect_project.py
py -3 -m unittest discover -s tools/meter -p "test_*.py" -v
```

These commands do not access USB or SigmaStudio. Python 3.11+ and the standard library are sufficient. If `py` is unavailable, use a suitable `python`/`python3` and check its version. `check_project.py` compares the package to the delivery manifest and the tables to the saved project; it is not a hardware test.

For `.dspproj`, use the data-only parser `tools/sigma/nrbf_project.py`. It supports the NRBF subset found in this project. Do not load the file through .NET BinaryFormatter for analysis. Investigate an unsupported record explicitly; do not bypass errors by deserializing executable objects.

## Saved-project invariants

- SigmaStudio 4.7, Fs = 96 kHz; the DSP is `IC 1`, EEPROM is `IC 2`.
- X4 / ADC0: 0–10 V → `VIN_LPF_20Hz` → `VIN_TABLE_0_10V` → `VIN_LIMIT_MIN/MAX` → 0–1 command.
- Command → `CURRENT_0_3A` → `ZERO_OFF` → DAC0; through enabled `Inv1` → DAC1.
- `ZERO_CONSTANT=0`. The nonzero first table coefficient compensates analog offset. A separate `ZERO_OFF` handles switch-off at zero.
- ADC1 → `CURRENT_LPF_20Hz` → `FB_LIMIT_MIN/MAX` (−0.78 / +0.70) → `I_FEEDBACK_0_1` → `Interpolator1` → DAC3 → X3.
- `DC2_3=0` drives DAC2. Negative `Interpolator1` coefficients are correct for the output-stage polarity.
- `VIN_MEAS_0_1 × 10` is input volts; `I_MEAS_0_1 × 3` is actual amperes. X3 represents actual current, not a copy of the command.
- Manual sources `CURRENT_INPUT_0_1` and `DC2_4` have been removed from the working version. Old scripts referring to them require adaptation.
- R42 = R43 = 10 kΩ for the current tables. Coefficients are specific to the measured board.

## Bench work

First establish the actual valve variant, permissible coil current, connections and power state. The 3 A scale comes from the previous bench, not a universal limit for this valve series. Before a loaded run, verify the absence of the X3–X4 calibration jumper: it creates positive feedback in the final circuit.

Carry out work already agreed with the user without repeatedly asking. If the task is limited to file analysis, do not energize the load, download the DSP or write EEPROM. Establish missing information about the connected load before actions that change its current. Do not treat DSP clamps as hardware overcurrent protection.

The disk file, DSP RAM and EEPROM are three different states. The 27.10.2026 calibration log says EEPROM was not written then. The author later confirmed operation on the machine but did not separately report current EEPROM contents. Do not present the old EEPROM note as an established fact about current operation. For another unit, verify the code being downloaded; `archive/eeprom-unverified/` is not ready-to-use verified firmware.

Before using the API, build the bridge as described in `docs/SETUP.en.md`. `SIGMASTUDIO_DIR` specifies the installed environment; the EXE is built locally in `tools/bin/`. The API can change the schematic and hardware parameters: check methods and arguments first. `capture_node.sample_node` also writes, selecting the capture-register node, although it does not change the current command.

After changing the schematic, recompile and verify consistency with the loaded project. `trap.dat` and `spi_map.dat` must come from that compilation: addresses and program counters are not fixed. Saved maps are historical material, not proof of current addresses. Disable GUI continuous readback (Ctrl+F12) before batch capture; Ctrl+F11 restores indicators. Standard F7 in SigmaStudio on a prepared bench is the verified way to refresh their binding.

Readback: 3 bytes, signed 5.19, divisor 524288. Control parameters are usually 5.23; do not confuse the formats. Capture used 2074 (0x081A); 2075 produced timeouts.

Multimeter: UNI-T UT61D+, tested CH9329 transport `1A86:E429`. CP2110 is implemented but was not tested on the original bench. For calibration, acquire a fresh measurement with `ok`, `checksum_valid`, `calibration_usable`; check `quantity`, mode, units and `received_unix` (guideline: no more than 3 s old). An old JSON file is not a live reading. Current mode needs the series current input; voltage mode needs a parallel V/COM connection.

## Changes and reporting

Do not run `archive/legacy-tools/` as a batch or import its modules: many execute actions immediately on import. They contain one-off scripts with obsolete windows, block names and commands up to 3 A/10 V. Read and adapt the required fragment to the current task first.

Preserve original captures and historical measurements. Put new logs in ignored `output/` and intermediates in `tmp/`. For a newly confirmed result, create a separate dated directory under `measurements/` and describe the configuration. Do not overwrite original records with calculated results.

After Python edits, run the relevant offline checks. For `.dspproj` changes, additionally check tables, constants, connections and a fresh netlist. Parser validation does not replace compilation checks and tests. State exactly what was checked: file, compilation, RAM, EEPROM, current or hydraulics.

`docs/manifest.json` contains checksums of the prepared package version. `docs/INVENTORY.en.md` records inventory history. Mismatches during development are expected; do not automatically update the manifest to conceal changes. First review the diff and document the new version. Do not publish the repository or send materials externally without a user task.
