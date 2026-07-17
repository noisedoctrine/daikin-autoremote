# Daikin AutoRemote Plan

## Goals
- Multi-AC control (Malaysian 2025 models).
- Single-tap "Comfort Profiles".
- Time-based progressions (Timeline).
- PWA/Web UI on RPi 4.

## Structure
- `src/`: Backend (FastAPI), Discovery, Engine.
- `ui/`: Frontend (Vanilla JS/CSS).
- `data/`: Profiles (JSON/DB).
- `docs/`: Specs & Research.

## Tech
- Go (Golang).
- Containerized via Docker for CasaOS.

## IR Specification
- **Hardware**: NPN-driven IR LED on GPIO 17.
- **Protocol**: Daikin ARC480 (Stateful).
- **Communication**: Socket interface to `pigpiod`.
