# Copyright (c) Dario Pizzolante
Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$pythonExe = Join-Path $repoRoot ".venv\Scripts\python.exe"
$frontendDir = Join-Path $repoRoot "frontend"
$frontendEnv = Join-Path $frontendDir ".env"
$frontendEnvExample = Join-Path $frontendDir ".env.example"
$frontendNodeModules = Join-Path $frontendDir "node_modules"
$rootEnv = Join-Path $repoRoot ".env"

if (-not (Test-Path $pythonExe)) {
    throw "Missing virtual environment Python at $pythonExe. Create the venv and install backend dependencies first."
}

if (-not (Test-Path $frontendEnv) -and (Test-Path $frontendEnvExample)) {
    Copy-Item $frontendEnvExample $frontendEnv
}

if (Test-Path $rootEnv) {
    $envMap = @{}
    foreach ($line in Get-Content $rootEnv) {
        if ([string]::IsNullOrWhiteSpace($line) -or $line.TrimStart().StartsWith("#")) {
            continue
        }
        $parts = $line -split "=", 2
        if ($parts.Count -eq 2) {
            $envMap[$parts[0].Trim()] = $parts[1].Trim()
        }
    }

    $inboxConnector = ""
    if ($envMap.ContainsKey("INBOX_CONNECTOR")) {
        $inboxConnector = $envMap["INBOX_CONNECTOR"].ToLowerInvariant()
    }

    $calendarConnector = ""
    if ($envMap.ContainsKey("CALENDAR_CONNECTOR")) {
        $calendarConnector = $envMap["CALENDAR_CONNECTOR"].ToLowerInvariant()
    }

    $tasksConnector = ""
    if ($envMap.ContainsKey("TASKS_CONNECTOR")) {
        $tasksConnector = $envMap["TASKS_CONNECTOR"].ToLowerInvariant()
    }

    $graphRefreshToken = ""
    if ($envMap.ContainsKey("MICROSOFT_GRAPH_REFRESH_TOKEN")) {
        $graphRefreshToken = $envMap["MICROSOFT_GRAPH_REFRESH_TOKEN"]
    }

    $zimbraBaseUrl = ""
    if ($envMap.ContainsKey("ZIMBRA_BASE_URL")) {
        $zimbraBaseUrl = $envMap["ZIMBRA_BASE_URL"]
    }

    $zimbraAccessToken = ""
    if ($envMap.ContainsKey("ZIMBRA_ACCESS_TOKEN")) {
        $zimbraAccessToken = $envMap["ZIMBRA_ACCESS_TOKEN"]
    }

    $zimbraUsername = ""
    if ($envMap.ContainsKey("ZIMBRA_USERNAME")) {
        $zimbraUsername = $envMap["ZIMBRA_USERNAME"]
    }

    $zimbraPassword = ""
    if ($envMap.ContainsKey("ZIMBRA_PASSWORD")) {
        $zimbraPassword = $envMap["ZIMBRA_PASSWORD"]
    }

    $usesOutlookInbox = @("outlook", "microsoft_graph", "graph") -contains $inboxConnector
    $usesOutlookCalendar = @("outlook", "microsoft_graph", "graph") -contains $calendarConnector
    $usesZimbra = @("zimbra") -contains $inboxConnector -or @("zimbra") -contains $calendarConnector -or @("zimbra") -contains $tasksConnector
    $hasGraphRefreshToken = -not [string]::IsNullOrWhiteSpace($graphRefreshToken)
    $hasZimbraAuth = (-not [string]::IsNullOrWhiteSpace($zimbraAccessToken)) -or (
        (-not [string]::IsNullOrWhiteSpace($zimbraUsername)) -and (-not [string]::IsNullOrWhiteSpace($zimbraPassword))
    )

    if (($usesOutlookInbox -or $usesOutlookCalendar) -and -not $hasGraphRefreshToken) {
        Write-Host "Warning: Outlook connectors are enabled, but MICROSOFT_GRAPH_REFRESH_TOKEN is missing." -ForegroundColor Yellow
        Write-Host "Run '.venv\\Scripts\\python.exe scripts\\microsoft_graph_device_code.py' once to enable automatic token refresh on app startup." -ForegroundColor Yellow
        Write-Host ""
    }

    if ($usesZimbra -and ([string]::IsNullOrWhiteSpace($zimbraBaseUrl) -or -not $hasZimbraAuth)) {
        Write-Host "Warning: Zimbra connectors are enabled, but ZIMBRA_BASE_URL or credentials are missing." -ForegroundColor Yellow
        Write-Host "Set ZIMBRA_BASE_URL plus either ZIMBRA_ACCESS_TOKEN or ZIMBRA_USERNAME/ZIMBRA_PASSWORD before relying on live reads." -ForegroundColor Yellow
        Write-Host ""
    }
}

Write-Host "Starting PostgreSQL container..." -ForegroundColor Cyan
docker compose up -d

Write-Host "Applying database initialization..." -ForegroundColor Cyan
& $pythonExe (Join-Path $repoRoot "scripts\init_db.py")

if (-not (Test-Path $frontendNodeModules)) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
    Push-Location $frontendDir
    try {
        npm install
    }
    finally {
        Pop-Location
    }
}

$backendCommand = @"
Set-Location '$repoRoot'
& '$pythonExe' -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload
"@

$frontendCommand = @"
Set-Location '$frontendDir'
npm run dev
"@

Write-Host "Launching backend window..." -ForegroundColor Cyan
Start-Process powershell.exe -ArgumentList @("-NoExit", "-Command", $backendCommand) | Out-Null

Write-Host "Launching frontend window..." -ForegroundColor Cyan
Start-Process powershell.exe -ArgumentList @("-NoExit", "-Command", $frontendCommand) | Out-Null

Write-Host ""
Write-Host "Backend:  http://127.0.0.1:8000/healthz" -ForegroundColor Green
Write-Host "Frontend: http://127.0.0.1:5173" -ForegroundColor Green
