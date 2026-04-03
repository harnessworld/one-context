#Requires -Version 5.1
<#
.SYNOPSIS
  Read-only survey of common C: disk space hints (no deletes, no prunes).

.PARAMETER Quick
  If set, only checks whether candidate paths exist (no recursive size scan).

.NOTES
  Full mode: large directories may take a long time; Ctrl+C to abort.
  Per skill-windows-c-drive-cleanup spec: this script must NOT perform batch deletes.
#>

[CmdletBinding()]
param(
  [switch]$Quick
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

function Format-Gb([double]$bytes) {
  if ($null -eq $bytes -or [double]::IsNaN($bytes)) { return 'n/a' }
  '{0:N2} GB' -f ($bytes / 1GB)
}

function Get-DirSizeBytes {
  param([string]$LiteralPath)
  if (-not (Test-Path -LiteralPath $LiteralPath)) { return $null }
  try {
    $sum = (Get-ChildItem -LiteralPath $LiteralPath -Recurse -Force -ErrorAction SilentlyContinue |
      Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    return $sum
  } catch {
    return $null
  }
}

Write-Host '=== C: drive (read-only) ===' -ForegroundColor Cyan
try {
  $d = Get-PSDrive -Name C -ErrorAction Stop
  Write-Host ('  Used: {0}  Free: {1}' -f (Format-Gb $d.Used), (Format-Gb $d.Free))
} catch {
  Write-Host '  Could not read PS drive C:' -ForegroundColor Yellow
}

$extraPaths = @()

if (Get-Command npm -ErrorAction SilentlyContinue) {
  try {
    $npmCache = (npm config get cache 2>$null).Trim()
    if ($npmCache -and (Test-Path -LiteralPath $npmCache)) { $extraPaths += $npmCache }
  } catch { }
}

if (Get-Command pip -ErrorAction SilentlyContinue) {
  try {
    $pipOut = & pip cache dir 2>$null
    if ($LASTEXITCODE -eq 0 -and $pipOut) {
      $pipCache = ($pipOut | Select-Object -First 1).Trim()
      if ($pipCache -and (Test-Path -LiteralPath $pipCache)) { $extraPaths += $pipCache }
    }
  } catch { }
}

if (Get-Command conda -ErrorAction SilentlyContinue) {
  try {
    $condaBase = (& conda info --base 2>$null)
    if ($LASTEXITCODE -eq 0 -and $condaBase) {
      $condaBase = ($condaBase | Select-Object -First 1).Trim()
      if ($condaBase) {
        $pkgs = Join-Path $condaBase 'pkgs'
        if (Test-Path -LiteralPath $pkgs) { $extraPaths += $pkgs }
      }
    }
  } catch { }
}

$candidates = @(
  @{ Label = 'USER TEMP'; Path = $env:TEMP },
  @{ Label = 'LOCALAPPDATA Temp'; Path = (Join-Path $env:LOCALAPPDATA 'Temp') },
  @{ Label = 'Windows Temp'; Path = 'C:\Windows\Temp' },
  @{ Label = 'Local npm-cache (default)'; Path = (Join-Path $env:LOCALAPPDATA 'npm-cache') },
  @{ Label = 'pnpm store (common)'; Path = (Join-Path $env:LOCALAPPDATA 'pnpm\store') },
  @{ Label = 'Yarn Berry cache (common)'; Path = (Join-Path $env:LOCALAPPDATA 'Yarn\Berry\cache') },
  @{ Label = 'NuGet HTTP cache'; Path = (Join-Path $env:LOCALAPPDATA 'NuGet\v3-cache') },
  @{ Label = 'Docker ProgramData'; Path = 'C:\ProgramData\Docker' },
  @{ Label = 'VS Installer packages cache (common)'; Path = 'C:\ProgramData\Microsoft\VisualStudio\Packages' }
)

foreach ($p in $extraPaths) {
  $candidates += @{ Label = 'extra (tool-detected)'; Path = $p }
}

if ($Quick) {
  Write-Host "`n=== Candidate paths (-Quick: existence only, no size scan) ===" -ForegroundColor Cyan
} else {
  Write-Host "`n=== Candidate paths (recursive size; may be slow) ===" -ForegroundColor Cyan
}

$seen = @{}
foreach ($item in $candidates) {
  $path = $item.Path
  if ([string]::IsNullOrWhiteSpace($path)) { continue }
  $key = $path.ToLowerInvariant()
  if ($seen.ContainsKey($key)) { continue }
  $seen[$key] = $true

  Write-Host ("`n[{0}]" -f $item.Label) -ForegroundColor DarkCyan
  Write-Host ("  {0}" -f $path)
  if (-not (Test-Path -LiteralPath $path)) {
    Write-Host '  (missing or inaccessible)' -ForegroundColor DarkGray
    continue
  }
  if ($Quick) {
    Write-Host '  Status: exists (run without -Quick for recursive size)' -ForegroundColor Green
    continue
  }
  $bytes = Get-DirSizeBytes -LiteralPath $path
  if ($null -eq $bytes) {
    Write-Host '  Size: (could not measure: permissions or errors)' -ForegroundColor Yellow
  } else {
    Write-Host ('  Size: {0}' -f (Format-Gb $bytes))
  }
}

Write-Host "`n=== Done (read-only; no files were deleted) ===" -ForegroundColor Green
Write-Host 'Any cleanup requires explicit user authorization per SKILL.md.' -ForegroundColor DarkGray
