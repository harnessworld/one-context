param(
  [Parameter(Mandatory = $true)]
  [string]$Project
)

$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path -LiteralPath $Project).Path
$Skill = Split-Path $PSScriptRoot -Parent
$Log = Join-Path $Project 'video-build.log'
$CfgPath = Join-Path $Project 'timing\wav-durations.json'
$Mp4 = Join-Path $Project 'final_auto.mp4'
if (Test-Path -LiteralPath $CfgPath) {
  try {
    $cfg = Get-Content -LiteralPath $CfgPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($cfg.outputFile) {
      $Mp4 = if ([System.IO.Path]::IsPathRooted($cfg.outputFile)) {
        $cfg.outputFile
      } else {
        Join-Path $Project $cfg.outputFile
      }
    }
  } catch { }
}

function Log($msg) {
  $line = "[{0}] {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $msg
  Add-Content -LiteralPath $Log -Value $line -Encoding UTF8
  Write-Host $line
}

try {
  if (Test-Path $Log) { Remove-Item -LiteralPath $Log -Force }
  Log '=== video build start ==='
  $wav = Join-Path $Project 'media\voiceover.wav'
  if (-not (Test-Path -LiteralPath $wav)) { throw "Missing WAV: $wav" }
  Log ("WAV OK: {0:N2} MB" -f ((Get-Item -LiteralPath $wav).Length / 1MB))

  Set-Location -LiteralPath $Skill
  if (-not (Test-Path 'node_modules\playwright')) {
    Log 'npm install...'
    & npm install --no-audit --no-fund 2>&1 | ForEach-Object { Log $_ }
    if ($LASTEXITCODE -ne 0) { throw "npm install failed: $LASTEXITCODE" }
  }

  Log 'playwright install chromium...'
  & npx playwright install chromium 2>&1 | ForEach-Object { Log $_ }

  Log 'node cli.js wav --skip-timing-check'
  & node cli.js wav --project $Project --skip-timing-check 2>&1 | ForEach-Object { Log $_ }
  if ($LASTEXITCODE -ne 0) { throw "wav failed: $LASTEXITCODE" }

  if (-not (Test-Path -LiteralPath $Mp4)) { throw "MP4 NOT FOUND: $Mp4" }
  Log ("SUCCESS MP4: {0} ({1:N2} MB)" -f $Mp4, ((Get-Item -LiteralPath $Mp4).Length / 1MB))
  Log '=== video build done ==='
} catch {
  Log ("ERROR: {0}" -f $_.Exception.Message)
  exit 1
}
