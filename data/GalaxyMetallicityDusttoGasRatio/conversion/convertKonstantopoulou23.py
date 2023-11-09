from velociraptor.observations.objects import (
    MultiRedshiftObservationalData,
    ObservationalData,
)

import unyt
import numpy as np
import os
import sys
import glob

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

# Cosmologies
h_sim = cosmology.h

# conversion for output as a representative 12+log10(OH) value
twelve_plus_log_OH_solar = 8.69

input_filename = "../raw/konstantopoulou23_*.txt"

output_filename = "Konstantopoulou2023.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

data = {}
exgals = ["grbs", "dlas"]


def read_tex_tables():
    """
    Read the LaTex formatted tables for the data, returning a dictionary object.
    """
    for fname in glob.glob("../raw/konstantopoulou23*"):
        abstype = fname.split(".")[-2].split("_")[-1]
        fields = ["Z", "Z_sigma", "DTG", "DTG_sigma", "z"]
        idxs = [-2, -5]
        dset = [[]] * len(fields)
        haszs = True if abstype in exgals else False

        with open(fname) as f:
            lines = f.readlines()
            for line in lines:
                if line[0] == "#":
                    continue
                els = line.split("&")
                inc = 0
                for i in idxs:
                    nums = els[i].split("$\\pm$")
                    if len(nums) < 2:
                        # add value and error
                        dset[inc] = [*dset[inc], np.nan]
                        inc += 1
                        dset[inc] = [*dset[inc], np.nan]
                    else:
                        dset[inc] = [*dset[inc], float(nums[0])]
                        inc += 1
                        dset[inc] = [*dset[inc], float(nums[1])]
                    inc += 1
                if haszs:
                    # add redshift where applicable
                    dset[inc] = [*dset[inc], float(els[1])]
                else:
                    dset[inc] = [*dset[inc], 0.0]
        data[abstype] = np.column_stack(dset)
    return data


def process(zs, data):
    multi_z = MultiRedshiftObservationalData()

    comment = (
        "Konstantopoulou et al. (2023). Obtained using VLT, X-shooter & HST for a combination of"
        "sources: MW, LMC, SMC, QSO-DLA and GRBs."
    )
    citation = "Konstantopoulou et al. (2023)"
    bibcode = "10.48550/arXiv.2310.07709"
    name = "Dust-to-gas ratio as a function of metallicity (represented as Oxygen abundance)"
    plot_as = "points"
    h = cosmology.h

    multi_z.associate_citation(citation, bibcode)
    multi_z.associate_name(name)
    multi_z.associate_comment(comment)
    multi_z.associate_cosmology(cosmology)

    for i in range(len(zs) - 1):
        processed = ObservationalData()

        zcen = (zs[i + 1] + zs[i]) / 2
        redshift = zcen

        combination = []
        for src in data.keys():
            bdx = np.logical_and(
                data[src][:, -1] >= zs[i], data[src][:, -1] < zs[i + 1]
            )
            combination.append(data[src][bdx, :])

        combdat = np.vstack(combination)
        combdat = combdat[~np.isnan(combdat).any(axis=-1)]

        OH = (combdat[:, 0] + twelve_plus_log_OH_solar) * unyt.dimensionless
        OH_err = np.row_stack([combdat[:, 1]] * 2) * unyt.dimensionless

        DTG = combdat[:, 2] * unyt.dimensionless
        DTG_err = np.row_stack([combdat[:, 3]] * 2) * unyt.dimensionless

        processed.associate_x(
            OH, scatter=OH_err, comoving=True, description="Gas Phase 12 + log10(O/H)"
        )
        processed.associate_y(
            DTG, scatter=DTG_err, comoving=True, description="Phi (GDMF)"
        )

        processed.associate_redshift(redshift, zs[i], zs[i + 1])
        processed.associate_plot_as(plot_as)
        multi_z.associate_dataset(processed)

    output_path = f"{output_directory}/{output_filename}"

    if os.path.exists(output_path):
        os.remove(output_path)

    multi_z.write(filename=output_path)


z_bins = [0, 0.5, 1, 2, 3, 7]
data = read_tex_tables()
process(z_bins, data)
