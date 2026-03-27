import numpy as np
from numpy.typing import NDArray
from data.constants import ISOTOPE_DATA, ATTENUATION_COEFFICIENTS


def simulate_pet_annihilations(
    n_events: int,
    tumor_radius: float,
    tumor_center_x: float = 0.0,
    tumor_center_y: float = 0.0
) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """
    Simulate PET annihilation events using Monte Carlo.
    
    Each event generates:
    - A random origin point (x, y) within the tumor (circular region)
    - Two photons emitted at 180° (511 keV each)
    
    Args:
        n_events: Number of annihilation events
        tumor_radius: Radius of the tumor in cm
        tumor_center_x: X coordinate of tumor center
        tumor_center_y: Y coordinate of tumor center
    
    Returns:
        Tuple of (origins, directions1, directions2)
        - origins: (n_events, 2) array of (x, y) coordinates
        - directions1: (n_events, 2) array of unit vectors for first photon
        - directions2: (n_events, 2) array of unit vectors for second photon (opposite)
    """
    r = np.sqrt(np.random.uniform(0, 1, n_events)) * tumor_radius
    theta = np.random.uniform(0, 2 * np.pi, n_events)
    
    origins = np.column_stack([
        tumor_center_x + r * np.cos(theta),
        tumor_center_y + r * np.sin(theta)
    ])
    
    emission_angles = np.random.uniform(0, 2 * np.pi, n_events)
    
    directions1 = np.column_stack([
        np.cos(emission_angles),
        np.sin(emission_angles)
    ])
    
    directions2 = -directions1
    
    return origins, directions1, directions2


def _interpolate_attenuation_coefficient(material: str, energy_kev: float) -> float:
    """
    Interpolate linear attenuation coefficient for given material and energy.
    
    Args:
        material: Material name (Plomo, Agua, Hormigón)
        energy_kev: Photon energy in keV
    
    Returns:
        Linear attenuation coefficient μ in cm⁻¹
    """
    coeffs = ATTENUATION_COEFFICIENTS[material]
    energies = np.array(sorted(coeffs.keys()))
    mu_values = np.array([coeffs[e] for e in energies])
    
    if energy_kev <= energies[0]:
        return mu_values[0]
    if energy_kev >= energies[-1]:
        return mu_values[-1]
    
    return np.interp(energy_kev, energies, mu_values)


def simulate_shielding(
    material: str,
    thickness: float,
    energy_kev: float,
    n_photons: int,
    use_random_walk: bool = True
) -> tuple[int, int, int, float]:
    """
    Simulate photon interaction with shielding material.
    
    Args:
        material: Material type (Plomo, Agua, Hormigón)
        thickness: Material thickness in cm
        energy_kev: Initial photon energy in keV
        n_photons: Number of photons to simulate
        use_random_walk: Use stochastic random walk vs Beer-Lambert
    
    Returns:
        Tuple of (transmitted, absorbed, scattered, mu)
        - transmitted: Number of photons that passed through
        - absorbed: Number of photons absorbed
        - scattered: Number of photons scattered
        - mu: Linear attenuation coefficient used
    """
    mu = _interpolate_attenuation_coefficient(material, energy_kev)
    
    if not use_random_walk:
        transmission_prob = np.exp(-mu * thickness)
        transmitted = int(n_photons * transmission_prob)
        absorbed = n_photons - transmitted
        scattered = 0
        return transmitted, absorbed, scattered, mu
    
    transmitted = 0
    absorbed = 0
    scattered = 0
    
    step_size = 0.1
    
    for _ in range(n_photons):
        position = 0.0
        photon_energy = energy_kev
        
        while position < thickness:
            interaction_prob = 1 - np.exp(-mu * step_size)
            
            if np.random.random() < interaction_prob:
                compton_prob = 0.6
                photoelectric_prob = 0.4
                
                if np.random.random() < photoelectric_prob:
                    absorbed += 1
                    break
                else:
                    photon_energy *= 0.8
                    
                    if photon_energy < 50:
                        absorbed += 1
                        break
                    
                    mu = _interpolate_attenuation_coefficient(material, photon_energy)
                    
                    deflection_angle = np.random.uniform(-np.pi/4, np.pi/4)
                    if abs(deflection_angle) > np.pi/6:
                        scattered += 1
                        break
            
            position += step_size
        
        if position >= thickness:
            transmitted += 1
    
    return transmitted, absorbed, scattered, mu


def simulate_radioactive_decay(
    isotope: str,
    initial_activity_mbq: float,
    time_hours: float,
    n_simulations: int = 10_000
) -> tuple[float, float, int, int, float, float]:
    """
    Simulate radioactive decay using Monte Carlo.
    
    Args:
        isotope: Isotope name (e.g., "Tc-99m")
        initial_activity_mbq: Initial activity in MBq
        time_hours: Time elapsed in hours
        n_simulations: Number of atoms to simulate
    
    Returns:
        Tuple of (final_activity, simulated_activity, n_initial, n_remaining, decay_constant, half_life)
    """
    isotope_info = ISOTOPE_DATA[isotope]
    half_life = isotope_info["half_life_hours"]
    
    decay_constant = np.log(2) / half_life
    
    final_activity = initial_activity_mbq * np.exp(-decay_constant * time_hours)
    
    decay_probabilities = 1 - np.exp(-decay_constant * time_hours)
    random_values = np.random.uniform(0, 1, n_simulations)
    
    n_remaining = np.sum(random_values > decay_probabilities)
    n_initial = n_simulations
    
    simulated_activity = initial_activity_mbq * (n_remaining / n_initial)
    
    return final_activity, simulated_activity, n_initial, n_remaining, decay_constant, half_life
