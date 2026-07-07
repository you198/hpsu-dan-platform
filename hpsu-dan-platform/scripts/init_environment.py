from __future__ import annotations

import secrets
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / ".env.example"
TARGET = ROOT / ".env"
CREDENTIALS = ROOT / "storage" / "bootstrap-credentials.txt"


def token(length: int = 24) -> str:
    return secrets.token_urlsafe(length)


def main() -> None:
    if TARGET.exists():
        raise SystemExit(".env already exists; refusing to overwrite deployment secrets.")

    admin_password = token()
    guest_password = token()
    replacements = {
        "replace-with-a-long-random-secret": token(48),
        "replace-with-a-strong-admin-password": admin_password,
        "replace-with-a-strong-guest-password": guest_password,
    }
    content = EXAMPLE.read_text(encoding="utf-8")
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    TARGET.write_text(content, encoding="utf-8")

    CREDENTIALS.parent.mkdir(parents=True, exist_ok=True)
    CREDENTIALS.write_text(
        "HPSU-DAN Platform bootstrap credentials\n"
        "Rotate these passwords after the first successful deployment.\n\n"
        f"Admin: admin\nPassword: {admin_password}\n\n"
        f"Guest: guest\nPassword: {guest_password}\n",
        encoding="utf-8",
    )
    print(f"Created {TARGET}")
    print(f"Created {CREDENTIALS}")


if __name__ == "__main__":
    main()

