# English annotations for the original hardware files

[Hardware overview](README.en.md) · [Original schematic](схема.pdf) · [English workbook](Спецификация_для_пайк.en.xlsx) · [BOM label translations](BOM-labels.en.md)

These annotations accompany the original files, whose bytes and electrical content are unchanged. They translate visible text; they do not correct a circuit or establish a previously undocumented connection.

## Schematic PDF

Both PDF pages were visually inspected. Most labels, component identifiers, values, pin names and the drawing title block are already Latin-script engineering notation. The Russian labels are:

| Page and location | Original | English meaning |
| --- | --- | --- |
| Page 1, DA7.2 near grid E7 | `ошибка` | `error` — the author's annotation of a problem at this buffer. It is retained as a warning, not silently corrected. See the documented DA7.2 wire modification and the limits of its reconstruction in the hardware overview. |
| Page 1, R5 near grid D2 | `330 2ВТ` | `330 Ω, 2 W` — resistor value and power rating. |

Page 2 uses component/pin identifiers and existing English labels; it needs no replacement of prose. The printed sheet indicator is part of the original drawing, even though the PDF contains two pages.

The schematic PDF has no included editable DipTrace source. Its raster/vector electrical drawing is therefore shared between languages, with this separate English annotation. No altered manufacturing drawing is implied.

## Soldering and cost workbook

The original `Спецификация_для_пайк.xlsx` contains three sheets:

1. `Порядок пайки` — **Soldering order**.
2. `Исходные данные` — **Source data**.
3. `Цены и источники` — **Prices and sources**.

The [English XLSX](Спецификация_для_пайк.en.xlsx) translates every Russian header, category and explanatory note, the three sheet names, and printed headers and footers. The [cell-by-cell companion](BOM-labels.en.md) retains locators in the original sheet names. Component values, quantities, formula logic and cached results, ruble prices, source links, cell formatting and print settings are preserved; formula and print-range references follow the renamed sheets. The original workbook remains byte-identical. The price assumptions are historical; translation does not recheck their availability or prices.

## Manufacturer document and photographs

`doc/Parker-Series-RE06MT.pdf` is already the manufacturer's English document. Its third-party rights and notices remain unchanged. Its statements concern the original Parker product and must not be treated as measured characteristics of this replacement board.

Photographs remain original shared images, with English captions in the README and enclosure guide. Printed component markings, personal text on the PCB and branding are not retouched. Their appearance does not establish ratings or exact wiring.
