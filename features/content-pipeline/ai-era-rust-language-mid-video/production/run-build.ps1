# Wrapper — canonical script: skills/html-video-from-slides/scripts/run-wav-build.ps1
$SkillScript = Join-Path $PSScriptRoot '..\..\..\..\skills\html-video-from-slides\scripts\run-wav-build.ps1'
& $SkillScript -Project $PSScriptRoot @args
