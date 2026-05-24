"""
Biosignature molecule catalog and templates.
"""
import numpy as np


BIOSIGNATURE_MOLECULES = {
    "H2O": {"type": "solvent/habitability", "wavelength_range": (0.9, 3.0)},
    "CH4": {"type": "biosignature/methanogenesis", "wavelength_range": (1.6, 3.5)},
    "CO2": {"type": "background/habitability", "wavelength_range": (2.0, 4.5)},
    "O2": {"type": "biosignature/photosynthesis", "wavelength_range": (0.7, 1.3)},
    "O3": {"type": "biosignature/photochemical", "wavelength_range": (9.0, 10.0)},
    "N2O": {"type": "biosignature/denitrification", "wavelength_range": (3.8, 4.6)},
    "NH3": {"type": "biosignature/cold-planets", "wavelength_range": (10.0, 11.0)},
    "PH3": {"type": "biosignature/reducing", "wavelength_range": (4.0, 4.5)},
}


def get_template(molecule: str, resolving_power: float = 100):
    """
    Get a theoretical transmission/emission template for a molecule.

    In a full implementation, this would fetch from a database like ExoMol or HITRAN.
    For this library version, we generate a synthetic template for demonstration.

    Parameters
    ----------
    molecule : str
        The chemical formula (e.g., 'H2O', 'CH4').
    resolving_power : float, optional
        The spectral resolving power R = λ/Δλ of the requested template. Default 100.

    Returns
    -------
    wavelength : np.ndarray
        Template wavelength grid (microns).
    depth : np.ndarray
        Template transit depth or cross-section (normalized).

    Raises
    ------
    ValueError
        If the molecule is not in the catalog.

    Examples
    --------
    >>> wl, depth = get_template("H2O", resolving_power=100)
    """
    if molecule not in BIOSIGNATURE_MOLECULES:
        raise ValueError(f"Molecule {molecule} not found in catalog.")

    wmin, wmax = BIOSIGNATURE_MOLECULES[molecule]["wavelength_range"]
    
    # Generate a logarithmic wavelength grid based on resolving power
    n_points = int(resolving_power * np.log(wmax / wmin))
    wl = np.geomspace(wmin, wmax, n_points)
    
    # Generate a synthetic "template" with some peaks
    # (In reality, use `pooch` to download cross-sections)
    np.random.seed(hash(molecule) % 100000)
    n_lines = 5
    centers = np.random.uniform(wmin, wmax, n_lines)
    widths = centers / resolving_power
    depths = np.random.uniform(0.1, 1.0, n_lines)

    depth = np.zeros_like(wl)
    for c, w, d in zip(centers, widths, depths):
        depth += d * np.exp(-0.5 * ((wl - c) / w) ** 2)

    return wl, depth
