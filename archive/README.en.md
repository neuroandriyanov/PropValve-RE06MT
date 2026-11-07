# Historical materials

[Русский](README.md) | **English**

`НАЧАТЬ_ЗДЕСЬ_ПЕРЕНОС_ПРОЕКТА.txt` is preserved unchanged. It describes the original working folder as of 27.10.2026. An [English translation](НАЧАТЬ_ЗДЕСЬ_ПЕРЕНОС_ПРОЕКТА.en.txt) is available. Its `output/meter` paths correspond to the current `measurements/2026-10-27`; current instructions are in `docs/SETUP.en.md` and `AGENTS.en.md`. Schematic and photo corrections are recorded in `docs/STATUS.en.md`.

The old log's pending-test status is obsolete: on 31.10.2026, the author confirmed that the board was operating on the machine, had passed tests and showed no observed heating. DipTrace and library references also describe the original folder; the author excluded them from the current package.

`legacy-tools/` contains the original Python/C#/PowerShell files from the old toolset. They were archived without adaptation and **are not a ready-to-run package**: relative paths after transfer, HWND/PID, parameter addresses, block names and hardware state may differ. Some modules write immediately when imported. Study the code as history and adapt each required operation separately. Portable active helpers are in the root `tools/` folder.

`eeprom-unverified/` contains the original `E2Prom.bin` and `E2Prom.Hex`. Their correspondence to the final project and actual EEPROM has not been established. They are not presented as verified, ready-to-use firmware.
