from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_obs = 0.70
h_sim = cosmology.h

input_filename = "../raw/Pouliasis_2024.txt"

output_filenames = ["Pouliasis2024_low.hdf5", "Pouliasis2024_high.hdf5"]
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
    "X-ray observations by Pouliasis et al. (2024). Alternative correction"
    f" by Lusso et al. (2012MNRAS.425..623L) has been applied. "
    f"h-corrected using cosmology: {cosmology.name}. "
)
citation = "Pouliasis et al. (2024) (X-ray, Lusso+ 2012 correction)"
bibcode = "2024arXiv240113515P"
name = "Redshift - Black-hole Mass Accretion Rate Density relation"
plot_as = "line"
redshift = np.mean(z)
h = h_sim

for i in range(2):

    # Load different data depending on which bolometric correction is being applied
    if i == 0:
        BHARD_low = unyt.unyt_array(10 ** raw[:, 1], "Msun / yr / Mpc**3")
        BHARD_high = unyt.unyt_array(10 ** raw[:, 2], "Msun / yr / Mpc**3")
    if i == 1:
        BHARD_low = unyt.unyt_array(10 ** raw[:, 3], "Msun / yr / Mpc**3")
        BHARD_high = unyt.unyt_array(10 ** raw[:, 4], "Msun / yr / Mpc**3")
    BHARD = 0.5 * BHARD_low + 0.5 * BHARD_high

    # Correct for cosmology
    BHARD = BHARD * (h_sim / h_obs) ** -2
    BHARD_low = BHARD_low * (h_sim / h_obs) ** -2
    BHARD_high = BHARD_high * (h_sim / h_obs) ** -2
    BHARD_scatter = unyt.unyt_array((BHARD - BHARD_low, BHARD_high - BHARD))

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
