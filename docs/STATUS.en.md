# Project status and material review

[Русский](STATUS.md) | English

Saved calibration state: 27 October 2026. Author clarification and package review: 31 October 2026.

## Operation on the machine

On 31 October 2026, the author reported: **the board was already installed and operating on the machine, had passed testing, and no board heating was observed**. Moving the electronics away from the valve's heat had been completed and checked in operation on this particular unit.

The earlier statement that the combined path had not yet been tested described the calibration log as of 27 October 2026. It is obsolete as a description of the current operating status. The date above is when the author reported the result, not an established test date. Numerical temperatures, test duration and operating conditions were not supplied.

## Working version

`проект_сигма/Design1_parker_v0.dspproj` and `Design1_parker_transfer_2026-10-27.dspproj` were byte-identical when the package was prepared. The file was read by a data-only NRBF parser: it contains four tables, the required constants and readbacks, and no longer contains the old manual sources `CURRENT_INPUT_0_1` and `DC2_4`. The saved netlist connections match the paths shown in the README.

The saved compiler report lists 153 instructions, 38 Data RAM words and 45 Parameter RAM words. The report itself contains generic text about an estimate at 48 kHz; the project's 96 kHz sample rate is recorded in the calibration settings and log. Do not treat a report-template line as confirmation of the hardware's current sample rate.

During documentation preparation, the assistant inspected files without connecting to equipment. The machine tests were performed by the author; the assistant did not run the machine again as part of the folder review. The packaged working `.dspproj` was not changed.

## Calibrations

These are the largest observed differences in the saved series, not guaranteed absolute accuracy or a tolerance applicable to another board.

| Channel | Observation | Record in `measurements/2026-10-27/` |
| --- | --- | --- |
| 0–10 V output | Up to 1 mV relative to the meter reading | `output_calibration_verification.json` |
| Current command | Up to 7.5 mA between command and meter reading | `feedback_final_verification.json` |
| DSP current measurement | About 2.8 mA relative to the meter in the final series | `feedback_final_verification.json` |
| 0–10 V input | Up to 1.326 mV, checked at 11 points | `voltage_input_verify.json` |

These saved series concern individual-channel calibration **before the final control-path integration**. The author subsequently confirmed successful board tests on the machine. The accuracy of the series is limited, among other things, by the multimeter's accuracy and resolution. One earlier series recorded current-channel zero drift equivalent to approximately 26 mA. That is an observation from calibration, not a new measurement on the machine.

Extract exact coefficients and Min/Max with `py -3 tools/sigma/inspect_project.py`. External TXT coefficient files do not contain the entire block configuration. Prefer the saved `.dspproj` and JSON settings for restoration.

| Table | Input range | Role |
| --- | --- | --- |
| `VIN_TABLE_0_10V` | −1…+1 | ADC0 → normalized voltage; output is additionally limited to 0…1 |
| `CURRENT_0_3A` | 0…1 | Command → differential DAC0/DAC1 output code |
| `I_FEEDBACK_0_1` | −0.78…+0.70 | ADC1 → normalized actual current; limiters precede the table |
| `Interpolator1` | 0…1 | Normalized current → DAC3 → X3; DAC2 must be 0 |

## Differences between the materials

1. **R42/R43.** The current PDF already shows 10 kΩ. The original XLSX BOM says 180 Ω, and the photograph shows the marking `1800`. The working calibrations apply to 10 kΩ. The photographs and BOM are preserved as original materials; they cannot be used unconditionally to build the calibrated version.
2. **DA7.2.** The first schematic sheet contains the author's “error” annotation by the refdac buffer. The photograph shows a wire modification near DA7. Its relationship to a specific PCB revision has not been documented. The correction circuit was not reconstructed from a photograph alone.
3. **Hardware files.** The author removed `.dip`, `.dch`, DipTrace libraries and the duplicate ZIP from the package. The PDF, unpacked v0 Gerber/drill set and XLSX remain. Account for the resistor values and modification described above when manufacturing a new board.
4. **Pinout and ranges.** Board markings in the photograph mention ±10 V; the saved DSP project is calibrated for 0…10 V. Do not extend the operating range on the basis of PCB text alone.
5. **Parker specification.** The supplied document includes F versions (0…10 V in the table and block diagram) and R versions (4…20 mA). Its introduction also mentions ±10 V. This does not confirm that this board supports all versions. The exact order code of the modified unit is absent.
6. **Current.** The original valve specification gives a maximum supply current of 2.0 A. That is not an approved coil-current limit. The bench board's 3 A scale must be checked against the specific solenoid; universal compatibility has not been established.
7. **EEPROM.** E2Prom.bin/Hex in `archive/eeprom-unverified/` came from the original archive. The 27 October 2026 log recorded that EEPROM was not written at that stage. The current EEPROM contents of the working machine were not separately reported; the archived images are not claimed to be a verified copy.

## Reproducing the design on another unit

For another unit, establish the valve variant and coil parameters, compare PDF/BOM/Gerber and the DA7.2 modification, and perform a new calibration. [SETUP.en.md](SETUP.en.md) describes connection checks and checking the X3–X4 jumper. This is a procedure for transferring the design to other equipment, not a list of tests left undone on the author's machine.

In the saved DSP project, `ZERO_OFF` compares the command with exact zero. The previously discussed 10/20 mV hysteresis is not implemented in this file. It is a possible development, not an established defect in machine operation. `ZERO_CONSTANT` supplies both the threshold and the zero output; do not change it without separating these functions.

## Enclosure and package updates

The [RUICHI A09 image](../корпус/RUICHI%20A09.jpg) was added from the original `корпус/` directory. It shows the enclosure with its ribbed lid and mounting lugs. The blanking-part files remain; see [корпус/README.en.md](../корпус/README.en.md).

On 2 November 2026, the author added photographs of the [control enclosure on the machine](../фото/Корпус_на_машине.jpg) and the [control board inside the open enclosure](../фото/Плата_в_корпусе.jpg). Both were added to the README with their bytes unchanged. This is the date the materials were added, not an established photography date or a date of new tests.
