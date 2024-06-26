from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmologies
h_obs = 0.7
h_sim = cosmology.h

output_filename = "Faisst2016_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

M_star = unyt.unyt_array(
    10 ** (np.array([8.83, 9.46, 10.34])) * (h_sim / h_obs) ** -2, "Solar_Mass"
)
Z_gas = unyt.unyt_array([8.05, 8.12, 8.32], "dimensionless")
Z_scatter = unyt.unyt_array(
    np.array([[0.74, 0.52, 0.74], [0.56, 0.33, 0.40]]), "dimensionless"
)

# Meta-data
comment = (
    "Data obtained assuming a Chabrier IMF and h=0.7. "
    f"h-corrected for SWIFT using cosmology: {cosmology.name}. "
    "The metallicity is expressed as 12 + log10(O/H). "
    "In these units the solar metallicity is 8.69."
)
citation = "Faisst et al. (2016)"
bibcode = "2016ApJ...822...29F"
name = "Stellar mass - Gas phase metallicity relation"
plot_as = "points"
redshift = 5.0
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_star, scatter=None, comoving=False, description="Galaxy Stellar Mass"
)
processed.associate_y(
    Z_gas, scatter=Z_scatter, comoving=False, description="Gas phase metallicity"
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
