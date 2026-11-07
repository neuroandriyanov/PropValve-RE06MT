# Hardware

[Русский](README.md) | **English**

- `схема.pdf` contains two sheets: power supply and power/analog path; then DSP, EEPROM and interface. An [English schematic](schematic.en.pdf) and [translation notes](schematic-notes.en.md) accompany the original drawing.
- `Proportional Valve Controller_v0/` is the unpacked Gerber/drill set: 7 `.gbr` files, `Through1.drl` and `Through2.tap`.
- `Спецификация_для_пайк.xlsx` is the historical assembly BOM, values and cost estimates. It is not a current purchasing estimate. The [English workbook](Спецификация_для_пайк.en.xlsx) preserves its values and formulas.

The author excluded DipTrace `.dip`/`.dch`, libraries and the duplicate Gerber ZIP from the package. PDF and Gerber viewers are needed for the remaining materials.

The author's board is already installed on the machine and has passed tests; no board heating is observed during operation. The following notes concern reproduction from the supplied materials.

## Connectors on this board according to the PDF

| Connector | Purpose | Note |
| --- | --- | --- |
| X1 | 24 V supply | Pin 1: +24 V; pin 2: GND |
| X2 | Coil | Check the power-output connection against the schematic and your load |
| X3 | Actual-current monitor output | Pin 1: signal; pin 2: GND_ISO |
| X4 | External 0–10 V command | Pin 1: signal; pin 2: GND_ISO |
| X5 | Programming interface | Check both sides of the connection against the schematic's second sheet |

`GND` and `GND_ISO` are separately labeled nets. X1…X5 numbering belongs to this PCB and does not match A…G designations on the standard Parker connector. A direct adapter cable and its pinout are not confirmed by these materials.

## Reproduction notes

For the supplied calibrations, **R42 and R43 = 10 kΩ**. The PDF is already updated, but the BOM still lists 180 Ω and the photos show the old values. R3, in the same BOM row, remains a separate component: the replacement note applies only to R42/R43.

The PDF retains the author's “ошибка” (“error”) annotation at DA7.2. A photograph shows a wire rework near DA7. Account for this rework when reproducing the board. The PDF and Gerber are unmodified; no separately corrected manufacturing-file set was created while preparing the package.

The [enclosure folder](../корпус/README.en.md) retains `заглушка.m3d`, `заглушка.stl`, `d.lxcf` and the author-added `RUICHI A09.jpg` image.
