from velociraptor.observations.objects import ObservationalData

import unyt
import numpy as np
import os
import sys
from scipy import stats

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

output_filename = "Carlsten2021.hdf5"
output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

processed = ObservationalData()

bibcode = "10.3847/1538-4357/ac2581"
name = "Galaxy Stellar Mass-Galaxy Size"
plot_as = "points"
redshift = 0.0
comment = """A sample of 223 low-mass satellites from the Exploration of Local Volume Satellites survey, in the mass 
     range 10**5.5 < M* < 10**8.5 Msun. The satellites are selected around massive hosts in the Local Volume. 
     The sample is complete to luminosities of MV <−9 mag and surface brightness of μ0,V < 26.5 mag arcsec**-2. 
     Only distance-confirmed satellites are listed. The distances are determined using the tip of the red giant branch. 
     Kroupa (1998) initial mass function is used in the raw data. Stellar masses are derived based on the integrated 
     luminosity and color using a color–M*/L relation. The effective radii are obtained using a Sersic fit"""
citation = "Carlsten et al. (2021) [local volume]"


data = np.genfromtxt("../raw/Carlsten2021.txt")
log_Mstar = data[:, 12]
r_kpc = data[:, 16] / 1e3

# 0.3-kpc bins
log_Mstar_edges = np.linspace(5.5, 8.5, 11)
log_Mstar_centres = 0.5 * (log_Mstar_edges[:-1] + log_Mstar_edges[1:])

r_kpc_low, _, _ = stats.binned_statistic(
    x=log_Mstar,
    values=r_kpc,
    statistic=lambda y: np.percentile(y, 16),
    bins=log_Mstar_edges,
)
r_kpc_median, _, _ = stats.binned_statistic(
    x=log_Mstar,
    values=r_kpc,
    statistic=lambda y: np.percentile(y, 50),
    bins=log_Mstar_edges,
)
r_kpc_high, _, _ = stats.binned_statistic(
    x=log_Mstar,
    values=r_kpc,
    statistic=lambda y: np.percentile(y, 84),
    bins=log_Mstar_edges,
)

Mstar = 10 ** log_Mstar_centres
Mstar *= kroupa_to_chabrier_mass
Mstar = unyt.unyt_array(Mstar, units=unyt.Solar_Mass)

R = unyt.unyt_array(r_kpc_median, units=unyt.kpc)
dR = unyt.unyt_array(
    [r_kpc_median - r_kpc_low, r_kpc_high - r_kpc_median], units=unyt.kpc
)

processed.associate_x(
    Mstar, scatter=None, comoving=False, description="Galaxy Stellar Mass"
)
processed.associate_y(R, scatter=dR, comoving=False, description="Galaxy size")
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
