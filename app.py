from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse, RedirectResponse
import numpy as np
from backend.euv_psf import generate_elliptical_source, propagate_asm
from backend.resist_model import calculate_3d_resist_profile
from backend.lithography_model import VirtualLithoProcess
from backend.dose_engine import PhoenixEngine
from backend.visualization import build_pipeline_figure, build_tunable_html

app = FastAPI(title="Laser-HHG-EUV Lab")

model = VirtualLithoProcess()
phoenix = PhoenixEngine()


@app.get("/")
async def root():
    return RedirectResponse(url="/api/visualize")


@app.get("/api/fleet-economics")
async def get_economics():
    return {
        "unit_cost_savings": "99.2%",
        "power_draw_reduction": "99.9%",
        "redundancy_impact_per_unit": "1.1%"
    }


@app.post("/api/simulate")
async def simulate(payload: dict = Body(...)):
    ai = np.zeros((256, 256))
    ai[:, 118:138] = 1.0

    dev_rate = model.simulate_chain(ai, {
        "dose": payload.get("dose", 20),
        "peb_time": payload.get("peb_time", 60),
        "diffusion_coef": payload.get("diffusion_coef", 5.0),
        "k_amp": payload.get("k_amp", 0.2),
        "r_max": payload.get("r_max", 100),
        "r_min": payload.get("r_min", 0.1),
        "n_mack": payload.get("n_mack", 5)
    })

    return {
        "status": "success",
        "visual_data": dev_rate.tolist(),
        "metrics": {
            "max_rate": float(np.max(dev_rate)),
            "mean_rate": float(np.mean(dev_rate))
        }
    }


@app.get("/api/visualize", response_class=HTMLResponse)
async def visualize(
    dose: float = 20.0,
    line_width: int = 20,
    peb_time: float = 60.0,
    diffusion_coef: float = 5.0,
    k_amp: float = 0.2,
    r_max: float = 100.0,
    r_min: float = 0.1,
    n_mack: int = 5,
):
    ai = np.zeros((256, 256))
    center = 256 // 2
    half = max(1, line_width // 2)
    ai[:, center - half:center + half] = 1.0

    params = {
        "dose": dose, "line_width": line_width, "peb_time": peb_time,
        "diffusion_coef": diffusion_coef, "k_amp": k_amp,
        "r_max": r_max, "r_min": r_min, "n_mack": n_mack,
    }

    stages = model.simulate_chain_detailed(ai, params)
    title = f"EUV Litho Pipeline (dose={dose} mJ/cm\u00b2, line={line_width} nm)"
    return build_tunable_html(stages, params, title=title)


@app.get("/api/v1/system-state")
async def get_system_state():
    return {
        "active_hypotheses": phoenix.hypotheses,
        "correction_factor": phoenix.get_correction_factor(),
        "dose_tolerance": f"{phoenix.dose_tolerance * 100}%",
        "status": "Adaptive Gating Active"
    }
