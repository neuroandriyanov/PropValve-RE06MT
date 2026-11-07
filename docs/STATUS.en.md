# Project status and material-verification results

[Русский](STATUS.md) | **English**

Saved calibrations: 27.10.2026. Author clarification and repeat package review: 31.10.2026.

## Operation on the machine

On 31.10.2026, the author reported: **the board is already installed and operating on the machine, has passed tests, and shows no observed heating**. Moving the electronics away from the valve's heat has been completed and checked during operation of this particular unit.

The earlier note that the combined path had not yet been tested described the calibration log's state on 27.10.2026. It is obsolete for the current operational status. The stated date is the author's report date, not an established date of testing. Numerical temperatures, test duration and operating conditions were not provided.

## Working version

`проект_сигма/Design1_parker_v0.dspproj` and `Design1_parker_transfer_2026-10-27.dspproj` matched byte for byte during preparation. A data-only NRBF parser read the file: it contains four tables and the required constants and indicators; the old manual sources `CURRENT_INPUT_0_1` and `DC2_4` are absent. The saved netlist connections match the signal paths in README.

Saved compiler report: 153 instructions, 38 Data RAM words, 45 Parameter RAM words. The report contains generic estimation text for 48 kHz; the project's actual 96 kHz sample rate is recorded in the calibration settings and log. Do not interpret the report-template line as confirmation of the hardware's current sample rate.

During document preparation, the assistant checks files without connecting to hardware. The author performed machine tests; the machine was not restarted as part of the folder review. The package's working `.dspproj` was not modified.

## Calibrations

The following are the maximum observed differences in the saved series, not guaranteed absolute accuracy or tolerances for another board.

| Channel | Observation | Record in `measurements/2026-10-27/` |
| --- | --- | --- |
| 0–10 V output | Up to 1 mV relative to the meter reading | `output_calibration_verification.json` |
| Current command | Up to 7.5 mA between command and meter reading | `feedback_final_verification.json` |
| DSP current measurement | About 2.8 mA relative to the meter in the final series | `feedback_final_verification.json` |
| 0–10 V input | Up to 1.326 mV, checked at 11 points | `voltage_input_verify.json` |

These saved series calibrated individual channels **before the final integration of the signal path**. The author subsequently confirmed successful board tests on the machine. The series' accuracy is limited, among other factors, by the multimeter's accuracy and resolution. One older series showed current-measurement zero drift equivalent to approximately 26 mA. That is a calibration-stage observation, not a new machine measurement.

Extract exact coefficients and Min/Max using `py -3 tools/sigma/inspect_project.py`. External coefficient TXT files do not contain all block settings. The saved `.dspproj` and JSON settings are preferable for restoration.

| Table | Input range | Role |
| --- | --- | --- |
| `VIN_TABLE_0_10V` | −1…+1 | ADC0 → normalized voltage; output is separately clamped to 0…1 |
| `CURRENT_0_3A` | 0…1 | Command → differential DAC0/DAC1 output code |
| `I_FEEDBACK_0_1` | −0.78…+0.70 | ADC1 → normalized actual current; clamps precede the table |
| `Interpolator1` | 0…1 | Normalized current → DAC3 → X3; DAC2 must be 0 |

## Differences between materials

1. **R42/R43.** The current PDF already shows 10 kΩ. The original XLSX BOM lists 180 Ω, and the photos show `1800` markings. Working calibrations use 10 kΩ. Photos and BOM remain unmodified source materials and cannot be used unconditionally to build the calibrated version.
2. **DA7.2.** The schematic's first sheet contains the annotation “ошибка” (“error”) at the refdac buffer. A wire rework near DA7 is visible in the photos. Its correspondence to a particular PCB revision is undocumented. No correction circuit was reconstructed from a photograph alone.
3. **Hardware-file contents.** At the author's request, `.dip`, `.dch`, DipTrace libraries and the duplicate ZIP were removed from the package. The PDF, unpacked v0 Gerber/drill set and XLSX remain. Account for the values and rework described above before manufacturing another board.
4. **Pin assignments and ranges.** Photo-visible board markings mention ±10 V; the saved DSP project is calibrated for 0…10 V. Do not extend its operating range solely from the PCB legend.
5. **Parker datasheet.** The supplied document includes variants F (0…10 V in its table and block diagram) and R (4…20 mA). The introductory page also mentions ±10 V. This does not confirm that this board supports every variant. The exact order code of the modified unit is unavailable.
6. **Current.** The original valve's datasheet specifies maximum current consumption of 2.0 A. That is not an approved coil-current limit. The bench board's 3 A scale requires separate assessment against the particular solenoid; universal compatibility has not been established.
7. **EEPROM.** E2Prom.bin/Hex in `archive/eeprom-unverified/` come from the original archive. The 27.10.2026 log noted that EEPROM had not been written at that stage. The current EEPROM contents of the operating machine were not separately reported; the archived images are not declared a verified copy of it.

## Reproducing another unit

For another unit, determine the valve variant and coil parameters, compare PDF/BOM/Gerber and the DA7.2 rework, then carry out a separate calibration. Connections and the X3–X4 jumper check are covered in [SETUP.en.md](SETUP.en.md). This is a transfer procedure for other hardware, not a list of tests missing from the author's machine.

In the saved DSP project, `ZERO_OFF` compares the command with exact zero. The previously discussed 10/20 mV hysteresis is not implemented in this file. It is a potential development, not an established operating defect on the machine. `ZERO_CONSTANT` supplies both the threshold and zero output; do not change it without separating those functions.

## Enclosure and package update

The [RUICHI A09 image](../корпус/RUICHI%20A09.jpg), found in the original `корпус/` folder, was added. It shows an enclosure with a ribbed lid and mounting lugs. End-cap files are preserved; contents are described in [корпус/README.en.md](../корпус/README.en.md).

On 02.11.2026, the author added photographs of the [control unit enclosure on the machine](../фото/Корпус_на_машине.jpg) and the [board in the open enclosure](../фото/Плата_в_корпусе.jpg). Both were included in README and preserved byte for byte. This is the date the materials were added, not an established shooting date or date of new tests.
