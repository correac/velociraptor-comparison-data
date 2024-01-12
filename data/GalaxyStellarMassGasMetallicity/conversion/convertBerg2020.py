from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Berg_2020.txt"

output_directory = "../"
output_filename = "Berg_2020.hdf5"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename, usecols=(1, 2, 3, 4), delimiter=",")
logOH_mean = raw[:, 0] * unyt.dimensionless  # log(O/H)+12
logOH_std = raw[:, 1] * unyt.dimensionless  # log(O/H)+12
logNO_mean = raw[:, 2] * unyt.dimensionless  # log(N/O)
logNO_std = raw[:, 3] * unyt.dimensionless  # log(N/O)

# Define the scatter as offset from the mean value
x_scatter = unyt.unyt_array(logOH_std)
y_scatter = unyt.unyt_array(logNO_std)

# Meta-data
comment = (
    "The gas-phase oxygen over hydrogen abundance is expressed as 12+log10(O/H). "
    "The gas-phase nitrogen over oxygen abundance is expressed as log10(N/O). "
    "The error bars give standard deviation of the distribution."
)
citation = "Berg et al. (2020) (CHAOS)"
bibcode = "2020APJ.893.96B"
name = "Gas phase O/H - N/O relation"
plot_as = "points"
redshift = 0.1

# Write everything
processed = ObservationalData()
processed.associate_x(
    logOH_mean,
    scatter=x_scatter,
    comoving=True,
    description="Gas-phase oxygen over hydrogen",
)
processed.associate_y(
    logNO_mean,
    scatter=y_scatter,
    comoving=True,
    description="Gas-phase nitrogen over oxygen",
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
