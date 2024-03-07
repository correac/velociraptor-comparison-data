from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys
from unyt import speed_of_light

speed_of_light = speed_of_light.to(unyt.cm / unyt.s)

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_obs = 0.7
h_sim = cosmology.h

input_filename = "../raw/Annana_2020.txt"

output_filenames = ["Annana2020_low.hdf5", "Annana2020_high.hdf5"]
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

# Correct for cosmology
BLD = BLD * (h_sim / h_obs) ** -2

# Meta-data
comment = (
    "Mixed-wavelength observations" f"h-corrected using cosmology: {cosmology.name}. "
)
bibcode = "2020ApJ...903...85A"
name = "Redshift - Black-hole Mass Accretion Rate Density relation"
plot_as = "line"
redshift = np.mean(z)
h = h_sim

radiative_efficiencies = [0.1, 0.34]

# Write two files, for different radiative efficiencies
for i in range(2):

    # Convert to BHARD
    BHARD = BLD / (radiative_efficiencies[i] * speed_of_light ** 2)

    # Convert units to Msun * yr^-1 * Mpc^-3
    BHARD = BHARD.to(unyt.Msun / unyt.yr / unyt.Mpc ** 3)

    # Write everything
    citation = f"Ananna et al. (2020) (X-ray, eps_rad = {radiative_efficiencies[i]})"
    processed = ObservationalData()
    processed.associate_x(a, scatter=None, comoving=True, description="Scale-factor")
    processed.associate_y(
        BHARD,
        scatter=None,
        comoving=True,
        description="Black-hole Accretion Rate Density",
    )
    processed.associate_citation(citation, bibcode)
    processed.associate_name(name)
    processed.associate_comment(comment)
    processed.associate_redshift(redshift)
    processed.associate_plot_as(plot_as)
    processed.associate_cosmology(cosmology)

    output_path = f"{output_directory}/{output_filenames[i]}"

    if os.path.exists(output_path):
        os.remove(output_path)

    processed.write(filename=output_path)
