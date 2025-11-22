#!/usr/bin/env python3
"""Helper to generate `.streamlit/secrets.toml` with an `[auth]` entry.

Usage:
  python scripts/generate_secrets.py --username alice --password secret

This will create (or update) `.streamlit/secrets.toml` with a sha256 password_hash.
"""
import argparse
import hashlib
import os
from pathlib import Path

try:
    import toml
except Exception:
    toml = None


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def write_secrets(username: str, password_hash: str, out_path: Path):
    out_path.parent.mkdir(parents=True, exist_ok=True)
    content = f"[auth]\nusername = \"{username}\"\npassword_hash = \"{password_hash}\"\n"
    out_path.write_text(content, encoding="utf-8")
    print(f"Wrote secrets to {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--out", default=".streamlit/secrets.toml")
    args = parser.parse_args()

    ph = hash_password(args.password)
    out_path = Path(args.out)
    write_secrets(args.username, ph, out_path)
    print("Done. Restart Streamlit and log in with the provided username and password.")


if __name__ == "__main__":
    main()
