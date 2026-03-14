import numpy as np

def generate_acid_map(aerial_image, dose_mj_cm2, quantum_efficiency=0.5):
    """
    Simulates stochastic acid generation from EUV photons.
    """
    # Convert dose to mean photon count per pixel
    # EUV Photon energy @ 13.5nm approx 92 eV
    h_c_lambda = 1.47e-17 # Joules per EUV photon
    mean_photons = (aerial_image * dose_mj_cm2 * 1e-3) / h_c_lambda
    
    # Poisson noise for shot noise
    actual_photons = np.random.poisson(mean_photons)
    
    # Acid generation (Probability of PAG conversion)
    acid_map = actual_photons * quantum_efficiency
    return acid_map

def simulate_peb(acid_map, initial_m=1.0, k_amp=0.05, d_acid=2.0, dt=0.1, steps=100):
    """
    Solves Reaction-Diffusion: dM/dt = -k*H*M and dH/dt = D*grad^2(H)
    """
    M = np.full_like(acid_map, initial_m)
    H = acid_map.copy()
    
    for _ in range(steps):
        # 1. Diffusion (Acid moves)
        laplacian = (np.roll(H, 1, axis=0) + np.roll(H, -1, axis=0) + 
                     np.roll(H, 1, axis=1) + np.roll(H, -1, axis=1) - 4*H)
        H += d_acid * laplacian * dt
        
        # 2. Reaction (Deprotection happens)
        M -= k_amp * H * M * dt
        M = np.clip(M, 0, 1) # Concentrations can't be negative
        
    return M # Returns the deprotection profile
