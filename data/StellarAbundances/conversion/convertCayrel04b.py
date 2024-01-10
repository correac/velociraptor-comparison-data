from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Cayrel_2004_b.txt"

output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# compute COLIBRE assumed abundances ( Asplund et al. 2009 )
Fe_over_H = 7.5
O_over_H = 8.69
C_over_H = 8.43
N_over_H = 7.83
O_over_Fe = O_over_H - Fe_over_H
C_over_Fe = C_over_H - Fe_over_H
N_over_Fe = N_over_H - Fe_over_H

# tabulate/compute the same ratios from Anders & Grevesse (1989)
Fe_over_H_AG89 = 7.45
O_over_H_AG89 = 8.74
C_over_H_AG89 = 8.39
N_over_H_AG89 = 7.78

O_over_Fe_AG89 = O_over_H - Fe_over_H
C_over_Fe_AG89 = C_over_H - Fe_over_H
N_over_Fe_AG89 = N_over_H - Fe_over_H

element_list = ["CFe", "NFe", "OFe"]
correction = np.array(
    [C_over_Fe_AG89 - C_over_Fe, N_over_Fe_AG89 - N_over_Fe, O_over_Fe_AG89 - O_over_Fe]
)
name_short = ["[C/Fe]", "[N/Fe]", "[O/Fe]"]

for i, element in enumerate(element_list):

    data = np.loadtxt(input_filename, usecols=[1, i + 2])
    select = np.where(data[:, 1] > -20)[0]
    FeH_cayrel = data[select, 0] + Fe_over_H_AG89 - Fe_over_H
    XFe_cayrel = data[select, 1] + correction[i]
    x = unyt.unyt_array(FeH_cayrel * unyt.dimensionless)
    y = unyt.unyt_array(XFe_cayrel * unyt.dimensionless)

    ###########
    # Meta-data
    output_filename = "Cayrel_2004_" + element_list[i] + "_FeH.hdf5"

    comment = "Solar abundances are taken from Asplund et al. (2009)."
    citation = "Cayrel et al. (2004), MW"
    bibcode = "2004A&A...416.1117C"
    name = name_short[i] + " as a function of [Fe/H]"
    plot_as = "points"
    redshift = 0.0

    # Write everything
    processed = ObservationalData()
    processed.associate_x(x, scatter=None, comoving=False, description="[Fe/H]")
    processed.associate_y(y, scatter=None, comoving=False, description=name_short[i])
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
