import numpy as np
from backend.lithography_model import VirtualLithoProcess

def test_process_sensitivity():
    model = VirtualLithoProcess(nx=128, ny=128)
    # Ensure this is NOT all zeros. We need a target to expose!
    test_pattern = np.zeros((128, 128))
    test_pattern[40:80, 40:80] = 1.0  # Create a central square
    
    params = {'dose': 5, 'peb_time': 60, 'diffusion_coef': 5.0, 'k_amp': 0.2, 'r_max': 100, 'r_min': 0.1, 'n_mack': 5}
    low_res = model.simulate_chain(test_pattern, params)
    
    params['dose'] = 100 # High dose
    high_res = model.simulate_chain(test_pattern, params)
    
    print(f"Low: {np.mean(low_res)}, High: {np.mean(high_res)}")
    assert np.mean(high_res) > np.mean(low_res)