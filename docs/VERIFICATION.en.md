# Prepared-package verification

[Русский](VERIFICATION.md) | English

Date: 31 October 2026. Checks were run locally on Windows with Python 3.12 and the .NET Framework compiler. The declared Python 3.11 minimum follows the standard-library APIs used; there was no separate run on Python 3.11 or other operating systems.

- SHA256 hashes of all copied originals were compared with their sources. Original files were unchanged. Differences existed only in four intentionally adapted copies: `meter.ps1`, `SigmaBridge.cs`, `sigma_api.py` and `capture_node.py`.
- All 10 `.dspproj` files were parsed successfully without running SigmaStudio or .NET deserialization. The working version and handoff snapshot matched.
- The working project's four tables were checked against text exports; corresponding tables were also compared with JSON settings. Basic constants, readback presence and the absence of old manual sources are checked by `tools/check_project.py`.
- All 7 existing multimeter-decoder tests passed: checksum, frame fragmentation, real data, units, polarity, modes unsuitable for calibration and rejection of other commands.
- The portable multimeter launcher was checked through `--help` with an explicitly selected Python. USB/HID was not polled.
- `build_bridge.ps1` successfully compiled the C# source. The test EXE was kept outside the supplied folder; no SigmaStudio server calls were made.
- Capture-register setup failure and invalid sample-count handling were checked with a substituted API and no hardware. A setup failure prevents subsequent reading.
- Syntax of active Python scripts and local Markdown links was checked.

On 31 October 2026, the author reported that the board had passed testing, was operating on the machine and showed no board heating. This is the current operating status. The assistant checks listed above concern files and tools; the assistant did not repeat the machine test.

## Recheck after changing package contents

- Removal of 54 DipTrace, library and duplicate-ZIP files was checked against the previous manifest. Other files were unchanged before documentation edits.
- The RUICHI A09 enclosure image was inspected and copied from the original directory. Its SHA256 matched the original.
- Documentation was updated with the test status and actual directory contents; the enclosure image was added to the README.
- The revision-2 manifest was recalculated for that package. Its checksums, 10 SigmaStudio projects, 4 tables and local links were verified.
- Tool code was unchanged; the tests and build listed above refer to that same code version.

Repeat the offline checks using the [setup instructions](SETUP.en.md). `docs/manifest.json` describes the prepared package version; new local results in `output/` are not included.

This is a translation of the historical verification report, not a claim that its hardware or compiler checks were repeated for the translation.
