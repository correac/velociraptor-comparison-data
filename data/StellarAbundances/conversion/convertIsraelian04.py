from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Israelian_2004.txt"

output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# compute COLIBRE assumed abundances ( Asplund et al. 2009 )
Fe_over_H = 7.5
O_over_H = 8.69
N_over_H = 7.83
O_over_Fe = O_over_H - Fe_over_H
N_over_Fe = N_over_H - Fe_over_H
N_over_O = N_over_H - O_over_H

# tabulate/compute the same ratios. These values are taken from Israelian+ 2004
Fe_over_H_AG89 = 7.67
O_over_H_AG89 = 8.93
N_over_H_AG89 = 8.05
N_over_O_AG89 = N_over_H_AG89 - O_over_H_AG89
O_over_Fe_AG89 = O_over_H_AG89 - Fe_over_H_AG89
N_over_Fe_AG89 = N_over_H_AG89 - Fe_over_H_AG89

element_list = ["NFe", "OFe", "NO"]
correction = np.array([N_over_Fe_AG89 - N_over_Fe,
                       O_over_Fe_AG89 - O_over_Fe,
                       N_over_O_AG89 - N_over_O])
name_short = ["[N/Fe]","[O/Fe]","[N/O]"]

data = np.loadtxt(input_filename, usecols=[0,1,3,5])
select = np.where(data[:,3]!=0)[0]

for i, element in enumerate(element_list):

    FeH = data[select, 0] + Fe_over_H_AG89 - Fe_over_H
    XFe = data[select, i + 1] + correction[i]
    if i<=1: XFe -= data[select, 0] # [N/Fe]

    x = unyt.unyt_array(FeH * unyt.dimensionless)
    y = unyt.unyt_array(XFe * unyt.dimensionless)

    ###########
    # Meta-data
    output_filename = "Israelian_2004_"+element_list[i]+"_FeH.hdf5"

    comment = (
        "Solar abundances are taken from Asplund et al. (2009)."
    )
    citation = "Israelian et al. (2004), MW"
    bibcode = "A&A 421, 649–658 (2004)"
    name = name_short[i]+" as a function of [Fe/H]"
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
