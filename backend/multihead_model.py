"""Multi-head writer array model for tiled maskless lithography.

Models the patent's core architecture: a 2D array of writer heads,
each exposing a local tile on the wafer, with stitching overlap zones
and per-site calibration.
"""

from dataclasses import dataclass, field
import numpy as np


# --- Architecture definitions ---
ARCHITECTURES = {
    "A": {
        "name": "Architecture A — NIR/Visible",
        "short": "A: NIR/Vis",
        "wavelength_nm": 405,
        "wavelength_label": "405 nm (GaN VCSEL)",
        "emitter_type": "GaN VCSEL array",
        "optics_material": "BK7 / fused silica",
        "tile_um": 200,
        "na": 0.3,
        "resolution_nm": 500,
        "emitter_pitch_um": 10,
        "power_per_emitter_mw": 2.0,
        "color": "#e63946",
        "description": "Proof-of-concept platform. NIR/visible VCSELs with standard MEMS "
                       "steering. Validates tiling, stitching, and calibration subsystems.",
        "trl": 5,
    },
    "B": {
        "name": "Architecture B — Deep UV",
        "short": "B: DUV",
        "wavelength_nm": 248,
        "wavelength_label": "248 nm (AlGaN DUV)",
        "emitter_type": "AlGaN DUV VCSEL array",
        "optics_material": "Fused silica / CaF\u2082 / MgF\u2082",
        "tile_um": 100,
        "na": 0.6,
        "resolution_nm": 80,
        "emitter_pitch_um": 5,
        "power_per_emitter_mw": 0.5,
        "color": "#457b9d",
        "description": "Production-class DUV writer. AlGaN deep-UV emitters at 193\u2013300 nm "
                       "with UV-compatible MEMS optics and high-NA micro-objectives.",
        "trl": 3,
    },
    "C": {
        "name": "Architecture C — EUV (Rydberg HHG)",
        "short": "C: EUV",
        "wavelength_nm": 13.5,
        "wavelength_label": "13.5 nm (Rydberg HHG)",
        "emitter_type": "Mo/Si MEMS mirror modulator",
        "optics_material": "Mo/Si multilayer reflectors",
        "tile_um": 100,
        "na": 0.33,
        "resolution_nm": 7,
        "emitter_pitch_um": 2,
        "power_per_emitter_mw": 0.001,
        "color": "#6a0dad",
        "description": "EUV prototype. Rydberg-enhanced HHG source feeds MEMS mirror "
                       "modulator heads with Mo/Si multilayer coatings at 13.5 nm.",
        "trl": 2,
    },
}


@dataclass
class WriterHead:
    """A single writer head in the multi-head array."""
    head_id: int
    row: int
    col: int
    tile_x_um: float        # tile center x on wafer
    tile_y_um: float        # tile center y on wafer
    tile_size_um: float     # side length of square tile
    n_emitters: int         # emitters per head (n x n)
    emitter_pitch_um: float
    power_mw: float         # total optical power from this head
    # Per-site calibration: correction factors for each emitter
    calibration_map: np.ndarray = field(default=None, repr=False)


@dataclass
class MultiHeadArray:
    """A 2D array of writer heads tiling a wafer region."""
    arch_key: str
    n_rows: int
    n_cols: int
    tile_size_um: float
    overlap_um: float       # overlap between adjacent tiles
    heads: list = field(default_factory=list)
    wafer_region_x_um: float = 0.0
    wafer_region_y_um: float = 0.0


def build_multihead_array(
    arch_key: str = "A",
    n_rows: int = 4,
    n_cols: int = 4,
    overlap_pct: float = 5.0,
    emitters_per_side: int = 16,
) -> MultiHeadArray:
    """Build a multi-head writer array for the given architecture."""
    arch = ARCHITECTURES[arch_key]
    tile_size = arch["tile_um"]
    overlap_um = tile_size * overlap_pct / 100.0
    pitch = tile_size - overlap_um  # center-to-center spacing

    heads = []
    for r in range(n_rows):
        for c in range(n_cols):
            head_id = r * n_cols + c
            cx = c * pitch + tile_size / 2
            cy = r * pitch + tile_size / 2
            n_emitters = emitters_per_side ** 2
            power = n_emitters * arch["power_per_emitter_mw"]

            # Simulate fabrication-induced intensity variation (±15%)
            rng = np.random.RandomState(42 + head_id)
            cal_map = 1.0 + 0.15 * (rng.rand(emitters_per_side, emitters_per_side) - 0.5)

            heads.append(WriterHead(
                head_id=head_id,
                row=r, col=c,
                tile_x_um=cx, tile_y_um=cy,
                tile_size_um=tile_size,
                n_emitters=n_emitters,
                emitter_pitch_um=arch["emitter_pitch_um"],
                power_mw=power,
                calibration_map=cal_map,
            ))

    region_x = n_cols * pitch + overlap_um
    region_y = n_rows * pitch + overlap_um

    return MultiHeadArray(
        arch_key=arch_key,
        n_rows=n_rows, n_cols=n_cols,
        tile_size_um=tile_size,
        overlap_um=overlap_um,
        heads=heads,
        wafer_region_x_um=region_x,
        wafer_region_y_um=region_y,
    )


def compute_tile_exposure(
    arch_key: str,
    source_power_mw: float,
    dose_mj_cm2: float = 15.0,
    n_heads: int = 16,
) -> dict:
    """Compute exposure time per tile and total wafer time."""
    arch = ARCHITECTURES[arch_key]
    tile_um = arch["tile_um"]
    tile_area_cm2 = (tile_um * 1e-4) ** 2
    energy_per_tile_mj = dose_mj_cm2 * tile_area_cm2
    power_per_head_mw = source_power_mw / n_heads if n_heads > 0 else source_power_mw

    time_per_tile_s = energy_per_tile_mj / power_per_head_mw if power_per_head_mw > 0 else float("inf")

    # 300mm wafer: ~707 mm² active area
    wafer_area_um2 = 707e6  # µm²
    tile_area_um2 = tile_um ** 2
    tiles_per_wafer = int(wafer_area_um2 / tile_area_um2)

    # With n_heads in parallel, each head covers tiles_per_wafer / n_heads tiles
    tiles_per_head = tiles_per_wafer / n_heads if n_heads > 0 else tiles_per_wafer
    total_exposure_s = tiles_per_head * time_per_tile_s
    # Add 20% overhead for stepping/settling
    total_time_s = total_exposure_s * 1.2

    return {
        "arch_key": arch_key,
        "arch_name": arch["name"],
        "tile_um": tile_um,
        "tile_area_cm2": tile_area_cm2,
        "energy_per_tile_mj": energy_per_tile_mj,
        "power_per_head_mw": power_per_head_mw,
        "time_per_tile_ms": time_per_tile_s * 1000,
        "tiles_per_wafer": tiles_per_wafer,
        "tiles_per_head": tiles_per_head,
        "n_heads": n_heads,
        "total_exposure_s": total_exposure_s,
        "total_time_s": total_time_s,
        "wph": 3600 / total_time_s if total_time_s > 0 else 0,
        "dose_mj_cm2": dose_mj_cm2,
        "source_power_mw": source_power_mw,
    }


def simulate_dose_calibration(
    emitters_per_side: int = 16,
    target_dose: float = 1.0,
    seed: int = 42,
) -> dict:
    """Simulate per-site calibration: raw variation, correction, and corrected output."""
    rng = np.random.RandomState(seed)

    # Raw emitter intensity (fabrication variation ±15%)
    raw_intensity = target_dose * (1.0 + 0.15 * (2 * rng.rand(emitters_per_side, emitters_per_side) - 1))

    # Static calibration correction (factory-measured)
    static_correction = target_dose / raw_intensity

    # Apply static correction
    after_static = raw_intensity * static_correction  # should be ~target_dose

    # Simulate thermal drift (±3% temporal variation)
    thermal_drift = 1.0 + 0.03 * (2 * rng.rand(emitters_per_side, emitters_per_side) - 1)
    after_drift = after_static * thermal_drift

    # Dynamic in-situ correction (sensor feedback)
    dynamic_correction = target_dose / after_drift
    final_dose = after_drift * dynamic_correction

    return {
        "raw_intensity": raw_intensity,
        "static_correction": static_correction,
        "after_static": after_static,
        "thermal_drift": thermal_drift,
        "after_drift": after_drift,
        "dynamic_correction": dynamic_correction,
        "final_dose": final_dose,
        "target_dose": target_dose,
        "raw_uniformity_pct": float(np.std(raw_intensity) / np.mean(raw_intensity) * 100),
        "corrected_uniformity_pct": float(np.std(final_dose) / np.mean(final_dose) * 100),
    }
