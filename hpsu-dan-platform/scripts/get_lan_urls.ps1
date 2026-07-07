$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root ".env"
$port = 8080

if (Test-Path -LiteralPath $envFile) {
    $line = Get-Content -LiteralPath $envFile | Where-Object { $_ -match '^(WEB_PORT|APP_PORT)=' } | Select-Object -First 1
    if ($line) {
        $port = [int](($line -split '=', 2)[1])
    }
}

$addresses = @()

try {
    $addresses = Get-NetIPAddress -AddressFamily IPv4 -ErrorAction Stop |
        Where-Object {
            $_.IPAddress -notlike '127.*' -and
            $_.IPAddress -notlike '169.254.*' -and
            $_.PrefixOrigin -ne 'WellKnown'
        } |
        Sort-Object InterfaceMetric, InterfaceAlias |
        ForEach-Object {
            [pscustomobject]@{ IPAddress = $_.IPAddress; InterfaceAlias = $_.InterfaceAlias }
        }
} catch {
    $addresses = ipconfig |
        Select-String -Pattern 'IPv4.*:\s*([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)' |
        ForEach-Object {
            $ip = $_.Matches[0].Groups[1].Value
            if ($ip -notlike '127.*' -and $ip -notlike '169.254.*') {
                [pscustomobject]@{ IPAddress = $ip; InterfaceAlias = 'ipconfig' }
            }
        }
}

Write-Host "Local: http://127.0.0.1:$port"
foreach ($address in $addresses) {
    Write-Host ("LAN:   http://{0}:{1}  ({2})" -f $address.IPAddress, $port, $address.InterfaceAlias)
}

Write-Host ""
Write-Host "If LAN devices cannot connect, allow TCP port $port in Windows Firewall."
