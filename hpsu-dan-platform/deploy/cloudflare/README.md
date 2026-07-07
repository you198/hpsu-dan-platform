# Cloudflare Tunnel

Quick tunnel for temporary demos:

```powershell
.\scripts\start_cloudflare_quick_tunnel.ps1
```

Named tunnel for stable demos:

1. Create a Cloudflare tunnel in the Cloudflare dashboard or with `cloudflared tunnel create`.
2. Copy `deploy/cloudflare/tunnel.example.yml` to your Cloudflare config path.
3. Replace `HPSU_DAN_TUNNEL_ID`, credentials path, and hostname.
4. Route the hostname to `http://127.0.0.1:8080`.

Keep `TENCENT_LLM_API_KEY`, tunnel tokens, and credentials out of source control.
