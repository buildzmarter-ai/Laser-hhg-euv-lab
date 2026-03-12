# Laser-HHG-EUV Lab: Distributed Lithography Architecture

This repository contains the interactive simulation stack for a **Chip-Scale Coherent EUV Source**. It provides a FastAPI backend for modeling high-harmonic generation (HHG), optical propagation, and resist exposure.

## Overview

- **Architectures**: Various lithography approaches including VCSEL/MEMS writers, UV semiconductor heads, cold-atom Rydberg HHG sources, and micro-FEL EUV sources.
- **Physics Engines**: HHG generation, dose control, stitching, and more are implemented under `backend/`.

## Quickstart

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   uvicorn app:app --reload
   ```
3. Open `http://127.0.0.1:8000/docs` to view the API documentation.

## API Endpoints

* `GET /api/fleet-economics` – sample cost and power metrics.
* `POST /api/simulate` – placeholder for exposure pipeline simulation (uses a dummy resist model).

## Development Notes

- Backend modules live in `backend/` and can be imported into `app.py` as needed.
- Use `uvicorn --reload` during development to auto-reload code changes.

## Building

No build step is required beyond installing Python dependencies. For production use, containerize the service or create a package as needed.

## License

[Add your license here]
