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

input_filename = "../raw/Peng15.txt"

output_filename = "Peng2015.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

raw_data = np.loadtxt(input_filename)

comment = """Stellar metallicity difference between passive central galaxies and star-forming central galaxies 
    as a function of stellar mass. Uses Chabrier (2003) initial mass function. The galaxy population is
   divided into star-forming and passive galaxies based on their spectroscopic emission line classifications 
   and rest-frame (U - B) colours. The stellar metallicities and r-band weighted stellar ages are derived from the 
   spectral absorption features of SDSS Data Release 4 spectra."""
citation = "Peng et al. (2015)"
bibcode = "2015Natur.521..192P"
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
