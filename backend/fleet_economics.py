"""Platform economics model: integrated multi-head writer vs ASML comparison.

Physical hierarchy:
  Writer Head (~2×2mm die) → Package (33×33mm) → Module (~200×200mm board) → Platform (desk-sized tool)

Each writer head is a 3D optical structure built from 2D planar semiconductor
processes, coupled optically for the target wavelength.  Components include beam
propagation optics, optical switches, waveguides, and polarizers — an 11-degree-
of-freedom system.  Heads are batch-fabricated (1,000+ per wafer run) and
robotically assembled in cleanrooms onto packages, giving semiconductor-class
cost scaling.

Three architecture variants (A: NIR/Vis, B: DUV, C: EUV) produce different
PSFs on resist but share the same physical platform and assembly process.
"""

from dataclasses import dataclass
import math

# --- ASML reference data ---
ASML_POWER_CHAIN = [
    {"stage": "Grid Power", "power_w": 1_500_000, "note": "Facility input"},
    {"stage": "CO\u2082 Drive Laser", "power_w": 40_000, "note": "Trumpf 40kW optical from 400kW electrical (10% eff)"},
    {"stage": "Tin Plasma EUV", "power_w": 2_000, "note": "5% conversion of 40kW laser \u2192 2kW into 2\u03c0 sr"},
    {"stage": "Collector Mirror", "power_w": 800, "note": "~40% of 2kW (limited solid angle ~5 sr)"},
    {"stage": "Spectral Filter (2%)", "power_w": 500, "note": "Mo/Si bandwidth filtering"},
    {"stage": "Intermediate Focus", "power_w": 250, "note": "ASML spec at IF"},
    {"stage": "Scanner Optics (11 mirrors)", "power_w": 3.0, "note": "0.67^11 \u2248 1.2% of 250W"},
    {"stage": "At Wafer", "power_w": 1.0, "note": "~1W usable at wafer plane"},
]

COHERENT_POWER_CHAIN = [
    {"stage": "Wall Plug", "power_w": 500, "note": "Total electrical input"},
    {"stage": "Drive Lasers (optical)", "power_w": 50, "note": "VCSEL + trap + HHG drive (~10% wall-plug eff)"},
    {"stage": "Coherent EUV Source", "power_w": 0.010, "note": "10 mW directed, coherent 13.5 nm"},
    {"stage": "Scanner Optics (6 mirrors)", "power_w": 0.0009, "note": "0.67^6 \u2248 9% (fewer mirrors needed)"},
    {"stage": "At Wafer", "power_w": 0.0009, "note": "~0.9 mW coherent at wafer"},
]

ASML_REFERENCE = {
    "unit_cost_m": 380,       # $M per machine
    "power_draw_kw": 1500,    # kW
    "wph": 220,               # wafers per hour (NXE:3800E target)
    "floor_area_m2": 120,     # approximate
    "annual_service_m": 25,   # $M/year service contract
    "install_months": 6,      # months to install
    "engineers_install": 250, # engineers needed
}


# --- Platform hierarchy ---

@dataclass
class PlatformConfig:
    """Physical configuration of an integrated multi-head writer platform.

    Each writer head is a 3D optical stack built from 2D planar semiconductor
    layers, with 11 degrees of freedom:
      1-2: X/Y beam position (MEMS tip/tilt)
      3:   Z focus (MEMS piston)
      4:   Intensity modulation (emitter drive current)
      5:   Polarization (integrated waveguide polarizer)
      6-7: Waveguide routing / optical switch state
      8:   Wavelength tuning (cavity bias)
      9:   Pulse timing (modulation phase)
      10:  Dose integration time (dwell control)
      11:  Thermal compensation (on-die sensor feedback)

    Heads are batch-fabricated ~1,000 per wafer run on standard 200/300mm
    semiconductor lines, then robotically assembled in cleanroom onto packages.
    """
    name: str
    heads_per_package: int       # e.g., 16 (4×4 grid on 33×33mm)
    packages_per_module: int     # e.g., 10 packages on one carrier board
    modules: int                 # e.g., 1-10 modules in one platform
    # Costs (semiconductor batch manufacturing)
    head_cost_usd: float = 150          # die cost: 2D planar fab + optical assembly
    package_cost_usd: float = 2_000     # interposer + flip-chip + optical coupling
    module_cost_usd: float = 25_000     # PCB carrier + cooling + robotic assembly
    frame_cost_usd: float = 500_000     # enclosure, stage, optics, controller
    # Batch manufacturing
    heads_per_fab_run: int = 1_000      # batch size from one wafer run
    # Power
    head_power_w: float = 0.5           # per-head electrical (11 DOF actuation)
    module_overhead_w: float = 50       # control + cooling per module
    platform_overhead_w: float = 200    # stage, vacuum, alignment
    # Physical
    footprint_m2: float = 2.0           # desk-sized platform

    @property
    def total_heads(self):
        return self.heads_per_package * self.packages_per_module * self.modules

    @property
    def total_packages(self):
        return self.packages_per_module * self.modules

    @property
    def total_cost_usd(self):
        heads_cost = self.total_heads * self.head_cost_usd
        pkg_cost = self.total_packages * self.package_cost_usd
        mod_cost = self.modules * self.module_cost_usd
        return heads_cost + pkg_cost + mod_cost + self.frame_cost_usd

    @property
    def total_cost_m(self):
        return self.total_cost_usd / 1e6

    @property
    def total_power_w(self):
        heads = self.total_heads * self.head_power_w
        mods = self.modules * self.module_overhead_w
        return heads + mods + self.platform_overhead_w

    @property
    def total_power_kw(self):
        return self.total_power_w / 1000


# Predefined platform configurations
PLATFORM_CONFIGS = {
    "R&D / Prototyping": PlatformConfig(
        name="R&D / Prototyping",
        heads_per_package=16,
        packages_per_module=2,
        modules=1,
        frame_cost_usd=300_000,
        footprint_m2=0.5,
    ),
    "Specialty / Defense": PlatformConfig(
        name="Specialty / Defense",
        heads_per_package=16,
        packages_per_module=10,
        modules=1,
        frame_cost_usd=500_000,
        footprint_m2=1.0,
    ),
    "Mid-Volume": PlatformConfig(
        name="Mid-Volume",
        heads_per_package=16,
        packages_per_module=10,
        modules=4,
        frame_cost_usd=800_000,
        footprint_m2=2.0,
    ),
    "HVM Parity": PlatformConfig(
        name="HVM Parity",
        heads_per_package=16,
        packages_per_module=10,
        modules=10,
        frame_cost_usd=1_200_000,
        footprint_m2=3.0,
    ),
}

# Legacy-compatible market segments (derived from configs)
MARKET_SEGMENTS = {}
for _seg_name, _cfg in PLATFORM_CONFIGS.items():
    MARKET_SEGMENTS[_seg_name] = {
        "heads": _cfg.total_heads,
        "packages": _cfg.total_packages,
        "modules": _cfg.modules,
        "description": {
            "R&D / Prototyping": "University labs, national labs, resist characterization",
            "Specialty / Defense": "Trusted foundry, photonics, MEMS fabs",
            "Mid-Volume": "Regional foundries, tower/UMC class",
            "HVM Parity": "Match ASML 220 wph throughput on a single platform",
        }[_seg_name],
        "capex_range": f"${_cfg.total_cost_m:.1f}M",
        "power_range": f"{_cfg.total_power_kw:.1f} kW",
        "config": _cfg,
    }


@dataclass
class PlatformScenario:
    """Result of platform economics calculation at a given EUV power level."""
    euv_power_mw: float
    dose_mj_cm2: float
    field_area_cm2: float
    fields_per_wafer: int
    seconds_per_field: float
    seconds_per_wafer: float
    # Platform hierarchy
    config_name: str
    total_heads: int
    total_packages: int
    modules: int
    # Throughput
    wph: float
    wph_per_head: float
    # Cost
    platform_cost_m: float
    # Power
    platform_power_kw: float
    # Footprint
    footprint_m2: float
    # vs ASML
    capex_savings_pct: float
    power_savings_pct: float
    footprint_savings_pct: float
    # Redundancy
    single_head_failure_pct: float


def compute_platform_scenario(
    euv_power_mw: float,
    config: PlatformConfig = None,
    dose_mj_cm2: float = 15.0,
    field_mm_x: float = 26.0,
    field_mm_y: float = 33.0,
    fields_per_wafer: int = 90,
    overhead_pct: float = 30.0,
) -> PlatformScenario:
    """Compute platform economics for a given EUV source power level.

    All writer heads on the platform operate in parallel, so total throughput
    scales linearly with head count.
    """
    if config is None:
        config = PLATFORM_CONFIGS["Specialty / Defense"]

    field_area_cm2 = (field_mm_x / 10) * (field_mm_y / 10)
    energy_per_field_mj = dose_mj_cm2 * field_area_cm2
    power_mw = euv_power_mw

    # Single-head exposure time for one field
    seconds_per_field_one_head = energy_per_field_mj / power_mw if power_mw > 0 else float("inf")

    # Total fields across the wafer; heads work in parallel on different fields
    total_heads = config.total_heads
    # Time to expose full wafer = (fields / heads) * time_per_field + overhead
    fields_per_head = math.ceil(fields_per_wafer / total_heads) if total_heads > 0 else fields_per_wafer
    exposure_seconds = fields_per_head * seconds_per_field_one_head
    total_seconds = exposure_seconds * (1 + overhead_pct / 100)
    wph = 3600 / total_seconds if total_seconds > 0 else 0
    wph_per_head = 3600 / (fields_per_wafer * seconds_per_field_one_head * (1 + overhead_pct / 100)) if seconds_per_field_one_head < float("inf") else 0

    platform_cost_m = config.total_cost_m
    platform_power_kw = config.total_power_kw
    footprint_m2 = config.footprint_m2

    asml_capex = ASML_REFERENCE["unit_cost_m"]
    asml_power = ASML_REFERENCE["power_draw_kw"]
    asml_area = ASML_REFERENCE["floor_area_m2"]

    capex_savings = (1 - platform_cost_m / asml_capex) * 100 if asml_capex > 0 else 0
    power_savings = (1 - platform_power_kw / asml_power) * 100 if asml_power > 0 else 0
    footprint_savings = (1 - footprint_m2 / asml_area) * 100 if asml_area > 0 else 0
    single_head_failure = (1 / total_heads) * 100 if total_heads > 0 else 100

    return PlatformScenario(
        euv_power_mw=euv_power_mw,
        dose_mj_cm2=dose_mj_cm2,
        field_area_cm2=field_area_cm2,
        fields_per_wafer=fields_per_wafer,
        seconds_per_field=seconds_per_field_one_head,
        seconds_per_wafer=total_seconds,
        config_name=config.name,
        total_heads=total_heads,
        total_packages=config.total_packages,
        modules=config.modules,
        wph=wph,
        wph_per_head=wph_per_head,
        platform_cost_m=platform_cost_m,
        platform_power_kw=platform_power_kw,
        footprint_m2=footprint_m2,
        capex_savings_pct=capex_savings,
        power_savings_pct=power_savings,
        footprint_savings_pct=footprint_savings,
        single_head_failure_pct=single_head_failure,
    )


def compute_sensitivity_table(
    power_levels_mw=None,
    config: PlatformConfig = None,
    **kwargs,
) -> list[PlatformScenario]:
    """Compute platform scenarios across multiple EUV power levels."""
    if power_levels_mw is None:
        power_levels_mw = [0.1, 1.0, 5.0, 10.0, 50.0]
    return [compute_platform_scenario(p, config=config, **kwargs) for p in power_levels_mw]


def compute_scaling_table(
    euv_power_mw: float = 10.0,
    configs: list[PlatformConfig] = None,
    **kwargs,
) -> list[PlatformScenario]:
    """Compute scenarios across platform configurations at fixed power."""
    if configs is None:
        configs = list(PLATFORM_CONFIGS.values())
    return [compute_platform_scenario(euv_power_mw, config=c, **kwargs) for c in configs]
