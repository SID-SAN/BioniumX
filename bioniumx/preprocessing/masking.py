"""
Wavelength masking and bad pixel removal.
"""
import numpy as np
from bioniumx.core import BioniumXObject


def mask_wavelength_regions(spectrum: BioniumXObject, regions: list):
    """
    Mask out specific wavelength regions from a spectrum.

    Useful for removing known bad pixels, telluric bands, or instrument artifacts.

    Parameters
    ----------
    spectrum : BioniumXObject
        The input spectrum.
    regions : list of tuples
        List of (min_wl, max_wl) tuples specifying regions to exclude.

    Returns
    -------
    masked : BioniumXObject
        A new spectrum object with the specified regions removed.

    Examples
    --------
    >>> spec_clean = mask_wavelength_regions(spec, [(1.35, 1.45), (1.8, 1.95)])
    """
    wl = spectrum.wavelength
    mask = np.ones(len(wl), dtype=bool)

    for (wmin, wmax) in regions:
        mask &= ~((wl >= wmin) & (wl <= wmax))

    if hasattr(spectrum, 'transit_depth'):
        return type(spectrum)(
            wavelength=wl[mask],
            transit_depth=spectrum.transit_depth[mask],
            err=spectrum.err[mask],
            **spectrum.meta
        )
    elif hasattr(spectrum, 'flux'):
        return type(spectrum)(
            wavelength=wl[mask],
            flux=spectrum.flux[mask],
            err=spectrum.err[mask],
            **spectrum.meta
        )
    else:
        raise TypeError("Object must have either 'transit_depth' or 'flux' attribute.")
