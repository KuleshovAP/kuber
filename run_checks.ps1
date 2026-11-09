# Запускайте из каталога решения в PowerShell с доступом к Docker Desktop.
$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Force evidence | Out-Null

function Invoke-Checked {
    param([string]$Log, [string]$Program, [string[]]$Arguments)
    # Windows PowerShell 5.1 оформляет stderr native-команд как ErrorRecord;
    # Docker пишет туда и обычный progress. Проверяем фактический exit code.
    $ErrorActionPreference = 'Continue'
    & $Program @Arguments 2>&1 | Tee-Object -FilePath (Join-Path 'evidence' $Log)
    if ($LASTEXITCODE -ne 0) { throw "Команда завершилась с ошибкой: $Program $Arguments" }
}

Invoke-Checked 'compose-config.log' 'docker' @('compose','config','--quiet')
Invoke-Checked 'compose-up.log' 'docker' @('compose','up','-d','--wait','kafka')
Invoke-Checked 'app-build.log' 'docker' @('compose','build','app')
Invoke-Checked 'unit.log' 'docker' @('compose','run','--rm','app','python','-m','pytest','tests/unit','-v')
Invoke-Checked 'integration.log' 'docker' @('compose','run','--rm','app','python','-m','pytest','tests/integration','-v')
Invoke-Checked 'app.log' 'docker' @('compose','run','--rm','app')
Invoke-Checked 'compose-ps.log' 'docker' @('compose','ps')
