# Prepared-package verification

[Русский](VERIFICATION.md) | **English**

Date: 31.10.2026. Verification was performed locally on Windows with Python 3.12 and the .NET Framework compiler. The stated Python 3.11 minimum was selected based on the standard-library APIs used; there was no separate run on Python 3.11 or other operating systems.

- SHA256 hashes of all transferred originals were compared against their sources. Original files were unchanged. Differences exist only in four intentionally adapted copies: `meter.ps1`, `SigmaBridge.cs`, `sigma_api.py`, `capture_node.py`.
- All 10 `.dspproj` files were parsed successfully without starting SigmaStudio or using .NET deserialization. The working version and transfer snapshot match.
- The working project's four tables were compared against text exports; the corresponding tables were also checked against JSON settings. `tools/check_project.py` checks basic constants, the presence of indicators and the absence of old manual sources.
- All 7 existing multimeter-decoder tests passed: checksum, frame fragmentation, real data, units, polarity, modes unsuitable for calibration and rejection of other commands.
- The portable multimeter launcher was checked with `--help` and an explicitly selected Python. USB/HID was not polled.
- `build_bridge.ps1` successfully compiled the C# source. The test EXE was kept outside the supplied folder; SigmaStudio server calls were not made.
- Capture-register setup failure and invalid sample-count handling were checked with a mocked API and no hardware. Reading does not start after setup failure.
- Active Python-script syntax and local Markdown links were checked.

On 31.10.2026, the author reported that the board had passed tests, was operating on the machine and showed no observed heating. This is the current operational status. The assistant checks listed above concern files and tools; the assistant did not repeat machine testing.

## Rechecking after the inventory changed

- Removal of 54 DipTrace, library and duplicate ZIP files was checked against the previous manifest. Other files were unchanged before documentation edits.
- The RUICHI A09 enclosure image was inspected and copied from the original folder. Its SHA256 matches the original.
- Documentation was updated with the test status and actual folder contents; the enclosure image was added to README.
- The version 2 manifest was recalculated for the current package. Its checksums, 10 SigmaStudio projects, 4 tables and local links were checked.
- Tool code was unchanged; the preceding test and build results refer to the same code version.

Repeat the offline checks using the commands in the [instructions](SETUP.en.md). `docs/manifest.json` describes the prepared-package version; new local results in `output/` are not included.
