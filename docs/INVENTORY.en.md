# Original-folder review and package inventory

[Русский](INVENTORY.md) | English

All original directories were accounted for. Documentation and logs were read, both schematic PDF sheets were inspected, the valve specification was extracted and its electrical-data/connection pages checked, and photographs were viewed. All ten `.dspproj` files were parsed as data; tables, constants and the saved netlist of the working version were inspected. Tool sources were checked for dependencies, paths and control operations. BOM data were read from XLSX; the file was not edited.

The current package retains the schematic PDF, Gerber/drill files and BOM; the author excluded DipTrace sources and libraries. Blanking-part models were preserved without editing and without a complete inspection in a 3D editor. Gerber geometry was not compared with CAD. The assistant did not operate hardware during the file review; the author separately confirmed successful testing and board operation on the machine without observed heating.

| Original directory | Contents and decision |
| --- | --- |
| `фото/` | Four JPG files copied completely with identical bytes: both board sides, enclosure on the machine and board inside the enclosure |
| `doc/` | Six-page Parker RE06M*T PDF copied |
| `схема_плата/` | PDF, XLSX and 9 Gerber/drill files retained. The author removed DipTrace, libraries and the duplicate ZIP |
| `проект_сигма/` | Ten projects, TXT/JSON and compilation outputs retained. Two EEPROM images moved to the archive |
| `корпус/` | `.m3d`, `.stl`, `.lxcf` retained; `RUICHI A09.jpg` and README added |
| `tools/` | Original scripts retained in `archive/legacy-tools/`. A small separate getting-started set prepared in `tools/` |
| `output/meter/` | JSON/JSONL records moved to `measurements/2026-10-27/`; `latest.json`, window captures and their metadata excluded |
| `tmp/` | Temporary captures, crops, API arguments and diagnostic output excluded |
| `программа_мультиметра/` | Third-party program, DLLs, runtime installer and GUI manuals excluded; the custom HID reader does not depend on them |
| Root handoff file | Original retained in `archive/`; new instructions in README/AGENTS/docs |

## Review on 31 October 2026, package revision 2

After the initial package preparation, the author clarified that the board was already operating on the machine, had passed tests and was not heating up. This status was added to README, AGENTS and the documentation; the earlier pending-test item for the combined path was removed. Old records were left unchanged as calibration history.

Before the update, comparison with the previous manifest showed that the author had removed **54 files**, all from `схема_плата/`: 7 `.dip`, 1 `.dch`, 23 `.eli`, 22 `.lib` and 1 `.zip`. Other files were unchanged at the time of comparison. The removals were preserved; sources were not restored from the adjacent working directory.

`корпус/RUICHI A09.jpg` was found in the original directory, inspected and copied into the package with unchanged bytes. It was added to the README. The XLSX BOM remained in the schematic directory and was retained.

## Installation photographs on 2 November 2026, package revision 4

Two inspected photographs were added from the original `фото/` directory: `Корпус.jpg` → `фото/Корпус_на_машине.jpg` and `плата_в_корасе.jpg` → `фото/Плата_в_корпусе.jpg`. Image bytes were retained; copy names were clarified for convenience. The README received the images with captions “Control enclosure installed on the machine” and “Control board inside the enclosure, lid open”; enclosure documentation received links to them.

Before the change, GitHub commits through `b774e7c` were obtained: the author's README edits, `LICENSE`, `LICENSES/CERN-OHL-P-2.0.txt` and updated NOTICE were preserved. The revision-3 manifest already differed from README and NOTICE after those edits; revision 4 accounts for them, the added licenses, new photographs and associated documentation update. Schematic, Gerber, DSP projects, tools and calibrations were unchanged.

When checked on GitHub on 2 November 2026, the repository was already Public. The obsolete current-Private statement was corrected; access settings were not changed.

## New and adapted files

- `README.md` describes the purpose, relocation of the board away from heat, use of audio DSP, signal paths and contents.
- `AGENTS.md` defines project orientation and continuation of AI-assisted debugging on another computer.
- `docs/SETUP.md`, `docs/STATUS.md` and directory explanations distinguish the current configuration from history.
- `tools/check_project.py` checks package hashes, project parsing, table/export consistency and basic constants.
- `tools/sigma/inspect_project.py` prints a structured saved-project report without hardware access.
- `tools/meter/meter.ps1` selects Python from an environment variable or PATH, without the author's profile.
- `tools/sigma/build_bridge.ps1` builds the native API bridge from C# on the user's computer.
- `SigmaBridge.cs`, `sigma_api.py` and `capture_node.py` use configurable paths. Capture checks validate sample count and register-setup failure; those checks remain active with Python `-O`.
- `.gitignore` excludes local logs, temporary files, caches and compiled EXE/DLL files. `.gitattributes` preserves original bytes and line endings for SHA256 verification after transfer.

## Checksums

`docs/manifest.json` contains relative paths, sizes and SHA256 hashes of every supplied file except itself. Files originating in the original directory additionally record the original path, original SHA256 and whether they changed during preparation. Full paths into the author's profile are not recorded.

The Russian source of this inventory describes package revision 4; the verification tool does not update the manifest. Revision 2 covered the file removals and enclosure image above. Revision 3 added a link to the initially private repository and updated hosting information. Revision 4 covered the installation photographs, licenses and documentation changes above. Metadata retained the previous manifest's SHA256 and the update description. After your own changes, differences from that package are expected and require deliberate comparison. Table consistency does not prove the correctness of every connection or hardware operation.

The author's publication destination is [neuroandriyanov/PropValve-RE06MT](https://github.com/neuroandriyanov/PropValve-RE06MT), initially private and public as of 2 November 2026. Only the prepared directory was included; adjacent source directories were not uploaded.
