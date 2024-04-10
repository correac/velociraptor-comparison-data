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

h_obs = 0.7
h_sim = cosmology.h

input_filename = f"../raw/Revalski2024.txt"
raw = np.loadtxt(input_filename)

comment = (
    "The relationship between stellar mass and gas-phase metallicity "
    "from the MUSE Ultra Deep Field. "
    "Uses Chabrier (2003) initial mass function and h=0.7. "
)
citation = "Revalski et al. (2024)"
bibcode = "2024arXiv240317047R"
name = "Galaxy Stellar Mass - Gas Metallicity"
plot_as = "points"

z_lo = raw[:, 0]
z_hi = raw[:, 1]
Mstar = 10.0 ** raw[:, 2] * (h_sim / h_obs) ** -2 * unyt.Solar_Mass
metal = raw[:, 4] * unyt.dimensionless
metal_err_hi = raw[:, 5] * unyt.dimensionless
metal_err_lo = raw[:, 6] * unyt.dimensionless

multi_z = MultiRedshiftObservationalData()
multi_z.associate_citation(citation, bibcode)
multi_z.associate_name(name)
multi_z.associate_comment(comment)
multi_z.associate_cosmology(cosmology)
multi_z.associate_maximum_number_of_returns(1)

for zmin in [0.23, 1.0]:
    processed = ObservationalData()

    mask = z_lo == zmin
    zmax = z_hi[mask][0]
    z = round((zmin + zmax) / 2, 1)

    processed.associate_x(
        Mstar[mask],
        scatter=None,
        comoving=False,
        description="Galaxy Stellar Mass",
    )
    y_scatter = unyt.unyt_array((metal_err_lo[mask], metal_err_hi[mask]))
    processed.associate_y(
        metal[mask],
        scatter=y_scatter,
        comoving=False,
        description="Galaxy Gas Metallicity",
    )
    processed.associate_redshift(z, zmin, zmax)
    processed.associate_plot_as(plot_as)

    multi_z.associate_dataset(processed)

output_path = f"../Revalski2024.hdf5"

if os.path.exists(output_path):
    os.remove(output_path)

multi_z.write(filename=output_path)
