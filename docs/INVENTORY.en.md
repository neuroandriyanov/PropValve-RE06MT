# Original-folder review and package contents

[Русский](INVENTORY.md) | **English**

All original directories were accounted for. Documentation and logs were read; both PDF schematic sheets were visually reviewed; the valve datasheet was extracted and its electrical-data/connection pages checked; photographs were inspected. All ten `.dspproj` files were parsed as data, including tables, constants and the working version's saved netlist. Tool source was reviewed for dependencies, paths and control operations. BOM data was read from XLSX; that file was not edited.

The current package retains the PDF schematic, Gerber/drill files and BOM; DipTrace source and libraries were excluded by the author. End-cap models were preserved without editing or full verification in a 3D editor. Gerber geometry was not compared to CAD. The assistant did not operate hardware during the file review; the author separately confirmed successful tests and operation on the machine without observed board heating.

| Original directory | Contents and decision |
| --- | --- |
| `фото/` | Four JPGs copied completely and byte for byte: both board sides, enclosure on the machine, and board in its enclosure |
| `doc/` | Six-page Parker RE06M*T PDF copied |
| `схема_плата/` | PDF, XLSX and 9 Gerber/drill files retained. DipTrace, libraries and duplicate ZIP removed from the package by the author |
| `проект_сигма/` | Ten projects, TXT/JSON and compiler outputs retained. Two EEPROM images moved to the archive |
| `корпус/` | `.m3d`, `.stl`, `.lxcf` retained; `RUICHI A09.jpg` image and README added |
| `tools/` | Original scripts retained in `archive/legacy-tools/`. A small separate starter toolset prepared in `tools/` |
| `output/meter/` | JSON/JSONL records moved to `measurements/2026-10-27/`; `latest.json`, window captures and their metadata excluded |
| `tmp/` | Temporary captures, crops, API arguments and diagnostic results excluded |
| `программа_мультиметра/` | Third-party application, DLLs, runtime installer and GUI manuals excluded; independent HID polling does not depend on them |
| Root transfer file | Original retained in `archive/`; new instructions are in README/AGENTS/docs |

## Repeat review on 31.10.2026, package version 2

After initial preparation, the author clarified that the board already operated on the machine, had passed tests and was not heating up. This status was added to README, AGENTS and documentation; the previous pending-test item for the integrated path was removed. Old records remain unchanged as calibration history.

Comparison with the previous manifest before the update showed that the author had removed **54 files**, all under `схема_плата/`: 7 `.dip`, 1 `.dch`, 23 `.eli`, 22 `.lib` and 1 `.zip`. Other files were unchanged at comparison time. The removals were preserved; sources were not restored from a neighboring working folder.

`корпус/RUICHI A09.jpg` was found in the original folder, inspected and copied byte for byte into the package. It was included in README. The XLSX BOM remained in the schematic folder and was preserved.

## Installation photographs on 02.11.2026, package version 4

Two inspected photos were added from the original `фото/` folder: `Корпус.jpg` → `фото/Корпус_на_машине.jpg` and `плата_в_корасе.jpg` → `фото/Плата_в_корпусе.jpg`. Image bytes were preserved; copy names were clarified for convenience. README gained images captioned “Control unit enclosure installed on the machine” and “Control board in its enclosure with the lid open”; enclosure documentation gained links to them.

Before editing, GitHub commits through `b774e7c` were fetched: the author's README, `LICENSE`, `LICENSES/CERN-OHL-P-2.0.txt` and updated NOTICE changes were preserved. Version 3 of the manifest already differed from README and NOTICE after those edits; version 4 incorporates them, the added licenses, new photos and associated documentation updates. Schematic, Gerber, DSP projects, tools and calibrations were unchanged.

When GitHub was checked on 02.11.2026, the repository was already Public. The obsolete statement that its current status was Private was corrected; access settings were not changed.

## New and adapted files

- `README.md` describes the purpose, moving the board away from heat, the audio-DSP application, signal paths and contents.
- `AGENTS.md` defines how an AI assistant on another computer should learn the project and continue debugging.
- `docs/SETUP.md`, `docs/STATUS.md` and folder explanations distinguish current configuration from history.
- `tools/check_project.py` checks package hashes, project parsing, table/export consistency and basic constants.
- `tools/sigma/inspect_project.py` outputs a structured report on the saved project without hardware access.
- `tools/meter/meter.ps1` selects Python via an environment variable or PATH, without the author's profile.
- `tools/sigma/build_bridge.ps1` builds the official API bridge from C# on the user's computer.
- `SigmaBridge.cs`, `sigma_api.py`, `capture_node.py` use configurable paths. Capture checks the sample count and setup-register failure; checks remain active under Python `-O`.
- `.gitignore` excludes local logs, temporary files, cache and compiled EXE/DLL files. `.gitattributes` preserves original bytes and line endings for SHA256 checks after transfer.

## Checksums

`docs/manifest.json` contains relative paths, sizes and SHA256 hashes for all delivery files except the manifest itself. Files originating in the source folder additionally record their original path, original SHA256 and whether preparation changed them. The author's full profile paths are not recorded.

The manifest fixes package version 4 and is not updated by the checker. Version 2 incorporated the file removals and enclosure image described above. Version 3 added the link to the initially private repository and updated hosting information. Version 4 incorporates installation photographs, licenses and the documentation changes described above. Metadata preserves the preceding manifest's SHA256 and update description. After your own changes, differences from this delivery are expected and require deliberate comparison. Table-consistency checks do not prove every connection or hardware operation correct.

The author designated the [neuroandriyanov/PropValve-RE06MT](https://github.com/neuroandriyanov/PropValve-RE06MT) repository as the destination: initially private, public as of 02.11.2026. The package contains the prepared folder; neighboring original directories are not included in the upload.
