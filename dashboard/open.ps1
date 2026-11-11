$ErrorActionPreference = 'Stop'
$dashboardUrl = 'http://127.0.0.1:8876/'
try { $null = Invoke-RestMethod ($dashboardUrl + 'api/report?days=1') -TimeoutSec 2 }
catch {
    $task = Get-ScheduledTask -TaskName 'Bundle Local Analytics' -ErrorAction SilentlyContinue
    if ($task) { Start-ScheduledTask -TaskName $task.TaskName }
    else {
        $pythonExe = (Get-Command python.exe).Source
        $pythonWindowless = Join-Path (Split-Path -Parent $pythonExe) 'pythonw.exe'
        Start-Process -FilePath $pythonWindowless -ArgumentList ('"' + (Join-Path $PSScriptRoot 'app.py') + '" serve') -WorkingDirectory (Split-Path -Parent $PSScriptRoot) -WindowStyle Hidden
    }
    for ($attempt = 0; $attempt -lt 12; $attempt++) {
        Start-Sleep -Milliseconds 500
        try { $null = Invoke-RestMethod ($dashboardUrl + 'api/report?days=1') -TimeoutSec 2; break } catch {}
    }
}
Start-Process $dashboardUrl
