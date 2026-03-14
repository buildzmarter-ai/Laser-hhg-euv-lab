# Laser-HHG-EUV Lab

Physics simulation backend for a chip-scale coherent EUV lithography source. FastAPI server with interactive Plotly visualizations, supporting patent claims for PSF synthesis via spatiotemporal exposure compositing.

## Overview

This repo contains the computational models and visualization engines for a distributed EUV lithography architecture. The backend simulates the full optical pipeline from VCSEL sources through high-harmonic generation to wafer exposure, including resist chemistry, dose optimization, and fleet economics.

Key capabilities:

- **PSF Synthesis** — build arbitrary effective PSFs from rapidly dithered sub-exposures using incoherent and coherent compositing regimes. Coupled (joint) optimization of spatial offsets + temporal intervals demonstrates the Claim 4 patent novelty: synergistic cross-coupling between spatial and temporal degrees of freedom.
- **Multi-Head Writer Array** — tiled lithography architecture with stitching zone calculation, per-site dose calibration, and three architecture variants (A/B/C).
- **3D Optical Pipeline** — VCSEL → HHG gas cell → EUV beam propagation with phase matching, power budget, and gas supply modeling.
- **2D Process Simulation** — aerial image formation (partially coherent), chemical amplification resist model, PEB diffusion (Fick's law), and Mack dissolution rate.
- **Fleet Economics** — cost-of-ownership modeling, throughput analysis, ASML power comparison, and market segment breakdown.
- **Phoenix Engine** — adaptive dose correction with QRL-based hypothesis tracking and gating.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Open `http://127.0.0.1:8000` for the dashboard, or `http://127.0.0.1:8000/docs` for the API docs.

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Dashboard with links to all visualizations |
| `GET /api/psf-synthesis` | PSF synthesis visualizer (Claim 4 evidence) |
| `GET /api/multihead` | Multi-head writer array with architecture selector |
| `GET /api/2d-process` | 2D resist process simulation pipeline |
| `GET /api/3d-pipeline` | 3D optical pipeline from source to wafer |
| `GET /api/fleet-economics` | Fleet cost and throughput analysis |
| `GET /api/phoenix-state` | Adaptive dose correction engine state |

All visualization endpoints accept query parameters for tuning simulation inputs and return self-contained HTML with interactive Plotly charts.

## Backend Modules

```
backend/
  psf_synthesis.py          # Core invention: PSF compositing engine
  visualization_psf.py      # Plotly dashboard for PSF synthesis
  multihead_model.py        # Multi-head tiling and stitching model
  visualization_multihead.py
  optical_pipeline.py       # VCSEL → HHG → EUV beam propagation
  visualization_3d.py
  lithography_model.py      # 2D aerial image + resist process
  visualization.py
  fleet_economics.py        # Cost-of-ownership and throughput
  visualization_fleet.py
  dose_engine.py            # Dose control and correction
  calibration_engine.py     # Per-site calibration
  physics_engine.py         # Shared physics utilities
  hhg_model.py              # High-harmonic generation model
  euv_psf.py                # Native EUV PSF model
  resist_model.py           # Chemically amplified resist
```

## PSF Synthesis (Patent Core)

The PSF synthesis engine (`backend/psf_synthesis.py`) implements:

- **Incoherent compositing**: `PSF_eff = Σ w_i · PSF_native(x-Δx_i, y-Δy_i)` — intensities add, composite always ≥ native FWHM. Value is in reshaping (flat-top, annular profiles).
- **Coherent compositing**: `|Σ a_i · e^(iφ_i) · E_native(...)|²` — destructive interference at wings can sharpen below native FWHM (~18% reduction).
- **Coupled optimization** (Claim 4): joint cost function with fidelity + damage + spatial×temporal cross-coupling terms, optimized via Powell method with bounded perturbations from sequential warm start.
- **NNLS decomposition**: non-negative least squares for physically valid incoherent weight constraints.
- **Thermal relaxation**: `τ = d²/(4α)` modeling for resist thickness dependence.

## Tests

```bash
pytest tests/ -v
```

45 tests covering PSF normalization, FWHM measurement, incoherent broadening constraints, coherent sharpening, thermal relaxation, NNLS decomposition, sequential/coupled optimization, coupled-beats-sequential guarantee, fleet economics, multihead tiling, 3D pipeline physics, and HTML generation.

## Static Export

The visualization pages can be exported as self-contained static HTML for deployment on Cloudflare Pages (or any static host). The export uses FastAPI's TestClient to render each page, then post-processes with BeautifulSoup to rewrite nav links and self-host Plotly.js. Exported pages are deployed at [industriallystrong.com/lab/](https://industriallystrong.com/lab/).

## License

Proprietary. Patent pending.
