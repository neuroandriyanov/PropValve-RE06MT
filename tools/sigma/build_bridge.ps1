param([string]$OutputPath)
$ErrorActionPreference = 'Stop'
if (-not $OutputPath) {
    $OutputPath = Join-Path (Split-Path $PSScriptRoot -Parent) 'bin/SigmaBridge2.exe'
}
$bridgeCandidates = @(
    (Join-Path $env:WINDIR 'Microsoft.NET/Framework64/v4.0.30319/csc.exe'),
    (Join-Path $env:WINDIR 'Microsoft.NET/Framework/v4.0.30319/csc.exe')
)
$bridgeCompiler = $bridgeCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
if (-not $bridgeCompiler) {
    throw '.NET Framework C# compiler was not found. Install the .NET Framework developer tools.'
}
$bridgeOutput = [IO.Path]::GetFullPath($OutputPath)
[IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($bridgeOutput)) | Out-Null
& $bridgeCompiler /nologo /r:System.Web.Extensions.dll /r:System.Drawing.dll "/out:$bridgeOutput" (Join-Path $PSScriptRoot 'SigmaBridge.cs')
if ($LASTEXITCODE -ne 0) { throw "C# compilation failed: $LASTEXITCODE" }
Write-Output "Built $bridgeOutput"
