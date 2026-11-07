# Setup on another computer

[Русский](SETUP.md) | English

## Viewing and checking without a board

Copy the entire directory and open a terminal at its root. File checks require Python 3.11+ and its standard library; no additional pip packages are needed.

The author's board is already operating on a machine and has passed tests without observed heating. The instructions below prepare another computer and connect another unit; they do not describe an unfinished commissioning of the author's machine.

```powershell
py -3 --version
py -3 tools/check_project.py
py -3 tools/sigma/inspect_project.py
py -3 -m unittest discover -s tools/meter -p "test_*.py" -v
```

`inspect_project.py` prints JSON containing block names, tables and constants. Another copy can be specified:

```powershell
py -3 tools/sigma/inspect_project.py "проект_сигма/Design1_parker_transfer_2026-10-27.dspproj"
```

The scripts locate the root from their own location. Run the relative commands above from the package root. On Linux/macOS, use `python3` for offline commands.

## Connection environment

| Component | Purpose |
| --- | --- |
| Windows | SigmaStudio and direct USB/HID access from the multimeter utility |
| Analog Devices SigmaStudio 4.7 | Version used for the original work; other versions have not been tested here |
| USBi / compatible programmer and driver | ADAU1701 connection; check the actual model and pinout against your equipment |
| Python 3.11+, preferably x64 | Checks, meter reading and API client |
| .NET Framework 4.x with `csc.exe` | Optional: local build of the native SigmaStudio API bridge |
| PDF viewer / Gerber viewer | Schematic and PCB manufacturing-file inspection |

Install programs and drivers separately from their manufacturers' sources. The package does not include installers, commercial DLLs or the UNI-T program. The custom HID reader does not need UNI-T program DLLs.

DipTrace sources and libraries were excluded by the author; DipTrace is not needed to use this package.

## Opening the project

Open `проект_сигма/Design1_parker_v0.dspproj` in SigmaStudio. Keep its name: compiler-directory names depend on it. If a particular installation cannot handle Cyrillic paths, move a working copy to a compatible path and update the tool paths consistently.

Check `IC 1`, the 96 kHz sample rate, hardware connections and the readbacks `ADC0_RAW`, `VIN_FILTERED`, `VIN_MEAS_0_1`, `ADC1_RAW` and `I_MEAS_0_1`. Check the current schematic and [limitations](STATUS.en.md) before downloading.

On a prepared bench, the native **Action → Link Compile Download (F7)** command compiles the project and loads DSP RAM. This can change coil current. Perform it after checking the load, zero command and absence of the X3–X4 jumper. RAM contents are lost when power is removed; the presence of EEPROM files does not prove that this version has been written to EEPROM.

Continuous readback: Ctrl+F11 enables it, Ctrl+F12 disables it. Disable continuous controls before batch API reading so that they do not compete for the capture register.

## Multimeter

The tested instrument is a UNI-T UT61D+ with a CH9329 HID adapter. From the package root:

```powershell
.\tools\meter\meter.ps1 --list
.\tools\meter\meter.ps1 --count 1
.\tools\meter\meter.ps1 --count 0 --interval 1 --latest output/meter/latest.json --log output/meter/readings.jsonl
```

The last command runs until Ctrl+C. The launcher selects `PROPVALVE_PYTHON`, then `py -3`, then `python`. Specify your executable if needed:

```powershell
$env:PROPVALVE_PYTHON = 'D:\Python311\python.exe'
```

Instead of the PowerShell script, run `py -3 tools/meter/read_meter.py` with the same arguments. If several adapters are found, choose `--path` from a fresh `--list`. The utility does not switch measurement mode: select DC V / DC A and connect leads on the instrument. For `CP2110`, it also sets temporary UART parameters; that transport was not tested on the original bench.

Check freshness, units and JSON flags. Do not use readings for calibration when `HOLD`, `REL`, `MIN/MAX`, `PEAK`, overload or low battery is active. If the vendor application interferes with polling, stop its polling. See the [protocol description](../tools/meter/ИНСТРУКЦИЯ.en.md).

## Optional SigmaStudio automation

The bridge is built from source; the package has no ready-made EXE. It uses DLLs from the installed SigmaStudio. A standard 4.7 installation is detected automatically; for another directory, set the variable **in the terminal from which the bridge will be used**:

```powershell
$env:SIGMASTUDIO_DIR = 'C:\Program Files\Analog Devices\SigmaStudio 4.7'
.\tools\sigma\build_bridge.ps1
.\tools\bin\SigmaBridge2.exe inspect
```

`inspect` lists available types and methods without creating a server object. It checks DLL availability, not a DSP connection. `call` requires a running SigmaStudio instance with the intended project and an available native automation server. Obtain the method list from the installed version: some API names contain `SAFELAOD`.

`tools/sigma/sigma_api.py` uses local `tools/bin/SigmaBridge2.exe`. Set `PROPVALVE_SIGMA_BRIDGE` for another EXE if necessary. `PROPVALVE_COMPILED_DIR` can specify the compilation-output directory (the directory directly containing `trap.dat`). Its default is `проект_сигма/IC 1_Design1_parker_v0/net_list_out2`.

Before reading a specific point, obtain a fresh `trap.dat` from the project actually loaded in the DSP. `capture_node.sample_node` selects the capture-register point by writing 2074, then reads the values. This helper does not independently verify that RAM and the map match.

`call` is a general API, including parameter changes, schematic changes and DSP loading. These getting-started instructions contain no automatic coil-sweep command: old scripts require adaptation to the particular bench and current project.

## Starting an AI chat

Open this folder as the working directory and send:

> Read AGENTS.md, its English companion, README.en.md and docs/STATUS.en.md. Check package completeness and the saved project without accessing hardware. Then help with this task: [description]. Tell me which details of my bench are needed for the next step.

This starting point does not depend on an earlier chat history or access to the author's accounts.
