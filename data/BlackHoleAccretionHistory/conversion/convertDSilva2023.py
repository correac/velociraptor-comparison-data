from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys
from unyt import speed_of_light

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_obs = 0.7
h_sim = cosmology.h

input_filename = "../raw/D'Silva_2023.txt"

output_filename = "DSilva2023.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename)
z = unyt.unyt_array(raw[:, 0], "dimensionless")

# Convert to scale factor
a = 1 / (1 + z)

BLD = (
    10 ** unyt.unyt_array(raw[:, 1], "dimensionless")
    * unyt.erg
    / (unyt.s * unyt.Mpc ** 3)
)
BLD_low = (
    10 ** unyt.unyt_array(raw[:, 2], "dimensionless")
    * unyt.erg
    / (unyt.s * unyt.Mpc ** 3)
)
BLD_high = (
    10 ** unyt.unyt_array(raw[:, 3], "dimensionless")
    * unyt.erg
    / (unyt.s * unyt.Mpc ** 3)
)

# Correct for cosmology
BLD = BLD * (h_sim / h_obs) ** -2
BLD_low = BLD_low * (h_sim / h_obs) ** -2
BLD_high = BLD_high * (h_sim / h_obs) ** -2

# Convert to BHARD
radiative_efficiency = 0.1
speed_of_light = speed_of_light.to(unyt.cm / unyt.s)
BHARD = BLD / (radiative_efficiency * speed_of_light ** 2)
BHARD_low = BLD_low / (radiative_efficiency * speed_of_light ** 2)
BHARD_high = BLD_high / (radiative_efficiency * speed_of_light ** 2)

# Convert units to Msun * yr^-1 * Mpc^-3
BHARD = BHARD.to(unyt.Msun / unyt.yr / unyt.Mpc ** 3)
BHARD_low = BHARD_low.to(unyt.Msun / unyt.yr / unyt.Mpc ** 3)
BHARD_high = BHARD_high.to(unyt.Msun / unyt.yr / unyt.Mpc ** 3)

BHARD_scatter = unyt.unyt_array((BHARD - BHARD_low, BHARD_high - BHARD))

# Meta-data
comment = (
    "Mixed-wavelength observations" f"h-corrected using cosmology: {cosmology.name}. "
)
citation = "D'Silva et al. (2023) (multi-wavelength)"
bibcode = "2023MNRAS.524.1448D"
name = "Redshift - Black-hole Mass Accretion Rate Density relation"
plot_as = "points"
redshift = np.mean(z)
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(a, scatter=None, comoving=True, description="Scale-factor")
processed.associate_y(
    BHARD,
    scatter=BHARD_scatter,
    comoving=True,
    description="Black-hole Accretion Rate Density",
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
