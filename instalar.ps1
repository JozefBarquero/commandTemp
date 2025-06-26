
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(`
    [Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "Requiere privilegios de administrador. Intentando relanzar..."
    Start-Process powershell "-ExecutionPolicy Bypass -File `"$PSCommandPath`"" -Verb RunAs
    exit
}

$archivo1 = "cliente.py"
$archivo2 = "server.py"
$batFile = "temp.bat"
$carpetaDestino = "C:\Scripts"


if (!(Test-Path $archivo1) -or !(Test-Path $archivo2)) {
    Write-Host "No se encontró '$archivo1' o '$archivo2' en este directorio."
    exit 1
}


if (!(Test-Path $carpetaDestino)) {
    New-Item -ItemType Directory -Path $carpetaDestino | Out-Null
}


Copy-Item $archivo1 -Destination $carpetaDestino
Copy-Item $archivo2 -Destination $carpetaDestino


$batContent = "@echo off`npython `"$carpetaDestino\cliente.py`" %*"
Set-Content -Path "$carpetaDestino\$batFile" -Value $batContent -Encoding ASCII

Write-Host "Scripts y archivo .bat copiados en $carpetaDestino"


$envPath = [System.Environment]::GetEnvironmentVariable("Path", "Machine")
if (-not $envPath.Split(';') -contains $carpetaDestino) {
    [System.Environment]::SetEnvironmentVariable("Path", "$envPath;$carpetaDestino", "Machine")
    Write-Host "Ruta $carpetaDestino agregada al PATH del sistema. Reiniciá la terminal para que surta efecto."
} else {
    Write-Host "La ruta ya estaba en el PATH."
}


$puerto = 54001
$reglaNombre = "PuertoClienteServer54001"
if (-not (Get-NetFirewallRule -DisplayName $reglaNombre -ErrorAction SilentlyContinue)) {
    New-NetFirewallRule -DisplayName $reglaNombre -Direction Inbound -Protocol TCP -LocalPort $puerto -Action Allow
    Write-Host "Puerto $puerto habilitado en el Firewall."
}

Write-Host "`n Instalación completa."
