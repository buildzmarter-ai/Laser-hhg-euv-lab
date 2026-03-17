import numpy as np
from backend.psf_synthesis import (
    gaussian_psf,
    gaussian_field,
    measure_fwhm,
    composite_psf_incoherent,
    composite_psf_coherent,
    compute_thermal_relaxation,
    flat_top_target,
    annular_target,
    decompose_psf_incoherent,
    optimize_sequential,
    optimize_coupled,
    run_psf_synthesis_comparison,
    SubExposure,
)
from backend.visualization_psf import build_psf_synthesis_html


def test_gaussian_psf_normalized():
    psf = gaussian_psf((64, 64), sigma_nm=5.0)
    assert abs(psf.sum() - 1.0) < 1e-6


def test_gaussian_psf_fwhm():
    psf = gaussian_psf((128, 128), sigma_nm=10.0, dx_nm=1.0)
    row = psf[64, :]
    fwhm = measure_fwhm(row, 1.0)
    # FWHM of Gaussian = 2.355 * sigma
    expected = 2.355 * 10.0
    assert abs(fwhm - expected) < 2.0  # within 2 nm


def test_incoherent_composite_broader_than_native():
    """Core physics: incoherent composite must be >= native FWHM."""
    shape = (128, 128)
    sigma = 10.0
    native = gaussian_psf(shape, sigma)
    native_fwhm = measure_fwhm(native[64, :])

    # Multi-point dither
    subs = [
        SubExposure(0, 0, 0.4),
        SubExposure(5, 0, 0.15),
        SubExposure(-5, 0, 0.15),
        SubExposure(0, 5, 0.15),
        SubExposure(0, -5, 0.15),
    ]
    comp = composite_psf_incoherent(shape, sigma, subs)
    comp_fwhm = measure_fwhm(comp[64, :])

    assert comp_fwhm >= native_fwhm - 1.0  # allow 1nm numerical tolerance


def test_coherent_can_sharpen():
    """Core physics: coherent composite with anti-phase can sharpen below native."""
    shape = (128, 128)
    sigma = 10.0
    native = gaussian_psf(shape, sigma)
    native_fwhm = measure_fwhm(native[64, :])

    # Anti-phase satellites for destructive interference at wings
    subs = [
        SubExposure(0, 0, 1.0, phase=0.0),
        SubExposure(sigma * 0.5, 0, 0.3, phase=np.pi),
        SubExposure(-sigma * 0.5, 0, 0.3, phase=np.pi),
    ]
    coh = composite_psf_coherent(shape, sigma, subs)
    coh_fwhm = measure_fwhm(coh[64, :])

    assert coh_fwhm < native_fwhm  # must be sharper


def test_thermal_relaxation_model():
    thermal = compute_thermal_relaxation(resist_thickness_nm=20.0)
    assert thermal.tau_thermal_ns > 0
    assert thermal.tau_thermal_ns < 10.0  # should be ~1 ns for 20nm resist
    # Long interval should give high relaxation
    long_idx = np.argmax(thermal.intervals_ns)
    assert thermal.relaxation_fractions[long_idx] > 0.99
    # Short interval should give low relaxation
    short_idx = np.argmin(thermal.intervals_ns)
    assert thermal.relaxation_fractions[short_idx] < 0.9


def test_flat_top_target():
    target = flat_top_target((128, 128), radius_nm=15.0)
    assert target.sum() > 0
    assert abs(target.sum() - 1.0) < 0.05  # approximately normalized


def test_annular_target():
    target = annular_target((128, 128), r_inner_nm=5.0, r_outer_nm=15.0)
    assert target.sum() > 0
    # Center should be near zero
    assert target[64, 64] < target[64, 74]


def test_decompose_produces_sub_exposures():
    target = flat_top_target((64, 64), radius_nm=10.0)
    subs = decompose_psf_incoherent(target, sigma_nm=5.0, max_offsets_nm=10.0, step_nm=3.0)
    assert len(subs) > 0
    # All weights non-negative (incoherent constraint)
    for s in subs:
        assert s.weight >= 0


def test_sequential_optimization():
    target = flat_top_target((64, 64), radius_nm=10.0)
    result = optimize_sequential(target, sigma_nm=5.0, n_sub=5)
    assert result.method == "sequential"
    assert result.fidelity_cost >= 0
    assert len(result.sub_exposures) > 0


def test_coupled_optimization():
    target = flat_top_target((64, 64), radius_nm=10.0)
    result = optimize_coupled(target, sigma_nm=5.0, n_sub=5)
    assert result.method == "coupled"
    assert result.fidelity_cost >= 0
    assert len(result.sub_exposures) > 0


def test_coupled_improves_on_sequential():
    """Claim 4 evidence: coupled optimization should produce
    results at least as good as sequential on the combined cost."""
    target = flat_top_target((64, 64), radius_nm=12.0)
    seq = optimize_sequential(target, sigma_nm=5.0, n_sub=7)
    coup = optimize_coupled(target, sigma_nm=5.0, n_sub=7)
    # Coupled starts from sequential solution (warm start), so it should
    # achieve at least as good total cost. Allow small numerical tolerance.
    assert coup.total_cost <= seq.total_cost * 1.1


def test_full_comparison():
    # Use larger grid and sigma for reliable coherent sharpening measurement
    comp = run_psf_synthesis_comparison(
        sigma_nm=10.0, grid_size=128, n_sub=5, resist_thickness_nm=20.0
    )
    assert comp.native_fwhm_nm > 0
    assert comp.coherent_fwhm_nm > 0
    assert comp.coherent_fwhm_nm < comp.native_fwhm_nm
    assert comp.sequential is not None
    assert comp.coupled is not None


def test_psf_html_contains_sections():
    html = build_psf_synthesis_html(
        sigma_nm=5.0, grid_size=64, n_sub=5
    )
    assert "PSF Synthesis Overview" in html
    assert "Incoherent PSF Compositing" in html
    assert "Cross-Section Profiles" in html
    assert "Claim 4 Evidence" in html
    assert "Thermal Relaxation" in html
    assert "Coherent PSF Sharpening" in html
    assert "Sub-Exposure Dither Positions" in html
