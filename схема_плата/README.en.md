# Hardware

[Русский](README.md) | English

- `схема.pdf` — two sheets: power supply and power/analog path, followed by the DSP, EEPROM and interface. The [English annotation guide](ANNOTATIONS.en.md) explains Russian labels without altering the schematic.
- `Proportional Valve Controller_v0/` — unpacked Gerber/drill set: 7 `.gbr` files, `Through1.drl` and `Through2.tap`.
- [English component workbook](Спецификация_для_пайк.en.xlsx) — historical soldering list, component values and cost estimates, with all three sheets translated. It is not a current purchasing quotation. The [Russian original](Спецификация_для_пайк.xlsx) is unchanged; the [cell-by-cell translation guide](BOM-labels.en.md) provides original sheet names and cell addresses.

The author excluded DipTrace `.dip`/`.dch` files, libraries and the duplicate Gerber ZIP from the package. PDF and Gerber viewers are needed for the remaining files.

The author's board is already installed on the machine and has passed testing; no board heating has been observed in operation. The following notes concern reproducing it from the supplied materials.

## Board connectors according to the PDF

| Connector | Function | Note |
| --- | --- | --- |
| X1 | 24 V supply | Pin 1: +24 V, pin 2: GND |
| X2 | Coil | Check the power-output connection against the schematic and your load |
| X3 | Actual-current monitor output | Pin 1: signal, pin 2: GND_ISO |
| X4 | External 0–10 V command | Pin 1: signal, pin 2: GND_ISO |
| X5 | Programming interface | Check both ends against the second schematic sheet |

`GND` and `GND_ISO` are distinct named nets. X1…X5 identify connectors on this PCB; they do not correspond to A…G on the original Parker connector. A direct adapter cable and its pinout are not established by the materials.

## Reproduction notes

The supplied calibrations use **R42 and R43 = 10 kΩ**. The PDF has already been updated, but the BOM still says 180 Ω and the photograph shows the old values. R3 in the same BOM row remains a separate component: the replacement note applies only to R42/R43.

The PDF retains the author's “error” annotation at DA7.2. The photograph shows a wire modification near DA7. Account for this modification when reproducing the board. The PDF and Gerber files were left unedited; no separately corrected manufacturing set was created during package preparation.

The [enclosure directory](../корпус/README.en.md) retains `заглушка.m3d`, `заглушка.stl`, `d.lxcf` and the author-supplied `RUICHI A09.jpg` image.
