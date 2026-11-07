# Material provenance and licensing

[Русский](NOTICE.md) | English

This directory was prepared locally from PropValve materials. It is not an official Parker Hannifin or Analog Devices project; names are used to describe compatibility and components.

## Permissive licenses for original materials

- **MIT** — original program source (Python, C#, PowerShell), original helper scripts and their associated original documentation. Full text: [LICENSE](LICENSE).
- **CERN-OHL-P-2.0** — original hardware design materials: electrical schematic, PCB manufacturing files and original enclosure drawings/models, to the extent that the author holds the rights to those materials. Full text: [LICENSES/CERN-OHL-P-2.0.txt](LICENSES/CERN-OHL-P-2.0.txt).
- **Independently created SigmaStudio settings and project files**, to the extent covered by the author's copyright and not containing proprietary code or third-party materials — MIT. This licensing does not grant rights to SigmaStudio or third-party libraries/components.

Both licenses permit commercial use, modification and redistribution subject to the applicable license. No rights to third-party trademarks or patents are automatically transferred.

## Exceptions and third-party materials

- `doc/Parker-Series-RE06MT.pdf` — Parker Hannifin documentation. **Not licensed** under MIT or CERN-OHL-P. Rights belong to the respective rights holder; permission for public redistribution is a separate matter.
- `корпус/RUICHI A09.jpg` — image of a product marked RUICHI. Rights to the photograph must be established separately if its photographer is not the repository owner.
- Parker, Analog Devices, RUICHI, SigmaStudio and their product names remain the names of their respective rights holders.
- Third-party dependencies, manufacturer documentation, development environments, vendor libraries and any included third-party elements are not relicensed under these licenses.
- `фото/PCB_TOP.JPG` and `фото/PCB_BOTTOM.JPG` may show personal contact details on the board. Before opening the repository, the author should decide whether those details may be published.

## Publication and technical limitations

The repository was **Private** when the licenses were added. The photograph update on 2 November 2026 confirmed its then-current **Public** status; access settings were not changed during that update. Adding licenses does not itself change repository visibility.

Original DipTrace `.dip`, `.dch` and shared libraries are not included. When reproducing the board, account for the R42/R43 differences between the historical BOM and working configuration, and for the hardware modification near DA7.2. See `docs/STATUS.en.md`.

This English notice translates the Russian notice; the original license texts remain unchanged.
