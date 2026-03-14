from fastapi import FastAPI, Body
import numpy as np
from backend.euv_psf import generate_elliptical_source, propagate_asm
from backend.resist_model import calculate_3d_resist_profile
from backend.lithography_model import VirtualLithoProcess
import numpy as np
from backend.dose_engine import PhoenixEngine

app = FastAPI(title="Laser-HHG-EUV Lab")

model = VirtualLithoProcess()

@app.get("/api/fleet-economics")
async def get_economics():
    # [span_6](start_span)[span_7](start_span)Returns the 99% power reduction and 1.1% fail-impact data[span_6](end_span)[span_7](end_span)
    return {
        "unit_cost_savings": "99.2%",
        "power_draw_reduction": "99.9%",
        "redundancy_impact_per_unit": "1.1%"
    }

from fastapi import FastAPI, Body
from backend.lithography_model import VirtualLithoProcess
import numpy as np

app = FastAPI()
# Instantiate the physics engine
model = VirtualLithoProcess()

from fastapi import FastAPI, Body
from backend.lithography_model import VirtualLithoProcess
import numpy as np

app = FastAPI()
model = VirtualLithoProcess()

@app.post("/api/simulate")
async def simulate(payload: dict = Body(...)):
    # 1. Generate 20nm Target Pattern (Aerial Image)
    # This creates a center-aligned 20nm vertical line
    ai = np.zeros((256, 256))
    ai[:, 118:138] = 1.0 
    
    # 2. Execute the E2E Virtual Process
    # Chaining Stochastic Exposure -> PEB -> Mack Dissolution
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



# Instantiate the engine
phoenix = PhoenixEngine()

@app.get("/api/v1/system-state")
async def get_system_state():
    """
    Exposes the Phoenix Engine's current hypotheses and correction factors.
    """
    return {
        "active_hypotheses": phoenix.hypotheses,
        "correction_factor": phoenix.get_correction_factor(),
        "dose_tolerance": f"{phoenix.dose_tolerance * 100}%",
        "status": "Adaptive Gating Active"
    }