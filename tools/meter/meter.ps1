# Portable launcher. Arguments are forwarded without string evaluation.
$ErrorActionPreference = 'Stop'
$meterReader = Join-Path $PSScriptRoot 'read_meter.py'
if ($env:PROPVALVE_PYTHON) {
    & $env:PROPVALVE_PYTHON $meterReader @args
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 $meterReader @args
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python $meterReader @args
} else {
    throw 'Install Python 3.11+ or set PROPVALVE_PYTHON to its executable.'
}
exit $LASTEXITCODE
