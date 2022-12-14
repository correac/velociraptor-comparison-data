from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

Z_solar_obs = 0.0142
h_sim = cosmology.h

input_filename = "../raw/Yates_2021.txt"

output_filename = "Yates2021_Data.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename)
M_star = 10 ** raw[:, 0] * unyt.Solar_Mass
Z_median = 10 ** raw[:, 1] * unyt.dimensionless * Z_solar_obs / solar_metallicity
Z_std_lo = 10 ** raw[:, 2] * unyt.dimensionless * Z_solar_obs / solar_metallicity
Z_std_hi = 10 ** raw[:, 3] * unyt.dimensionless * Z_solar_obs / solar_metallicity

y_scatter = (
    unyt.unyt_array((Z_median - Z_std_lo, Z_std_hi - Z_median))
)


# Meta-data
comment = (
    "Data obtained from Yates et al. (2021). No need for "
    "h-correction. The metallicity is expressed in units of solar metallicity, using Z=0.0142. "
    f"This has been corrected to use Z_solar={solar_metallicity}. "
)
citation = "Yates et al. (2021, MaNGA)"
bibcode = "2021MNRAS...503...4474Y"
name = "Stellar mass - Stellar metallicity relation"
plot_as = "points"
redshift = 0.1
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_star, scatter=None, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(
    Z_median, scatter=y_scatter, comoving=True, description="Stellar metallicity"
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
