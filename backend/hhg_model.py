import numpy as np

def calculate_cutoff_energy(intensity_w_cm2, ionization_potential_ev):
    # [span_3](start_span)Up (Ponderomotive energy) = 9.33e-14 * I * lambda^2[span_3](end_span)
    wavelength_um = 0.8 
    up = 9.33e-14 * intensity_w_cm2 * (wavelength_um**2)
    return ionization_potential_ev + 3.17 * up

def get_harmonic_wavelength(q, fundamental_nm=800):
    return fundamental_nm / q
