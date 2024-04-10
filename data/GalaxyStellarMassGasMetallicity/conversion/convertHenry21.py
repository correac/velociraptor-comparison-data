from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

h_obs = 0.674
h_sim = cosmology.h

input_filename = f"../raw/Henry2021.txt"
raw = np.loadtxt(input_filename)

comment = (
    "The relationship between stellar mass and gas-phase metallicity "
    "from the CANDELS survey. "
    "Uses Chabrier (2003) initial mass function and Planck cosmology."
)
citation = "Henry et al. (2021)"
bibcode = "2021ApJ...919..143H"
name = "Galaxy Stellar Mass - Gas Metallicity"
plot_as = "points"

z = 1.9
zmin = 1.3
zmax = 2.3

Mstar = 10.0 ** raw[:, 0] * (h_sim / h_obs) ** -2 * unyt.Solar_Mass
metal = raw[:, 2] * unyt.dimensionless
metal_err_hi = raw[:, 3] * unyt.dimensionless
metal_err_lo = raw[:, 4] * unyt.dimensionless

processed = ObservationalData()
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_cosmology(cosmology)
processed.associate_redshift(z, zmin, zmax)
processed.associate_plot_as(plot_as)

processed.associate_x(
    Mstar,
    scatter=None,
    comoving=False,
    description="Galaxy Stellar Mass",
)
y_scatter = unyt.unyt_array((metal_err_lo, metal_err_hi))
processed.associate_y(
    metal,
    scatter=y_scatter,
    comoving=False,
    description="Galaxy Gas Metallicity",
)

output_path = f"../Henry2021.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
