# Docker Deployment

Build and start the 8080 gateway stack:

```powershell
docker compose up --build -d web api inference
docker compose ps
```

Open:

```text
http://127.0.0.1:8080
```

For Cloudflare Tunnel with a token:

```powershell
docker compose --profile cloudflare up -d cloudflared
```

Keep `CLOUDFLARE_TUNNEL_TOKEN` in `.env` only.
