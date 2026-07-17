# Daikin AutoRemote

Local Daikin air-conditioner control experiments for Raspberry Pi and pigpio.

## Private configuration

Copy `secrets/local.example.yaml` to `secrets/local.yaml` and edit the local copy. The private file is ignored by Git and may contain LAN addresses, SSH details, room names, and GPIO assignments.

Do not store passwords, access tokens, API keys, private keys, or certificates in the repository. Use environment variables or a credential manager for credentials.

## Python setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.main
```

The API binds to `127.0.0.1:8000` by default. Change this only on a trusted network and add authentication before exposing it beyond the local machine.

## Git safety check

Before committing, run:

```bash
git status --short --ignored
git check-ignore -v secrets/local.yaml data/units.json data/profiles.json
```
