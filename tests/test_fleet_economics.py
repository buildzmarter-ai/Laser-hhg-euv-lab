from backend.fleet_economics import (
    compute_platform_scenario,
    compute_sensitivity_table,
    compute_scaling_table,
    ASML_POWER_CHAIN,
    COHERENT_POWER_CHAIN,
    PLATFORM_CONFIGS,
)
from backend.visualization_fleet import (
    build_sensitivity_figure,
    build_waterfall_figure,
    build_fleet_dashboard_html,
)


def test_platform_scenario_basic():
    s = compute_platform_scenario(10.0)
    assert s.euv_power_mw == 10.0
    assert s.wph > 0
    assert s.total_heads > 0
    assert s.platform_cost_m > 0
    assert s.platform_power_kw > 0


def test_higher_power_more_throughput():
    s1 = compute_platform_scenario(1.0)
    s10 = compute_platform_scenario(10.0)
    assert s10.wph > s1.wph


def test_sensitivity_table_length():
    scenarios = compute_sensitivity_table()
    assert len(scenarios) == 5


def test_sensitivity_table_custom_powers():
    scenarios = compute_sensitivity_table(power_levels_mw=[1.0, 50.0])
    assert len(scenarios) == 2
    assert scenarios[0].euv_power_mw == 1.0
    assert scenarios[1].euv_power_mw == 50.0


def test_power_chain_decreasing():
    asml_powers = [s["power_w"] for s in ASML_POWER_CHAIN]
    for i in range(1, len(asml_powers)):
        assert asml_powers[i] <= asml_powers[i - 1]

    coh_powers = [s["power_w"] for s in COHERENT_POWER_CHAIN]
    for i in range(1, len(coh_powers)):
        assert coh_powers[i] <= coh_powers[i - 1]


def test_sensitivity_figure_has_traces():
    scenarios = compute_sensitivity_table()
    fig = build_sensitivity_figure(scenarios)
    assert len(fig.data) >= 4


def test_waterfall_figure_has_traces():
    fig = build_waterfall_figure()
    assert len(fig.data) == 2


def test_platform_dashboard_html():
    scenarios = compute_sensitivity_table()
    params = {"dose_mj_cm2": 15.0, "config_name": "Specialty / Defense"}
    html = build_fleet_dashboard_html(scenarios, params)
    assert "Platform Economics" in html
    assert "ASML" in html
    assert "Sensitivity" in html
    assert "Power Loss Chain" in html
    assert "Platform Hierarchy" in html
    assert "11" in html  # 11 DOF reference


def test_capex_savings_positive_at_10mw():
    s = compute_platform_scenario(10.0)
    assert s.capex_savings_pct > 0


def test_power_savings_positive():
    for power in [0.1, 1.0, 10.0, 50.0]:
        s = compute_platform_scenario(power)
        assert s.power_savings_pct > 0, f"Expected power savings at {power} mW"


def test_single_head_failure_decreases_with_more_heads():
    """More heads = lower single-head failure impact."""
    configs = list(PLATFORM_CONFIGS.values())
    failures = [compute_platform_scenario(10.0, config=c).single_head_failure_pct for c in configs]
    for i in range(1, len(failures)):
        assert failures[i] <= failures[i - 1]


def test_scaling_table():
    scenarios = compute_scaling_table(euv_power_mw=10.0)
    assert len(scenarios) == len(PLATFORM_CONFIGS)
    # Larger configs should have more throughput
    wphs = [s.wph for s in scenarios]
    for i in range(1, len(wphs)):
        assert wphs[i] >= wphs[i - 1]


def test_platform_hierarchy_counts():
    cfg = PLATFORM_CONFIGS["Specialty / Defense"]
    assert cfg.total_heads == 160  # 16 heads/pkg * 10 pkg/mod * 1 mod
    assert cfg.total_packages == 10
    assert cfg.modules == 1

    cfg_hvm = PLATFORM_CONFIGS["HVM Parity"]
    assert cfg_hvm.total_heads == 1600  # 16 * 10 * 10
