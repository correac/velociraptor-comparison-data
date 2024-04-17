from velociraptor.observations.objects import (
    ObservationalData,
    MultiRedshiftObservationalData,
)

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmology
h_sim = cosmology.h
h_obs = 0.7

input_filename = "../raw/Lyu23.txt"

output_filename = "Lyu2023.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

raw_data = np.loadtxt(input_filename)

comment = """Stellar metallicity difference between passive central galaxies and star-forming central galaxies 
    as a function of stellar mass. Uses Chabrier (2003) initial mass function. The galaxies 
    with Delta MS > −0.5 are classified as star-forming galaxies, and with Delta MS < −1.5 as passive."""
citation = "Lyu et al. (2023)"
bibcode = "2023ApJ...959....5L"
name = "Stellar mass - Stellar metallicity difference b/w passive and active galaxies"
plot_as = "line"

multi_z = MultiRedshiftObservationalData()
multi_z.associate_citation(citation, bibcode)
multi_z.associate_name(name)
multi_z.associate_comment(comment)
multi_z.associate_cosmology(cosmology)
multi_z.associate_maximum_number_of_returns(1)

for z in [0, 0.5, 1, 2]:
    processed = ObservationalData()

    mask = raw_data[:, 0] == z

    M_star = unyt.unyt_array(10 ** raw_data[:, 1][mask] * (h_sim / h_obs) ** -2, "Msun")
    delta_Z = unyt.unyt_array(raw_data[:, 2][mask], "dimensionless")
    delta_Z_err = unyt.unyt_array(raw_data[:, 3][mask], "dimensionless")

    processed.associate_x(
        M_star, scatter=None, comoving=True, description="Galaxy Stellar Mass"
    )
    processed.associate_y(
        delta_Z,
        scatter=delta_Z_err,
        comoving=True,
        description="Stellar metallicity difference b/w passive and active galaxies",
    )

    processed.associate_redshift(z, z - 0.5, z + 0.5)
    processed.associate_plot_as(plot_as)
    multi_z.associate_dataset(processed)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

multi_z.write(filename=output_path)
