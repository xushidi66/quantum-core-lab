import numpy as np


def pass_intensity(
    initial_intensity: float,
    angles_deg: list[float],
    unpolarized_input: bool = True
) -> float:
    """
    Simulate light intensity after passing through a sequence of ideal polaroids.

    Args:
        initial_intensity: input light intensity.
        angles_deg: polaroid angles in degrees, e.g. [0, 45, 90].
        unpolarized_input: if True, the first polaroid reduces natural light by 1/2.

    Returns:
        Output light intensity.
    """
    if initial_intensity < 0:
        raise ValueError("initial_intensity must be non-negative")

    if len(angles_deg) == 0:
        return float(initial_intensity)

    intensity = initial_intensity

    if unpolarized_input:
        intensity = intensity * 0.5

    for prev, curr in zip(angles_deg[:-1], angles_deg[1:]):
        theta_deg = curr - prev
        theta_rad = np.deg2rad(theta_deg)
        factor = np.cos(theta_rad) ** 2
        intensity = intensity * factor

    return float(intensity)