# Sync VOLCENGINE_PODCAST_* from local.env to Windows User persistent env.
# Usage: powershell -ExecutionPolicy Bypass -File scripts/sync-user-env-from-local.ps1
#        powershell ... -File ... -ResetFirst   # 先清空本 skill 相关的 User 变量，避免残留错的 APP_ID
param([string]$EnvFile = "", [switch]$ResetFirst)

$KnownKeys = @(
    'VOLCENGINE_PODCAST_APP_ID',
    'VOLCENGINE_PODCAST_ACCESS_KEY',
    'VOLCENGINE_PODCAST_API_KEY',
    'VOLCENGINE_PODCAST_RESOURCE_ID',
    'VOLCENGINE_PODCAST_APP_KEY',
    'VOLCENGINE_PODCAST_RETRY_TASK_ID'
)

if ($ResetFirst) {
    foreach ($k in $KnownKeys) {
        [Environment]::SetEnvironmentVariable($k, $null, 'User')
    }
    Write-Host "ResetFirst: cleared user-level VOLCENGINE_PODCAST_* keys."
}

if (-not $EnvFile) {
    $skillDir = Split-Path $PSScriptRoot -Parent
    $EnvFile = Join-Path $skillDir "local.env"
}
if (-not (Test-Path -LiteralPath $EnvFile)) {
    Write-Error "Missing local.env. Copy local.env.example to local.env under volc-podcast-tts. Expected: $EnvFile"
    exit 1
}

$n = 0
foreach ($raw in Get-Content -LiteralPath $EnvFile -Encoding UTF8) {
    $line = $raw.Trim()
    if (-not $line) { continue }
    if ($line.StartsWith('#')) { continue }
    $eq = $line.IndexOf('=')
    if ($eq -lt 1) { continue }
    $key = $line.Substring(0, $eq).Trim()
    $val = $line.Substring($eq + 1).Trim().Trim('"').Trim("'")
    if ($key.StartsWith('$env:')) { $key = $key.Substring(5) }
    if ($key -notmatch '^VOLCENGINE_PODCAST_') { continue }
    if ([string]::IsNullOrEmpty($val)) { continue }
    [Environment]::SetEnvironmentVariable($key, $val, 'User')
    $n++
}

if ($n -eq 0) {
    Write-Warning "No variables written. Set VOLCENGINE_PODCAST_API_KEY (new console) or APP_ID+ACCESS_KEY in local.env."
    exit 2
}

Write-Host "OK: wrote $n user-level env vars (VOLCENGINE_PODCAST_*). Open a NEW terminal before running cli.py."
