
param (
    [string]$TargetDir = "..\test_complexity"
)

$TargetDir = Resolve-Path $TargetDir
Write-Host "Manual Verification Scanning: $TargetDir" -ForegroundColor Cyan

# Initialize counters
$TotalFiles = 0
$Metrics = @{
    "Inline_CSS" = 0
    "Internal_Style" = 0
    "Inline_JS" = 0
    "Ajax_Calls" = 0
    "Internal_Script" = 0
}

# Get all recursively, excluding git/bin/obj
$Files = Get-ChildItem -Path $TargetDir -Recurse -File | Where-Object { 
    $_.FullName -notmatch "\\(\.git|bin|obj|node_modules)\\" -and 
    $_.Extension -match "\.(html|cshtml|js|aspx|php)$"
}

foreach ($File in $Files) {
    $Content = Get-Content $File.FullName -Raw
    $TotalFiles++
    
    # 1. Inline CSS: look for style="..."
    $Matches = $Content | Select-String -Pattern "style\s*=\s*[`"'][^`"']*[`"']" -AllMatches
    if ($Matches) { $Metrics["Inline_CSS"] += $Matches.Matches.Count }

    # 2. Internal Style: <style ...>
    $Matches = $Content | Select-String -Pattern "<style\b" -AllMatches
    if ($Matches) { $Metrics["Internal_Style"] += $Matches.Matches.Count }
    
    # 3. Inline JS: onclick=... or href="javascript:..."
    $Matches = $Content | Select-String -Pattern "(\bon\w+\s*=\s*[`"'][^`"']*[`"']|href=[`"']\s*javascript:)" -AllMatches
    if ($Matches) { $Metrics["Inline_JS"] += $Matches.Matches.Count }

    # 4. Internal Script: <script> without src
    # PS Regex is tricky for negative lookahead in Select-String, doing simple check:
    # We find all <script, then checking if they have src.
    $ScriptTags = $Content | Select-String -Pattern "<script\b[^>]*>" -AllMatches
    foreach ($m in $ScriptTags.Matches) {
        if ($m.Value -notmatch "src=") {
            $Metrics["Internal_Script"]++ 
        }
    }

    # 5. AJAX Calls: comprehensive pattern matching (matches scanner.py exactly)
    # Includes: fetch, XMLHttpRequest, jQuery, axios, .open(), .send(), WebSocket, EventSource
    $AjaxPatterns = @"
(?x)  # Enable verbose mode for readability
(
    \bfetch\s*\(|
    new\s+XMLHttpRequest\s*\(|
    (?:\$|jQuery|axios|superagent|http)\s*\.\s*(?:ajax|get|post|getJSON|getScript|load|request)\s*\(|
    \.open\s*\(\s*["'](?:GET|POST|PUT|DELETE|PATCH)["']|
    \bonreadystatechange\s*=|
    \.send\s*\(|
    \baxios(?:\.\w+)?\s*\(|
    new\s+WebSocket\s*\(|
    new\s+EventSource\s*\(
)
"@
    $Matches = $Content | Select-String -Pattern $AjaxPatterns -AllMatches
    if ($Matches) { $Metrics["Ajax_Calls"] += $Matches.Matches.Count }
}

Write-Host "`n--- PowerShell Manual Check Results ---" -ForegroundColor Yellow
$Metrics.GetEnumerator() | Sort-Object Name | Format-Table -AutoSize
Write-Host "Total Files Scanned: $TotalFiles"

Write-Host "`n--- For Consistency Verification ---" -ForegroundColor Cyan
Write-Host "Run this command to verify against tool output:"
Write-Host "python verify_consistency.py $($Metrics['Inline_CSS']) $($Metrics['Internal_Style']) $($Metrics['Inline_JS']) $($Metrics['Internal_Script']) $($Metrics['Ajax_Calls'])" -ForegroundColor Green
