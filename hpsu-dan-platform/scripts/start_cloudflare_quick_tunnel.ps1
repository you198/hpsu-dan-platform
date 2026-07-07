$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$cloudflared = Join-Path $root "cloudflared-windows-amd64.exe"
$envFile = Join-Path $root ".env"
$port = 8080

if (Test-Path -LiteralPath $envFile) {
    $line = Get-Content -LiteralPath $envFile | Where-Object { $_ -match '^(WEB_PORT|APP_PORT)=' } | Select-Object -First 1
    if ($line) {
        $port = [int](($line -split '=', 2)[1])
    }
}

if (-not (Test-Path -LiteralPath $cloudflared)) {
    throw "Missing cloudflared executable: $cloudflared"
}

Write-Host "Starting Cloudflare quick tunnel for http://127.0.0.1:$port"
Write-Host "Keep this window open while presenting."
& $cloudflared tunnel --url "http://127.0.0.1:$port"
