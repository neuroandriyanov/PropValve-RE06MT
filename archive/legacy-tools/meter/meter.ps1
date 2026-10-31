# Convenience launcher. All arguments are forwarded to the Python reader.
$meterPython = 'C:\Users\Sergey\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
if (-not (Test-Path -LiteralPath $meterPython)) {
    throw 'Bundled Python was not found. Run read_meter.py using an installed Python 3.'
}
& $meterPython (Join-Path $PSScriptRoot 'read_meter.py') @args
exit $LASTEXITCODE
