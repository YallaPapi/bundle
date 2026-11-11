$ErrorActionPreference = 'Stop'
$projectDir = Split-Path -Parent $PSScriptRoot
$pythonExe = (Get-Command python.exe).Source
$pythonWindowless = Join-Path (Split-Path -Parent $pythonExe) 'pythonw.exe'
if (-not (Test-Path -LiteralPath $pythonWindowless)) { throw 'pythonw.exe was not found beside Python.' }
$appFile = Join-Path $PSScriptRoot 'app.py'
$taskName = 'Bundle Local Analytics'
$taskUser = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$action = New-ScheduledTaskAction -Execute $pythonWindowless -Argument ('"' + $appFile + '" serve') -WorkingDirectory $projectDir
$triggers = @((New-ScheduledTaskTrigger -AtLogOn -User $taskUser), (New-ScheduledTaskTrigger -Daily -At '09:00'))
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
$principal = New-ScheduledTaskPrincipal -UserId $taskUser -LogonType Interactive -RunLevel Limited
$task = New-ScheduledTask -Action $action -Trigger $triggers -Settings $settings -Principal $principal -Description 'Local Bundle analytics page with daily GET-only collection and catch-up after downtime.'
Register-ScheduledTask -TaskName $taskName -InputObject $task -Force | Out-Null
Start-ScheduledTask -TaskName $taskName
Get-ScheduledTask -TaskName $taskName | Select-Object TaskName,State
