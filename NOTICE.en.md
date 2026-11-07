# Material provenance and licensing

[Русский](NOTICE.md) | **English**

This folder was prepared locally from PropValve materials. It is not an official Parker Hannifin or Analog Devices project; names describe compatibility and components.

## Permissive licenses for original materials

- **MIT** — original program source (Python, C#, PowerShell), original helper scripts and their associated original documentation. Full text: [LICENSE](LICENSE).
- **CERN-OHL-P-2.0** — original hardware design materials: electrical schematic, board production files, original enclosure drawings and models, to the extent that the author holds rights to them. Full text: [LICENSES/CERN-OHL-P-2.0.txt](LICENSES/CERN-OHL-P-2.0.txt).
- **Independently created SigmaStudio settings and project files**, to the extent protected by the author's copyright and not containing proprietary third-party code or materials, are under MIT. This licensing grants no rights to SigmaStudio or third-party libraries/components.

Both licenses permit commercial use, modification and distribution subject to the applicable license terms. No rights to third-party trademarks or patents are automatically transferred.

## Exceptions and third-party materials

- `doc/Parker-Series-RE06MT.pdf` is Parker Hannifin documentation. It is **not licensed** under MIT or CERN-OHL-P. Rights remain with the respective rights holder; permission for public redistribution is a separate matter.
- `корпус/RUICHI A09.jpg` is an image of a RUICHI-branded product. Rights to the photograph must be established separately if its photographer is not the repository owner.
- Parker, Analog Devices, RUICHI, SigmaStudio and their product designations remain the names of their respective rights holders.
- Third-party dependencies, manufacturer documentation, software environments, proprietary libraries and any included third-party elements are not relicensed under these licenses.
- `фото/PCB_TOP.JPG` and `фото/PCB_BOTTOM.JPG` may contain personal contact details printed on the board. Before opening the repository, the author should decide whether they may be published.

## Publication and technical limitations

When the licenses were added, the repository was **Private**. During the photo update on 02.11.2026, its current status was confirmed as **Public**; access settings were not changed as part of that update. Adding licenses by itself does not change repository visibility.

Original DipTrace `.dip`, `.dch` files and shared libraries are not included. When reproducing the board, account for the differences in R42/R43 between the historical BOM and working configuration, and the hardware rework near DA7.2. See `docs/STATUS.en.md`.
