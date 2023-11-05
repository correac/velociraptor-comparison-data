from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Nicholls_2017.txt"

output_directory = "../"
output_filename = "Nicholls_2017a.hdf5"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# Read the data
raw = np.loadtxt(input_filename)
logOH = raw[:, 0] * unyt.dimensionless  # 12 + log(O/H)
logCO = raw[:, 1] * unyt.dimensionless  # log(C/O)
logNO = raw[:, 2] * unyt.dimensionless  # log(N/O)

# Meta-data
comment = (
    "The gas-phase oxygen over hydrogen abundance is expressed as 12+log10(O/H), "
    "and the gas-phase carbon over oxygen abundance is expressed as log10(C/O). "
    "The data corresponds to a best-fitting relation (Eq. 3 from Nicholls+)."
)
citation = "Nicholls et al. (2017) (MW)"
bibcode = "2017MNRAS.466.4403N"
name = "Gas phase O/H - C/O relation"
plot_as = "line"
redshift = 0.1

# Write everything
processed = ObservationalData()
processed.associate_x(
    logOH, scatter=None, comoving=True, description="Gas-phase oxygen over hydrogen"
)
processed.associate_y(
    logCO, scatter=None, comoving=True, description="Gas-phase carbon over oxygen"
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_plot_as(plot_as)
processed.associate_redshift(redshift)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)

#######
output_directory = "../"
output_filename = "Nicholls_2017b.hdf5"

# Meta-data
comment = (
    "The gas-phase oxygen over hydrogen abundance is expressed as 12+log10(O/H), "
    "and the gas-phase nitrogen over oxygen abundance is expressed as log10(N/O). "
    "The data corresponds to a best-fitting relation (Eq. 3 from Nicholls+)."
)
name = "Gas phase O/H - N/O relation"

# Write everything
processed = ObservationalData()
processed.associate_x(
    logOH, scatter=None, comoving=True, description="Gas-phase oxygen over hydrogen"
)
processed.associate_y(
    logNO, scatter=None, comoving=True, description="Gas-phase nitrogen over oxygen"
)
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_plot_as(plot_as)
processed.associate_redshift(redshift)
processed.associate_cosmology(cosmology)

output_path = f"{output_directory}/{output_filename}"

processed.write(filename=output_path)
