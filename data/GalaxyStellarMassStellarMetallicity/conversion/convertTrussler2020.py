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

input_filename = "../raw/Trussler2020.txt"

output_filename = "Trussler2020.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

raw_data = np.loadtxt(input_filename)

comment = """Stellar metallicity difference between passive central galaxies and star-forming central galaxies 
    as a function of stellar mass. Uses the spectroscopic sample of galaxies in the SDSS DR7. Converted from Kroupa 
    to Chabrier initial mass function. The galaxy population is divided into star-forming and passive galaxies based on 
    the distance from the star formation main sequence. Uses the spectral fitting code FIREFLY to obtain stellar
    metallicities and stellar ages for each galaxy."""
citation = "Trussler et al. (2020)"
bibcode = "2020MNRAS.491.5406T"
name = "Stellar mass - Stellar metallicity difference b/w passive and active galaxies"
plot_as = "line"
redshift = 0.0

processed = ObservationalData()
processed.associate_citation(citation, bibcode)
processed.associate_name(name)
processed.associate_comment(comment)
processed.associate_cosmology(cosmology)


M_star = unyt.unyt_array(10 ** raw_data[:, 1], "Msun")
delta_Z = unyt.unyt_array(raw_data[:, 2], "dimensionless")
delta_Z_err = unyt.unyt_array(raw_data[:, 3], "dimensionless")

processed.associate_x(
    M_star, scatter=None, comoving=True, description="Galaxy Stellar Mass"
)
processed.associate_y(
    delta_Z,
    scatter=delta_Z_err,
    comoving=True,
    description="Stellar metallicity difference b/w passive and active galaxies",
)

processed.associate_redshift(redshift)
processed.associate_plot_as(plot_as)

output_path = f"{output_directory}/{output_filename}"

if os.path.exists(output_path):
    os.remove(output_path)

processed.write(filename=output_path)
