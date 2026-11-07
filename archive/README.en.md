# Historical materials

[Русский](README.md) | English

`НАЧАТЬ_ЗДЕСЬ_ПЕРЕНОС_ПРОЕКТА.txt` is preserved unchanged. It describes the original working directory as of 27 October 2026; an [English translation](НАЧАТЬ_ЗДЕСЬ_ПЕРЕНОС_ПРОЕКТА.en.md) accompanies it. Its `output/meter` paths now correspond to `measurements/2026-10-27`; current instructions are in `docs/SETUP.md` and `AGENTS.md` (with English companions). Schematic and photograph clarifications are in `docs/STATUS.en.md`.

The old log's pending-test status is obsolete: on 31 October 2026, the author confirmed that the board was operating on the machine, had passed testing and showed no heating. References to DipTrace and libraries also concern the original directory; the author excluded them from the current package.

`legacy-tools/` contains original Python/C#/PowerShell files from the earlier set. They were archived without adaptation and **are not a runnable package**: relocated relative paths, HWND/PID, parameter addresses, block names and hardware state may differ. Some modules write immediately on import. Read the code as history and adapt the required operation separately. Working portable helpers are in the root `tools/` directory.

`eeprom-unverified/` contains the original `E2Prom.bin` and `E2Prom.Hex`. Their correspondence to the final project and actual EEPROM has not been established. They are not presented as verified ready-to-use firmware.
