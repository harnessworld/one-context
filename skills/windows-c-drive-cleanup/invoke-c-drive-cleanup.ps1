#Requires -Version 5.1
<#
.SYNOPSIS
  在用户已通过对话明确授权的前提下，执行白名单内的 C 盘相关清理（缓存/临时/Docker 等）。

.DESCRIPTION
  **无授权不得运行**：必须提供 -ChatAuthorizationNote（用户在聊天中的同意原话，供审计）。
  至少指定一个清理开关。建议清理前后各执行一次 Get-PSDrive C。
  本脚本不卸载「已安装的应用」注册表项；卸载请用系统设置。

.PARAMETER ChatAuthorizationNote
  必填。粘贴用户在对话中同意执行清理的原文（≥8 字符）。

.PARAMETER DryRun
  只打印将执行的步骤，不调用删除/清理命令。

.NOTES
  与 SKILL.md 安全边界一致；未列出的路径请勿在此脚本外批量删除。
#>

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true, HelpMessage = 'Paste the user exact consent message from the chat')]
  [ValidateLength(8, 4000)]
  [string]$ChatAuthorizationNote,

  [switch]$DryRun,

  [switch]$NpmCache,
  [switch]$PipCache,
  [switch]$YarnCache,
  [switch]$PnpmStorePrune,
  [switch]$UserTemp,
  [switch]$LocalAppDataTemp,
  [switch]$RecycleBin,
  [switch]$DockerSystemPrune,
  [switch]$DockerSystemPruneAll,
  [switch]$CondaCleanAll,
  [switch]$DotnetNugetLocalsAllClear,
  [switch]$VisualStudioPackagesCache
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

$any = $NpmCache -or $PipCache -or $YarnCache -or $PnpmStorePrune -or $UserTemp -or $LocalAppDataTemp -or $RecycleBin -or $DockerSystemPrune -or $DockerSystemPruneAll -or $CondaCleanAll -or $DotnetNugetLocalsAllClear -or $VisualStudioPackagesCache

if (-not $any) {
  Write-Error 'Specify at least one cleanup switch (e.g. -NpmCache). Use -DryRun to preview. See SKILL.md.'
  exit 2
}

function Write-CFree {
  try {
    $d = Get-PSDrive -Name C -ErrorAction Stop
    Write-Host ('  C: 已用 {0:N2} GB  可用 {1:N2} GB' -f ($d.Used / 1GB), ($d.Free / 1GB))
  } catch {
    Write-Host '  (无法读取 C: 盘)' -ForegroundColor Yellow
  }
}

function Invoke-Step {
  param([string]$Title, [scriptblock]$Action)
  Write-Host ""
  Write-Host ">> $Title" -ForegroundColor Cyan
  if ($DryRun) {
    Write-Host '   [DryRun] 跳过实际执行' -ForegroundColor DarkGray
    return
  }
  try {
    & $Action
    Write-Host '   完成' -ForegroundColor Green
  } catch {
    Write-Host ('   失败: {0}' -f $_.Exception.Message) -ForegroundColor Yellow
  }
}

Write-Host '=== invoke-c-drive-cleanup（白名单清理）===' -ForegroundColor Cyan
Write-Host ('  授权记录（对话原文摘要前 120 字）: {0}' -f ($ChatAuthorizationNote.Substring(0, [Math]::Min(120, $ChatAuthorizationNote.Length))))
if ($ChatAuthorizationNote.Length -gt 120) { Write-Host '  …' -ForegroundColor DarkGray }
Write-Host ('  模式: {0}' -f ($(if ($DryRun) { 'DryRun' } else { '执行' })))
Write-Host '  清理前 C:' -ForegroundColor DarkGray
Write-CFree

if ($NpmCache) {
  Invoke-Step 'npm cache clean --force' {
    if (-not (Get-Command npm -ErrorAction SilentlyContinue)) { throw 'npm 不在 PATH' }
    & npm cache clean --force
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { throw "npm 退出码 $LASTEXITCODE" }
  }
}

if ($PipCache) {
  Invoke-Step 'pip cache purge' {
    if (-not (Get-Command pip -ErrorAction SilentlyContinue)) { throw 'pip 不在 PATH' }
    & pip cache purge
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { throw "pip 退出码 $LASTEXITCODE" }
  }
}

if ($YarnCache) {
  Invoke-Step 'yarn cache clean' {
    if (-not (Get-Command yarn -ErrorAction SilentlyContinue)) { throw 'yarn 不在 PATH' }
    & yarn cache clean
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { throw "yarn 退出码 $LASTEXITCODE" }
  }
}

if ($PnpmStorePrune) {
  Invoke-Step 'pnpm store prune' {
    if (-not (Get-Command pnpm -ErrorAction SilentlyContinue)) { throw 'pnpm 不在 PATH' }
    & pnpm store prune
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { throw "pnpm 退出码 $LASTEXITCODE" }
  }
}

if ($UserTemp) {
  Invoke-Step '清空 %TEMP% 下文件（保留 Temp 目录本身）' {
    $t = $env:TEMP
    if ([string]::IsNullOrWhiteSpace($t) -or -not (Test-Path -LiteralPath $t)) { throw 'TEMP 无效' }
    Get-ChildItem -LiteralPath $t -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
  }
}

if ($LocalAppDataTemp) {
  Invoke-Step '清空 LocalAppData\Temp 下文件' {
    $lt = Join-Path $env:LOCALAPPDATA 'Temp'
    if (-not (Test-Path -LiteralPath $lt)) { throw 'LocalAppData\Temp 不存在' }
    Get-ChildItem -LiteralPath $lt -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
  }
}

if ($RecycleBin) {
  Invoke-Step '清空回收站（当前用户）' {
    if (-not (Get-Command Clear-RecycleBin -ErrorAction SilentlyContinue)) { throw 'Clear-RecycleBin 不可用' }
    Clear-RecycleBin -Force -ErrorAction Stop
  }
}

if ($DockerSystemPruneAll) {
  Invoke-Step 'docker system prune -a -f（删除未使用镜像/网络等，激进）' {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'docker 不在 PATH' }
    & docker system prune -a -f
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { throw "docker 退出码 $LASTEXITCODE" }
  }
}
elseif ($DockerSystemPrune) {
  Invoke-Step 'docker system prune -f（不删未使用镜像）' {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { throw 'docker 不在 PATH' }
    & docker system prune -f
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { throw "docker 退出码 $LASTEXITCODE" }
  }
}

if ($CondaCleanAll) {
  Invoke-Step 'conda clean -a -y' {
    if (-not (Get-Command conda -ErrorAction SilentlyContinue)) { throw 'conda 不在 PATH' }
    & conda clean -a -y
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { throw "conda 退出码 $LASTEXITCODE" }
  }
}

if ($DotnetNugetLocalsAllClear) {
  Invoke-Step 'dotnet nuget locals all --clear' {
    if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) { throw 'dotnet 不在 PATH' }
    & dotnet nuget locals all --clear
    if ($LASTEXITCODE -ne 0 -and $null -ne $LASTEXITCODE) { throw "dotnet 退出码 $LASTEXITCODE" }
  }
}

if ($VisualStudioPackagesCache) {
  Invoke-Step '删除 Visual Studio Installer 包缓存（ProgramData\...\Packages 内文件）' {
    $vsPkg = 'C:\ProgramData\Microsoft\VisualStudio\Packages'
    if (-not (Test-Path -LiteralPath $vsPkg)) { throw 'VS Packages 目录不存在' }
    Write-Warning '以后修复/增装 VS 组件可能需要重新下载。'
    Get-ChildItem -LiteralPath $vsPkg -Force -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
  }
}

Write-Host ""
Write-Host '  清理后 C:' -ForegroundColor DarkGray
Write-CFree
Write-Host ""
Write-Host '=== 结束 ===' -ForegroundColor Green
if ($DryRun) { Write-Host '本次为 DryRun，未修改磁盘。去掉 -DryRun 且保持授权记录可真正执行。' -ForegroundColor DarkGray }
