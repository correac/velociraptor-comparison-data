from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import re
import sys
import itertools as it

ORIGINAL_H = 0.7


def load_file_and_split_by_z(raw_file_name):
    """
    Read the data file and do all the mucking around needed to extract a list of the
    redshift bins for which the GDMF is tabulated, along with the corresponding GDMF
    values and their errors.
    The number and spacing of the stellar mass bins vary with z; they are given in the
    first column of the returned array.

    raw_file_name: the file name of the raw data file to extract the GDMF from
    """

    data = np.genfromtxt(raw_file_name, comments="#")

    # array of the lower redshift bin edges for each GDMF
    z_bins_arr = np.unique(data[:, -2])

    gdmf_arr = []
    for zlow in z_bins_arr:
        bdx = data[:, -2] == zlow
        gdmf_arr.append(data[bdx, :-2])

    return z_bins_arr, gdmf_arr


def process_for_redshift(z, gdmf_and_Mstar_at_z):
    """
    Output an HDF5 file containing the GDMF at a given redshift.

    z: the redshift to produce the GDMF for. The given value corresponds to the lower
    edge of a range in redshift of width 0.5, except for the first bin 0.2 < z < 0.5,
    and the last bin 3.0 < z < 4.0
    gdmf_and_mstar_at_z: the array containing stellar mass bins and the GDMF at the
    chosen redshift
    """

    processed = ObservationalData()

    comment = (
        "Beeston et al. (2018). Obtained using H-ATLAS+GAMA"
        f"data, h-corrected for SWIFT using Cosmology: {cosmology.name}."
    )
    citation = "Beeston et al. (2018)"
    bibcode = "2018MNRAS.479.1077B"
    name = "GDMF from H-ATLAS+GAMA"
    plot_as = "points"
    redshift = z
    h = cosmology.h

    Mstar_bins = gdmf_and_Mstar_at_z[:, 0]
    M = 10 ** Mstar_bins * (h / ORIGINAL_H) ** (-2) * unyt.Solar_Mass
    Phi = 10 ** gdmf_and_Mstar_at_z[:, 1] * (h / ORIGINAL_H) ** 3 * unyt.Mpc ** (-3)
    # y_scatter should be a 1xN or 2xN array describing offsets from
    # the median point 'y'
    # Errors are log error dz = 1/ln(10) dy/y
    # We want dy = y ln(10) dz
    M_err = (
        (
            10 ** gdmf_and_Mstar_at_z[:, 2][:, None]
            * np.log(10)
            * gdmf_and_Mstar_at_z[:, [2, 3]]
        ).T
        * (h / ORIGINAL_H) ** 3
        * unyt.Solar_Mass
    )

    Phi_err = (
        (
            10 ** gdmf_and_Mstar_at_z[:, 2][:, None]
            * np.log(10)
            * gdmf_and_Mstar_at_z[:, [4, 5]]
        ).T
        * (h / ORIGINAL_H) ** 3
        * unyt.Mpc ** (-3)
    )

    processed.associate_x(
        M, scatter=M_err, comoving=True, description="Galaxy Dust Mass"
    )
    processed.associate_y(Phi, scatter=Phi_err, comoving=True, description="Phi (GDMF)")
    processed.associate_citation(citation, bibcode)
    processed.associate_name(name)
    processed.associate_comment(comment)
    processed.associate_redshift(redshift)
    processed.associate_plot_as(plot_as)
    processed.associate_cosmology(cosmology)

    return processed


def stringify_z(z):
    """
    Eagle-style text formatting of redshift label.
    Example: z=1.5 will be printed as z001p500.

    z: The redshift to produce a label for
    """
    whole = int(z)
    frac = int(1000 * (z - whole))
    return f"z{whole:03d}p{frac:03d}"


# Exec the master cosmology file passed as first argument
# These lines are _required_ and you are required to use
# the cosmology specified (this is an astropy.cosmology
# instance)
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/Beeston2018.txt"

output_filename = "Beeston2018_{}.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# z_bins is a 1-D ndarray containing the lower edges of the redshift bins
# gdmf_and_Mstar is a list of 2D ndarrays, one per redshift
# Each contains five columns as follows:
# log(Mstar) bins, Mstar errors, log(GDMF), GDMF +- errors
z_bins, gdmf_and_Mstar = load_file_and_split_by_z(input_filename)

for z, gdmf_and_Mstar_at_z in zip(z_bins, gdmf_and_Mstar):
    processed = process_for_redshift(z, gdmf_and_Mstar_at_z)

    output_path = f"{output_directory}/{output_filename.format(stringify_z(z))}"

    if os.path.exists(output_path):
        os.remove(output_path)

    processed.write(filename=output_path)
