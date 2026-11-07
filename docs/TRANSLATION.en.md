# Russian-first publication and English translation

[Русский](TRANSLATION.md) | **English**

Russian is the project's source language. First update and publish Russian material at its existing address. The English version lives beside it: `README.en.md`, `STATUS.en.md` or `name.en.txt`. Original directory and technical filenames remain stable. Each Markdown page starts with language navigation.

## Normal workflow

1. Edit the Russian document or add a new one. Give new images separate captions; keep text in editable diagrams in their source files.
2. Run `python tools/i18n.py status`. An edited Russian source becomes `stale`; a new untranslated text becomes `pending`. These states do not prevent Russian publication.
3. Translate the complete document into a sibling `.en.*` file, including tables, captions, notes and image alternative text. English document links should lead to English versions; links to source data may be shared.
4. Check meaning, numbers, units, formulas and links. For PDF and XLSX, also check rendering and preservation of technical data. Then record only the reviewed pair, for example: `python tools/i18n.py record docs/STATUS.md docs/STATUS.en.md`.
5. Run `python tools/i18n.py check --strict` before describing the English version as fully current. For normal Russian publication, `python tools/i18n.py check` is sufficient: it allows material awaiting translation while reporting it.

The checker uses only Python's standard library and does not contact translation services. State is stored in [i18n/manifest.json](../i18n/manifest.json): the Russian source path, translation path and SHA256 of both files. Editing an English file after review produces `unreviewed`. Use `record` after actual translation and review; a bulk checksum refresh is not a substitute for translation.

## Translation scope

Translate authored descriptions, instructions, calibration results and historical explanations. English reports reproduce the original measurements and level of certainty. Dates in archived documents and price information refer to the original record.

The schematic and BOM have English copies. Their [notes](../схема_плата/schematic-notes.en.md) list text changes and preserved identifiers. Original photographs are shared; their captions and descriptions are translated in documents.

## Shared and immutable material

- Measurement CSV/JSON, numerical coefficient tables, `.dspproj`, compiler exports, EEPROM, Gerber/Excellon and enclosure files are preserved as technical data. Translating them could change values, format or reproducibility.
- Board and equipment photographs remain original evidence. Do not redraw measurement data or hide rework for a language version.
- Parker documentation and canonical license texts retain their original form; these are third-party or normative texts.
- Source code, commands, paths, parameter names and APIs are not translated as ordinary prose. Their usage instructions have English versions.
- The historical `docs/manifest.json` is not regenerated for translation. It records an earlier package, so adding language navigation to Russian Markdown files may differ from its previous hashes. Translation tracking is separate.

Do not hide new Russian material behind an exclusion merely to pass a check. Add a new pair after translation; record shared data with an explicit reason.
