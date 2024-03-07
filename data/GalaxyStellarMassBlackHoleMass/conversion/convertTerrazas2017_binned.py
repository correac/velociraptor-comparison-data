from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_sim = cosmology.h

output_filename = "Terrazas2017_binned.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = np.loadtxt("../raw/Terrazas2017_binned.txt")

# Read in stellar masses
M_star = (10 ** data[:, 0]) * unyt.Solar_Mass
M_star_low = (10 ** data[:, 1]) * unyt.Solar_Mass
M_star_high = (10 ** data[:, 2]) * unyt.Solar_Mass

# Calculate scatter
M_star_scatter_low = M_star - M_star_low
M_star_scatter_high = M_star_high - M_star
M_star_scatter = unyt.unyt_array(
    (M_star_scatter_low, M_star_scatter_high), units=unyt.Solar_Mass
)

# Read in BH mass - stellar mass ratios and convert to BH mass
M_bh = (10 ** data[:, 3]) * M_star
M_bh_low = (10 ** data[:, 4]) * M_star
M_bh_high = (10 ** data[:, 5]) * M_star

# Calculate scatter
M_bh_scatter_low = M_bh - M_bh_low
M_bh_scatter_high = M_bh_high - M_bh
M_bh_scatter = unyt.unyt_array(
    (M_bh_scatter_low, M_bh_scatter_high), units=unyt.Solar_Mass
)


# Meta-data
comment = (
    "Binned median galaxy stellar masses and black hole masses from Terrazas et "
    "al. (2017) (2023MNRAS.518.2177G). The BH masses for active and passive "
    "galaxies are weighted by using passive fractions of galaxies as a function "
    "of stellar mass from Gilbank et al. (2010) (2010MNRAS.405.2594G)."
)
citation = "Terrazas et al. (2017), binned"
bibcode = "2017ApJ...844..170T"
name = "Black hole mass - stellar mass relation at z = 0"
plot_as = "points"
redshift = 0.0
redshift_lower = 0.0
redshift_upper = 0.1
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_star, scatter=M_star_scatter, comoving=True, description="Stellar mass ($M_*$)"
)
processed.associate_y(
    M_bh, scatter=M_bh_scatter, comoving=True, description="Black hole mass"
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift, redshift_lower, redshift_upper)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
