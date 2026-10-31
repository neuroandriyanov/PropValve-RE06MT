$ErrorActionPreference = 'Stop'
$sigmaAssembly = [Reflection.Assembly]::LoadFrom('C:\Program Files\Analog Devices\SigmaStudio 4.7\Analog.SigmaStudioServer.dll')
foreach ($sigmaType in $sigmaAssembly.GetExportedTypes()) {
    Write-Output $sigmaType.FullName
    foreach ($sigmaMethod in $sigmaType.GetMethods([Reflection.BindingFlags]'Public,Instance,DeclaredOnly')) {
        Write-Output $sigmaMethod.ToString()
    }
}
