#Requires -Version 5.1
<#
.SYNOPSIS
  只读生成 C 盘空间「产品化」报告：目录维度、应用维度、体积 + 最近修改 + 建议动作。

.DESCRIPTION
  不写磁盘、不删除。默认跳过对整棵 C:\Windows 的递归（极慢）；可 -IncludeWindowsFull 全量扫描。
  应用体积来自「卸载」注册表 EstimatedSize（KB），可能与真实占用有偏差。

.PARAMETER IncludeWindowsFull
  递归统计整个 %SystemRoot%（可能非常慢）。

.PARAMETER MaxApps
  注册表中按预估体积排序后最多显示条数（默认 40）。

.PARAMETER MaxProfileSubs
  LocalAppData / Roaming 下一级子目录各取 Top N（默认 20）。

.PARAMETER IncludeProgramFilesBreakdown
  额外统计 C:\Program Files 与 Program Files (x86) 下一级子目录体积（较慢，便于按「应用安装目录」决策）。

.NOTES
  删除授权仍按 SKILL.md：本脚本仅枚举与建议。
#>

[CmdletBinding()]
param(
  [switch]$IncludeWindowsFull,
  [switch]$IncludeProgramFilesBreakdown,
  [int]$MaxApps = 40,
  [int]$MaxProfileSubs = 20,
  [int]$MaxProgramFileSubs = 25
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

function Format-Gb([double]$bytes) {
  if ($null -eq $bytes -or [double]::IsNaN([double]$bytes)) { return 'n/a' }
  '{0:N2} GB' -f ([double]$bytes / 1GB)
}

function Format-Mb([double]$bytes) {
  if ($null -eq $bytes -or [double]::IsNaN([double]$bytes)) { return 'n/a' }
  if ($bytes -ge 1GB) { return (Format-Gb $bytes) }
  '{0:N0} MB' -f ($bytes / 1MB)
}

function Get-DirSizeBytes {
  param([string]$LiteralPath)
  if (-not (Test-Path -LiteralPath $LiteralPath)) { return $null }
  try {
    $sum = (Get-ChildItem -LiteralPath $LiteralPath -Recurse -Force -ErrorAction SilentlyContinue |
      Measure-Object -Property Length -Sum -ErrorAction SilentlyContinue).Sum
    if ($null -eq $sum) { return 0 }
    return [double]$sum
  } catch {
    return $null
  }
}

function Get-DirMeta {
  param([string]$LiteralPath)
  $bytes = Get-DirSizeBytes -LiteralPath $LiteralPath
  $lw = $null
  try {
    if (Test-Path -LiteralPath $LiteralPath) {
      $lw = (Get-Item -LiteralPath $LiteralPath -Force -ErrorAction SilentlyContinue).LastWriteTime
    }
  } catch { }
  [pscustomobject]@{
    Path         = $LiteralPath
    SizeBytes    = $bytes
    LastWrite    = $lw
  }
}

function Write-Section([string]$Title) {
  Write-Host ""
  Write-Host "=== $Title ===" -ForegroundColor Cyan
}

function Get-DirHint {
  param([string]$PathLower)
  if ($PathLower -match '^c:\\windows$') { return '系统目录; 默认未扫整树; 用 设置→存储; 勿手删 WinSxS' }
  if ($PathLower -match '^c:\\programdata$') { return '程序共享数据; 先定位子文件夹再决定; 服务相关勿盲删' }
  if ($PathLower -match '^c:\\users$') { return '各用户配置与资料; 看本节 AppData 细分; 文档/下载须点名授权' }
  if ($PathLower -match '\\windows\\winsxs') { return '勿手删; 仅用 DISM 官方清理' }
  if ($PathLower -match '\\windows\\softwaredistribution') { return '更新缓存; 勿在更新中动; 须授权+管理员' }
  if ($PathLower -match '\\windows\\temp') { return '系统临时; cleanmgr 或存储→临时文件' }
  if ($PathLower -match '\\windows\\installer') { return 'MSI 缓存; 勿乱删; 可用疑难解答或工具' }
  if ($PathLower -match '\\program files \(x86\)') { return '优先「设置→应用」卸载对应程序' }
  if ($PathLower -match '\\program files\\') { return '优先「设置→应用」卸载对应程序' }
  if ($PathLower -match '^c:\\program files$') { return '优先「设置→应用」卸载对应程序' }
  if ($PathLower -match '\\users\\[^\\]+\\appdata\\local\\temp') { return '可清临时文件; 关闭占用程序后删; 须授权' }
  if ($PathLower -match '\\users\\[^\\]+\\downloads') { return '默认不碰; 仅当你点名并授权' }
  if ($PathLower -match 'npm-cache') { return 'npm cache clean --force; 须授权' }
  if ($PathLower -match '\\pnpm\\store') { return 'pnpm store prune; 须授权' }
  if ($PathLower -match 'pip\\cache') { return 'pip cache purge; 须授权' }
  if ($PathLower -match 'visualstudio\\packages') { return 'VS Installer 清理缓存; 删则以后可能要重下' }
  if ($PathLower -match '\\docker') { return 'Docker Desktop / docker system df; prune 须授权' }
  if ($PathLower -match '\\wsl($|\\)') { return 'WSL 虚拟磁盘; 压缩/清理见 SKILL 高风险附录; 须授权' }
  if ($PathLower -match '\\users\\') { return '看下方 AppData 细分与大应用' }
  return '看路径性质; 不确定则用存储感知或先备份'
}

function Get-AppHint {
  param([string]$Name, [string]$Loc)
  $n = ($Name + ' ' + $Loc).ToLowerInvariant()
  if ($n -match 'visual studio|vs_') { return 'Visual Studio Installer → 修改/卸载工作负载' }
  if ($n -match 'docker') { return 'Docker Desktop → 清理 / docker system prune' }
  if ($n -match 'android studio|sdk') { return 'SDK Manager 删平台镜像; 或卸载重装' }
  if ($n -match 'office|microsoft 365') { return '设置→应用 卸载或联机修复' }
  if ($n -match 'game|steam|epic|battle') { return '平台内删游戏或移动库盘' }
  return '设置 → 应用 → 已安装的应用 → 卸载'
}

function Get-AppDataPlaybookEntry {
  param([string]$FullPath, [double]$SizeBytes, [string]$Layer, [string]$Name)
  if ($null -eq $SizeBytes -or [double]::IsNaN($SizeBytes)) { return $null }
  $pl = $FullPath.ToLowerInvariant()
  $szPretty = if ($SizeBytes -ge 1GB) { Format-Gb $SizeBytes } else { Format-Mb $SizeBytes }
  $who = 'AppData\{0}\{1}' -f $Layer, $Name

  if ($pl -match 'npm-cache') {
    return [pscustomobject]@{ Text = ('[{0} ≈{1}] npm 全局缓存。' -f $who, $szPretty); AutoSwitches = @('NpmCache') }
  }
  if ($pl -match '[\\/]pnpm[\\/]store') {
    return [pscustomobject]@{ Text = ('[{0} ≈{1}] pnpm 全局 store。' -f $who, $szPretty); AutoSwitches = @('PnpmStorePrune') }
  }
  if ($pl -match '[\\/]pip[\\/]cache') {
    return [pscustomobject]@{ Text = ('[{0} ≈{1}] pip 下载缓存。' -f $who, $szPretty); AutoSwitches = @('PipCache') }
  }
  if ($pl -match '[\\/]yarn[\\/]berry[\\/]cache') {
    return [pscustomobject]@{ Text = ('[{0} ≈{1}] Yarn Berry 缓存。' -f $who, $szPretty); AutoSwitches = @('YarnCache') }
  }
  if ($pl -match '\\appdata\\local\\temp$') {
    return [pscustomobject]@{
      Text         = ('[{0} ≈{1}] 临时目录（多为 %TEMP%）。优先 **设置→存储→临时文件**；若命令行清理须先关占用程序。' -f $who, $szPretty)
      AutoSwitches = @('UserTemp')
    }
  }
  if ($pl -match '[\\/]wsl($|\\)') {
    return [pscustomobject]@{
      Text         = ('[{0} ≈{1}] WSL 虚拟磁盘：**无法**用本 skill 脚本自动压缩。先 wsl --shutdown，再按 SKILL「WSL 高风险附录」操作（须单独授权）。' -f $who, $szPretty)
      AutoSwitches = @()
    }
  }
  if ($pl -match '[\\/]docker') {
    return [pscustomobject]@{
      Text         = ('[{0} ≈{1}] Docker 数据：可在 **Docker Desktop** 里清理；命令行授权后可用 **-DockerSystemPrune**（更彻底用 **-DockerSystemPruneAll**，会删未用镜像）。' -f $who, $szPretty)
      AutoSwitches = @('DockerSystemPrune')
    }
  }
  if ($pl -match 'android') {
    return [pscustomobject]@{
      Text         = ('[{0} ≈{1}] Android/SDK：**须手动** 打开 Android Studio → SDK Manager 删不用的系统镜像，或从 **设置→应用** 卸载 Android Studio。' -f $who, $szPretty)
      AutoSwitches = @()
    }
  }
  if ($pl -match 'steam') {
    return [pscustomobject]@{
      Text         = ('[{0} ≈{1}] Steam 游戏文件：**须手动** 在 Steam 客户端卸载游戏或将库移到其它盘。' -f $who, $szPretty)
      AutoSwitches = @()
    }
  }
  if ($pl -match 'nuget') {
    return [pscustomobject]@{ Text = ('[{0} ≈{1}] NuGet/dotnet 本地缓存。' -f $who, $szPretty); AutoSwitches = @('DotnetNugetLocalsAllClear') }
  }
  return $null
}

Write-Section '摘要 · C: 盘'
try {
  $d = Get-PSDrive -Name C -ErrorAction Stop
  Write-Host ('  已用: {0}   可用: {1}' -f (Format-Gb $d.Used), (Format-Gb $d.Free))
} catch {
  Write-Host '  无法读取 C: 盘信息' -ForegroundColor Yellow
}

$sysRoot = $env:SystemRoot
if ([string]::IsNullOrWhiteSpace($sysRoot)) { $sysRoot = 'C:\Windows' }

Write-Section '一、目录维度 · C:\ 根目录（按体积降序）'
$cRoots = @()
try {
  $kids = Get-ChildItem -LiteralPath 'C:\' -Directory -Force -ErrorAction Stop
} catch {
  $kids = @()
  Write-Host '  无法枚举 C:\ 根目录（权限？）' -ForegroundColor Yellow
}

foreach ($dir in $kids) {
  $full = $dir.FullName
  $name = $dir.Name
  Write-Verbose ("  正在统计: {0}" -f $full)

  if ($name -eq 'Windows' -and -not $IncludeWindowsFull) {
    $winHot = @(
      (Join-Path $sysRoot 'Temp'),
      (Join-Path $sysRoot 'SoftwareDistribution\Download'),
      (Join-Path $sysRoot 'Logs'),
      (Join-Path $sysRoot 'Installer')
    )
    $partial = 0.0
    foreach ($hp in $winHot) {
      if (-not (Test-Path -LiteralPath $hp)) { continue }
      $b = Get-DirSizeBytes -LiteralPath $hp
      if ($null -ne $b) { $partial += $b }
    }
    $cRoots += [pscustomobject]@{
      Path      = $full
      SizeBytes = $partial
      LastWrite = (Get-Item -LiteralPath $full -Force -ErrorAction SilentlyContinue).LastWriteTime
      Note      = '部分（Temp/SoftwareDistribution\Download/Logs/Installer）；非整棵 Windows。加 -IncludeWindowsFull 可全量（很慢）'
    }
    continue
  }

  $meta = Get-DirMeta -LiteralPath $full
  $note = ''
  if ($name -eq 'Windows' -and $IncludeWindowsFull) { $note = '全量递归 Windows' }
  $cRoots += [pscustomobject]@{
    Path      = $meta.Path
    SizeBytes = $meta.SizeBytes
    LastWrite = $meta.LastWrite
    Note      = $note
  }
}

$cSorted = $cRoots | Sort-Object { if ($_.SizeBytes -is [double]) { $_.SizeBytes } else { 0 } } -Descending
$pfTopForPlaybook = @()
foreach ($row in $cSorted) {
  $pl = $row.Path.ToLowerInvariant()
  $hint = Get-DirHint -PathLower $pl
  $sz = if ($null -eq $row.SizeBytes) { 'n/a' } else { Format-Gb $row.SizeBytes }
  $lw = if ($row.LastWrite) { $row.LastWrite.ToString('yyyy-MM-dd HH:mm') } else { 'n/a' }
  Write-Host ""
  Write-Host ('  [{0}]' -f $sz) -ForegroundColor Yellow -NoNewline
  Write-Host ('  {0}' -f $row.Path)
  Write-Host ('        最近修改(文件夹): {0}' -f $lw)
  Write-Host ('        建议: {0}' -f $hint)
  if ($row.Note) { Write-Host ('        说明: {0}' -f $row.Note) -ForegroundColor DarkGray }
}

if ($IncludeProgramFilesBreakdown) {
  Write-Section '目录维度 · Program Files 下大户（一级子目录，按体积）'
  $pfRoots = @('C:\Program Files', 'C:\Program Files (x86)')
  $pfRows = @()
  foreach ($pfr in $pfRoots) {
    if (-not (Test-Path -LiteralPath $pfr)) { continue }
    Write-Host ("  根: {0}" -f $pfr) -ForegroundColor DarkCyan
    Get-ChildItem -LiteralPath $pfr -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
      Write-Verbose ("    Program Files 子项: {0}" -f $_.Name)
      $m = Get-DirMeta -LiteralPath $_.FullName
      $pfRows += [pscustomobject]@{
        Root      = $pfr
        Name      = $_.Name
        FullPath  = $m.Path
        SizeBytes = $m.SizeBytes
        LastWrite = $m.LastWrite
      }
    }
  }
  $pfTop = $pfRows | Sort-Object { if ($_.SizeBytes -is [double]) { $_.SizeBytes } else { 0 } } -Descending | Select-Object -First $MaxProgramFileSubs
  $pfTopForPlaybook = @($pfTop)
  foreach ($r in $pfTop) {
    $sz = if ($null -eq $r.SizeBytes) { 'n/a' } else { Format-Gb $r.SizeBytes }
    $lw = if ($r.LastWrite) { $r.LastWrite.ToString('yyyy-MM-dd') } else { 'n/a' }
    Write-Host ('  [{0}] {1}\{2}  修改:{3}' -f $sz, $r.Root, $r.Name, $lw)
    Write-Host ('        建议: 对应程序请用「设置→应用」卸载；勿只删文件夹。') -ForegroundColor DarkGray
  }
}

Write-Section '二、目录维度 · 当前用户 AppData（一级子目录 Top，按体积）'
$allAppDataHits = @()
$profileBases = @(
  @{ Name = 'Local';   Path = $env:LOCALAPPDATA },
  @{ Name = 'Roaming'; Path = $env:APPDATA }
)

foreach ($pb in $profileBases) {
  $base = $pb.Path
  Write-Host ""
  Write-Host ("  --- {0} ({1}) ---" -f $pb.Name, $base) -ForegroundColor DarkCyan
  if (-not (Test-Path -LiteralPath $base)) {
    Write-Host '  (路径不存在)' -ForegroundColor DarkGray
    continue
  }
  $subs = @()
  Get-ChildItem -LiteralPath $base -Directory -Force -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Verbose ("    AppData 子目录: {0}" -f $_.Name)
    $m = Get-DirMeta -LiteralPath $_.FullName
    $subs += [pscustomobject]@{
      Name      = $_.Name
      FullPath  = $m.Path
      SizeBytes = $m.SizeBytes
      LastWrite = $m.LastWrite
    }
  }
  $top = $subs | Sort-Object { if ($_.SizeBytes -is [double]) { $_.SizeBytes } else { 0 } } -Descending | Select-Object -First $MaxProfileSubs
  foreach ($t in $top) {
    $allAppDataHits += [pscustomobject]@{
      Layer     = $pb.Name
      Name      = $t.Name
      FullPath  = $t.FullPath
      SizeBytes = $t.SizeBytes
    }
    $sz = if ($null -eq $t.SizeBytes) { 'n/a' } else { Format-Mb $t.SizeBytes }
    $lw = if ($t.LastWrite) { $t.LastWrite.ToString('yyyy-MM-dd') } else { 'n/a' }
    $hint = Get-DirHint -PathLower ($t.FullPath.ToLowerInvariant())
    Write-Host ('    {0,-28} {1,12}  修改:{2}  | {3}' -f $t.Name, $sz, $lw, $hint)
  }
}

Write-Section '三、应用维度 · 已安装程序（注册表预估大小，降序）'
$uninstallKeys = @(
  'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall',
  'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall',
  'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall'
)
$apps = @{}
foreach ($uk in $uninstallKeys) {
  if (-not (Test-Path -LiteralPath $uk)) { continue }
  Get-ChildItem -LiteralPath $uk -ErrorAction SilentlyContinue | ForEach-Object {
    $p = Get-ItemProperty -LiteralPath $_.PSPath -ErrorAction SilentlyContinue
    if (-not $p) { return }
    if ([string]::IsNullOrWhiteSpace($p.DisplayName)) { return }
    if ($p.SystemComponent -eq 1) { return }
    $loc = [string]$p.InstallLocation
    if ([string]::IsNullOrWhiteSpace($loc)) { $loc = '' }
    $key = ($p.DisplayName.Trim() + '|' + $loc)
    if ($apps.ContainsKey($key)) { return }
    $sizeKb = 0
    if ($null -ne $p.EstimatedSize) { try { $sizeKb = [int]$p.EstimatedSize } catch { $sizeKb = 0 } }
    $apps[$key] = [pscustomobject]@{
      DisplayName     = $p.DisplayName.Trim()
      Publisher       = [string]$p.Publisher
      EstimatedSizeKB = $sizeKb
      InstallLocation = $loc
      InstallDate     = [string]$p.InstallDate
      UninstallString = [string]$p.UninstallString
    }
  }
}

$appList = $apps.Values | Where-Object { $_.EstimatedSizeKB -gt 0 } | Sort-Object EstimatedSizeKB -Descending | Select-Object -First $MaxApps
foreach ($a in $appList) {
  $bytesEst = [double]$a.EstimatedSizeKB * 1024
  $gb = Format-Gb $bytesEst
  $hint = Get-AppHint -Name $a.DisplayName -Loc $a.InstallLocation
  Write-Host ""
  Write-Host ('  [{0}] {1}' -f $gb, $a.DisplayName) -ForegroundColor Yellow
  if ($a.Publisher) { Write-Host ('        发布者: {0}' -f $a.Publisher) }
  if ($a.InstallLocation) { Write-Host ('        安装位置: {0}' -f $a.InstallLocation) }
  if ($a.InstallDate) { Write-Host ('        安装日期(注册表): {0}' -f $a.InstallDate) }
  Write-Host ('        建议: {0}' -f $hint)
}

Write-Section '四、如何行动（摘要）'
Write-Host @'
  · 本 skill 的交付方式：下方「五」拆成 **A 可自动（你授权后代为执行）** 与 **B 须你手动**。
  · 目录/应用明细仍看「一」「二」「三」。
'@

Write-Section '五、交付清单 · 自动清理 vs 手动清理'
Write-Host '  A 类：你在对话里**逐条说清同意哪些项**后，由代理在仓库根运行 `invoke-c-drive-cleanup.ps1`（可先 `-DryRun`）。' -ForegroundColor DarkGray
Write-Host '  B 类：系统界面或第三方客户端内操作，脚本无法可靠代替。' -ForegroundColor DarkGray
Write-Host ''

$seenPlaybookPaths = @{}
$autoRows = New-Object System.Collections.Generic.List[object]
$manualRows = New-Object System.Collections.Generic.List[string]
$suggestedSwitches = [System.Collections.Generic.HashSet[string]]::new()

$adataOrdered = $allAppDataHits | Where-Object { $_.SizeBytes -is [double] } | Sort-Object SizeBytes -Descending
$autoCap = 12
foreach ($h in $adataOrdered) {
  $key = $h.FullPath.ToLowerInvariant()
  if ($seenPlaybookPaths.ContainsKey($key)) { continue }
  $ent = Get-AppDataPlaybookEntry -FullPath $h.FullPath -SizeBytes ([double]$h.SizeBytes) -Layer $h.Layer -Name $h.Name
  if (-not $ent) { continue }
  $seenPlaybookPaths[$key] = $true
  if ($ent.AutoSwitches -and $ent.AutoSwitches.Count -gt 0) {
    if ($autoRows.Count -lt $autoCap) {
      foreach ($sw in $ent.AutoSwitches) { [void]$suggestedSwitches.Add($sw) }
      $swLabel = '-' + ($ent.AutoSwitches -join ' -')
      $autoRows.Add([pscustomobject]@{ Line = ('  · {0}  [invoke: {1}]' -f $ent.Text, $swLabel) })
    }
  } else {
    $manualRows.Add($ent.Text)
  }
}

$genericLeft = 2
foreach ($h in $adataOrdered) {
  if ($genericLeft -le 0) { break }
  $key = $h.FullPath.ToLowerInvariant()
  if ($seenPlaybookPaths.ContainsKey($key)) { continue }
  if ($null -eq $h.SizeBytes -or $h.SizeBytes -lt 3GB) { continue }
  $seenPlaybookPaths[$key] = $true
  $szPretty = if ($h.SizeBytes -ge 1GB) { Format-Gb $h.SizeBytes } else { Format-Mb $h.SizeBytes }
  $who = 'AppData\{0}\{1}' -f $h.Layer, $h.Name
  $manualRows.Add(('[{0} ≈{1}] **须手动**：资源管理器打开路径确认归属 → 软件内清理缓存或 **设置→应用** 卸载；勿盲删整夹。' -f $who, $szPretty))
  $genericLeft--
}

Write-Section '五-A · 许可后 · 可由代理自动执行（invoke-c-drive-cleanup.ps1）'
if ($autoRows.Count -eq 0) {
  Write-Host '  （本机 AppData 大户未命中内置「可脚本化」规则；仍可对 npm/pip 等单独授权后手动指定开关，见 SKILL。）' -ForegroundColor DarkGray
} else {
  foreach ($r in $autoRows) { Write-Host $r.Line }
  $orderedSw = @($suggestedSwitches | Sort-Object)
  $swArgs = ($orderedSw | ForEach-Object { '-' + $_ }) -join ' '
  Write-Host ''
  Write-Host '  示例（在 **one-context 仓库根**；`ChatAuthorizationNote` 填你在对话里的**同意原文**）：' -ForegroundColor DarkCyan
  Write-Host ('  .\skills\windows-c-drive-cleanup\invoke-c-drive-cleanup.ps1 -ChatAuthorizationNote ''<粘贴同意原文>'' {0} -DryRun' -f $swArgs)
  Write-Host '  上列开关是本机**命中项的并集**；**实跑时只保留你在对话里逐条同意的那几个**，不要照抄全部。' -ForegroundColor Yellow
  Write-Host '  确认 DryRun 输出无误后去掉 -DryRun 再执行。' -ForegroundColor DarkGray
}

Write-Section '五-B · 须你本机手动（界面 / 客户端 / 高风险附录）'
$mIdx = 1
Write-Host ("  {0}. **设置 → 系统 → 存储 → 临时文件** — 勾选后清理（微软官方入口，优先做）。" -f $mIdx)
$mIdx++

try {
  $cFree = (Get-PSDrive -Name C -ErrorAction Stop).Free
  if ($cFree -lt 10GB) {
    Write-Host ("  {0}. C: 可用仅约 **{1}** — 建议今天内完成存储清理，并处理五-A 或下方卸载。" -f $mIdx, (Format-Gb $cFree))
    $mIdx++
  }
} catch { }

foreach ($txt in $manualRows) {
  Write-Host ("  {0}. {1}" -f $mIdx, $txt)
  $mIdx++
}

foreach ($row in $cSorted) {
  $leaf = Split-Path -Leaf $row.Path
  if ($leaf -ne 'Users') { continue }
  if ($null -eq $row.SizeBytes -or $row.SizeBytes -lt 15GB) { continue }
  Write-Host ("  {0}. **C:\Users** 合计约 **{1}** — 对照「二」；桌面/文档/下载勿盲删。" -f $mIdx, (Format-Gb $row.SizeBytes))
  $mIdx++
  break
}

if ($pfTopForPlaybook.Count -gt 0) {
  foreach ($r in ($pfTopForPlaybook | Sort-Object { if ($_.SizeBytes -is [double]) { $_.SizeBytes } else { 0 } } -Descending | Select-Object -First 2)) {
    if ($null -eq $r.SizeBytes -or $r.SizeBytes -lt 1GB) { continue }
    Write-Host ("  {0}. **{1}\{2}** ≈ **{3}** — **设置→应用** 卸载对应程序（勿只删文件夹）。" -f $mIdx, $r.Root, $r.Name, (Format-Gb $r.SizeBytes))
    $mIdx++
  }
}

$appPick = @($appList | Select-Object -First 3)
if ($appPick.Count -eq 0) {
  Write-Host ("  {0}. 注册表无可靠体积字段时：**设置 → 应用 → 已安装的应用** 自行查找卸载。" -f $mIdx)
  $mIdx++
} else {
  foreach ($a in $appPick) {
    $bytesEst = [double]$a.EstimatedSizeKB * 1024
    Write-Host ("  {0}. 不需要 **{1}**（预估 **{2}**）→ **设置→应用** 卸载。" -f $mIdx, $a.DisplayName, (Format-Gb $bytesEst))
    $mIdx++
  }
}

if (-not $IncludeProgramFilesBreakdown) {
  Write-Host ("  {0}. 需要 **Program Files 谁最大**：重跑本报告并加 **-IncludeProgramFilesBreakdown**。" -f $mIdx)
}

Write-Host ''
Write-Host '  其它：管理员 **cleanmgr / DISM**、**VS Installer 包缓存**（-VisualStudioPackagesCache）、**conda**（-CondaCleanAll）、**回收站**（-RecycleBin）等见 SKILL「可自动清理」表；均须在对话**点名授权**后再跑 invoke。' -ForegroundColor DarkGray

Write-Host ''
Write-Host '=== 报告结束（只读；未删除任何文件）===' -ForegroundColor Green
Write-Host '自动清理仅通过 invoke-c-drive-cleanup.ps1，且必须带你在对话中的同意原文。' -ForegroundColor DarkGray
