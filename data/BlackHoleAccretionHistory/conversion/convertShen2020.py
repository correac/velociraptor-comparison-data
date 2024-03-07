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

input_filename = "../raw/Shen_2020.txt"

output_filenames = ["Shen2020_low.hdf5", "Shen2020_high.hdf5"]
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename)
z = unyt.unyt_array(raw[:, 0], "dimensionless")

# Convert to scale factor
a = 1 / (1 + z)

# Meta-data
comment = (
    "Data extracted from multi-wavelength observations by Shen et al. (2020)"
    " (2020MNRAS.495.3252S). "
)
bibcode = "2020MNRAS.495.3252S"
name = "Redshift - Black-hole Mass Accretion Rate Density relation"
plot_as = "line"
redshift = np.mean(z)
h = h_sim

for i in range(2):

    # Load two different datasets depending on which fit the authors did
    if i == 0:
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
    if i == 1:
        BLD = (
            10 ** unyt.unyt_array(raw[:, 4], "dimensionless")
            * unyt.erg
            / (unyt.s * unyt.Mpc ** 3)
        )
        BLD_low = (
            10 ** unyt.unyt_array(raw[:, 5], "dimensionless")
            * unyt.erg
            / (unyt.s * unyt.Mpc ** 3)
        )
        BLD_high = (
            10 ** unyt.unyt_array(raw[:, 6], "dimensionless")
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

    citation = f"Shen et al. (2020) (multi-wavelength, fit {i})"

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

    output_path = f"{output_directory}/{output_filenames[i]}"

    if os.path.exists(output_path):
        os.remove(output_path)

    processed.write(filename=output_path)
