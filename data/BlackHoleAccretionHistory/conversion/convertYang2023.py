from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_obs = 0.7
h_sim = cosmology.h

input_filename = "../raw/Yang_2023.txt"

output_filename = "Yang2023.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename)
z = unyt.unyt_array(raw[:, 0], "dimensionless")
z_low = unyt.unyt_array(raw[:, 1], "dimensionless")
z_high = unyt.unyt_array(raw[:, 2], "dimensionless")

# Convert to scale factor
a = 1 / (1 + z)
a_low = 1 / (1 + z_high)
a_high = 1 / (1 + z_low)
a_scatter = unyt.unyt_array((a - a_low, a_high - a))

BHARD = unyt.unyt_array(10 ** raw[:, 3], "Msun / yr / Mpc**3")
BHARD_low = unyt.unyt_array(10 ** raw[:, 4], "Msun / yr / Mpc**3")
BHARD_high = unyt.unyt_array(10 ** raw[:, 5], "Msun / yr / Mpc**3")

# Correct for cosmology
BHARD = BHARD * (h_sim / h_obs) ** -2
BHARD_low = BHARD_low * (h_sim / h_obs) ** -2
BHARD_high = BHARD_high * (h_sim / h_obs) ** -2
BHARD_scatter = unyt.unyt_array((BHARD - BHARD_low, BHARD_high - BHARD))

# Meta-data
comment = (
    "JWST observations in infrared."
    f"h-corrected for SWIFT using cosmology: {cosmology.name}. "
)
citation = "Yang et al. (2023) (infrared, JWST)"
bibcode = "2023ApJ...950L...5Y"
name = "Redshift - Black-hole Mass Accretion Rate Density relation"
plot_as = "points"
redshift = np.mean(z)
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(a, scatter=a_scatter, comoving=True, description="Scale-factor")
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
