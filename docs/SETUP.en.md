# Setup on another computer

[Русский](SETUP.md) | **English**

## Viewing and checking without a board

Copy the entire folder and open a terminal at its root. File checks require Python 3.11+ and the standard library; no extra pip packages are needed.

The author's board already operates on the machine and has passed tests without observed heating. The following describes preparing another computer and connecting another unit, not an unfinished startup of the author's machine.

```powershell
py -3 --version
py -3 tools/check_project.py
py -3 tools/sigma/inspect_project.py
py -3 -m unittest discover -s tools/meter -p "test_*.py" -v
```

`inspect_project.py` prints JSON with block names, tables and constants. Another copy can be specified:

```powershell
py -3 tools/sigma/inspect_project.py "проект_сигма/Design1_parker_transfer_2026-10-27.dspproj"
```

The scripts find the root from their own location. Run the relative commands above from the package root. On Linux/macOS, use `python3` for offline commands.

## Environment for connecting hardware

| Component | Purpose |
| --- | --- |
| Windows | SigmaStudio and direct USB/HID access from the multimeter utility |
| Analog Devices SigmaStudio 4.7 | Version used for the original work; other versions were not tested here |
| USBi / compatible programmer and driver | ADAU1701 connection; check the exact model and pinout against your hardware |
| Python 3.11+, preferably x64 | Checks, meter reading and API client |
| .NET Framework 4.x with `csc.exe` | Optional local build of the official SigmaStudio API bridge |
| PDF viewer / Gerber viewer | Viewing the schematic and board manufacturing files |

Install software and drivers separately from their manufacturers. This package contains no installers, commercial DLLs or UNI-T application. The independent HID polling does not need UNI-T application DLLs.

The author excluded DipTrace source files and libraries; DipTrace is not needed for the current package.

## Opening the project

Open `проект_сигма/Design1_parker_v0.dspproj` in SigmaStudio. Keep its name: compiler-directory names depend on it. If a particular installation cannot handle a Cyrillic path, move a working copy to a compatible path and update tool paths consistently.

Check `IC 1`, the 96 kHz sample rate, hardware connections and the indicators `ADC0_RAW`, `VIN_FILTERED`, `VIN_MEAS_0_1`, `ADC1_RAW`, `I_MEAS_0_1`. Review the current schematic and [limitations](STATUS.en.md) before downloading.

On a prepared bench, **Action → Link Compile Download (F7)** compiles the project and downloads DSP RAM. This can change coil current. Perform it after checking the load, zero command and absence of the X3–X4 jumper. RAM contents disappear when power is removed; EEPROM files alone do not prove that this version is stored in EEPROM.

Continuous indicator reading: Ctrl+F11 enables it; Ctrl+F12 disables it. Disable continuous indicators before batch API reads so they do not compete for the capture register.

## Multimeter

The verified instrument is a UNI-T UT61D+ with a CH9329 HID adapter. From the package root:

```powershell
.\tools\meter\meter.ps1 --list
.\tools\meter\meter.ps1 --count 1
.\tools\meter\meter.ps1 --count 0 --interval 1 --latest output/meter/latest.json --log output/meter/readings.jsonl
```

The last command runs until Ctrl+C. The launcher chooses `PROPVALVE_PYTHON`, then `py -3`, then `python`. Specify your executable if needed:

```powershell
$env:PROPVALVE_PYTHON = 'D:\Python311\python.exe'
```

Instead of the PowerShell script, run `py -3 tools/meter/read_meter.py` with the same arguments. If multiple adapters are found, select `--path` from a fresh `--list`. The utility does not change measurement mode: select DC V / DC A and connect the probes on the instrument. For `CP2110`, it also sets temporary UART parameters; that transport was not tested on the original bench.

Check JSON freshness, units and flags. Do not use measurements for calibration with `HOLD`, `REL`, `MIN/MAX`, `PEAK`, overload or low battery. If the manufacturer application interferes, stop its polling. [Protocol description](../tools/meter/ИНСТРУКЦИЯ.en.txt).

## Optional SigmaStudio automation

Build the bridge from source; no ready-made EXE is supplied. It uses DLLs from the installed SigmaStudio. A standard 4.7 installation is detected automatically; for another directory, set the variable **in the same terminal used to run the bridge**:

```powershell
$env:SIGMASTUDIO_DIR = 'C:\Program Files\Analog Devices\SigmaStudio 4.7'
.\tools\sigma\build_bridge.ps1
.\tools\bin\SigmaBridge2.exe inspect
```

`inspect` lists available types and methods without creating a server object. It checks DLL availability, not DSP communication. `call` requires SigmaStudio running with the required project and its automation server available. Obtain method names from the installed version: some API names contain `SAFELAOD`.

`tools/sigma/sigma_api.py` uses the local `tools/bin/SigmaBridge2.exe`. Set `PROPVALVE_SIGMA_BRIDGE` if another EXE is needed. Set `PROPVALVE_COMPILED_DIR` to the compiler-output folder containing `trap.dat` directly. The default is `проект_сигма/IC 1_Design1_parker_v0/net_list_out2`.

Before reading a particular node, obtain a fresh `trap.dat` from the project actually loaded into the DSP. `capture_node.sample_node` selects the capture-register point by writing 2074, then reads values. This helper does not independently verify that RAM matches the map.

`call` exposes the general API, including parameter changes, schematic edits and DSP downloads. The getting-started instructions deliberately contain no automatic coil-run command: older scripts need adaptation to the particular bench and current project.

## Starting an AI conversation

Open this folder as the working directory and send:

> Read AGENTS.en.md, README.en.md and docs/STATUS.en.md. Check package completeness and the saved project without accessing hardware. Then help with this task: [description]. Tell me what information about my bench is needed for the next step.

This starting point does not depend on previous chat history or access to the author's accounts.
