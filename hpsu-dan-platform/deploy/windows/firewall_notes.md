# Windows LAN Access

The local web gateway listens on `0.0.0.0:8080`.

Use:

```powershell
.\scripts\get_lan_urls.ps1
```

Then open the reported LAN URL from another device on the same network.

If the page is not reachable, allow inbound TCP 8080 in Windows Defender Firewall:

```powershell
New-NetFirewallRule -DisplayName "HPSU-DAN Platform 8080" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow
```

Only expose the web gateway port. Keep API `8000` and inference `8010` local-only for development.
