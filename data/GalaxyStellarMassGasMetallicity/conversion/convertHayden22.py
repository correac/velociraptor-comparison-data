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

input_filename_a = "../raw/HaydenPawson_2022a.txt"
input_filename_b = "../raw/HaydenPawson_2022b.txt"

output_directory = "../"
output_filename_a = "HaydenPawson_2022a.hdf5"
output_filename_b = "HaydenPawson_2022b.hdf5"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename_a)
M_star = 10 ** raw[:, 0] * unyt.Solar_Mass * (h_sim / h_obs) ** -2
logNO_median = raw[:, 1] * unyt.dimensionless  # log(N/O)
logNO_lo = raw[:, 2] * unyt.dimensionless  # log(N/O)
logNO_hi = raw[:, 3] * unyt.dimensionless  # log(N/O)

# Define the scatter as offset from the mean value
y_scatter = unyt.unyt_array((logNO_median - logNO_lo, logNO_hi - logNO_median))

# Meta-data
comment = (
    "Data obtained assuming a Chabrier IMF and h=0.7. "
    f"h-corrected for SWIFT using cosmology: {cosmology.name}. "
    "The gas-phase nitrogen over oxygen abundance is expressed as log10(N/O). "
    "The error bars given the 16th and 84th percentile of the distribution."
)
citation = "Hayden-Pawson et al. (2022) (SDSS)"
bibcode = "2004ApJ...613..898T"
name = "Stellar mass - Gas phase N/O relation"
plot_as = "line"
redshift = 0.1
h = h_sim

# Write everything
processed = ObservationalData()
processed.associate_x(
    M_star, scatter=None, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(
    logNO_median, scatter=y_scatter, comoving=True, description="Gas-phase nitrogen over oxygen"
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename_a}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)

#######
# Read the data

raw = np.loadtxt(input_filename_b)
logOH_median = raw[:, 0] * unyt.dimensionless  # 12 + log(O/H)
logNO_median = raw[:, 1] * unyt.dimensionless  # log(N/O)
logNO_lo = raw[:, 2] * unyt.dimensionless  # log(N/O)
logNO_hi = raw[:, 3] * unyt.dimensionless  # log(N/O)

# Define the scatter as offset from the mean value
y_scatter = unyt.unyt_array((logNO_median - logNO_lo, logNO_hi - logNO_median))

# Write everything
processed = ObservationalData()
processed.associate_x(
    logOH_median, scatter=None, comoving=True, description="Gas-phase metallicity"
)
processed.associate_y(
    logNO_median, scatter=y_scatter, comoving=True, description="Gas-phase nitrogen over oxygen"
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_redshift(redshift)
processed.associate_plot_as(plot_as)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename_b}"

processed.write(filename=output_path)