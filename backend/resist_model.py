import numpy as np


def calculate_3d_resist_profile(exposure, thickness, sensitivity=1.0):
    """Placeholder resist development model.

    Args:
        exposure (np.ndarray): 2D exposure dose map.
        thickness (float): initial resist thickness in nm.
        sensitivity (float): development sensitivity constant.

    Returns:
        np.ndarray: 2D resist profile after development (same shape as
        exposure).
    """
    # simple linear decay model for demonstration
    profile = thickness - sensitivity * exposure
    return np.clip(profile, 0, thickness)
