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

output_filename = "Graham2023_binned.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = np.loadtxt("../raw/Graham2023_binned.txt")

# conversion for Mstar from_Kroupa (2002) to Chabrier (2003) IMF
# (table 2, Bernardi et al, 2010, 2010MNRAS.404.2087B)
log_M_offset = 0.05

# Read in stellar masses
M_star = (10 ** (data[:, 0] + log_M_offset)) * unyt.Solar_Mass
M_star_low = (10 ** (data[:, 1] + log_M_offset)) * unyt.Solar_Mass
M_star_high = (10 ** (data[:, 2] + log_M_offset)) * unyt.Solar_Mass

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
    "Binned median galaxy stellar masses and black hole masses from Graham & "
    "Sahu (2023) (2023MNRAS.518.2177G). The BH masses for different "
    "morphological types are weighted by using fractions of those "
    "morphological types as a function of stellar mass from Moffet et al. "
    "(2016) (2016MNRAS.462.4336M). Converted from the Kroupa (2002) to "
    "Chabrier (2003) IMF."
)
citation = "Graham & Sahu (2023), binned"
bibcode = "2023MNRAS.518.2177G"
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
