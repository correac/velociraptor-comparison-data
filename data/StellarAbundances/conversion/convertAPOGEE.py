import unyt
import numpy as np
import os
import sys
import h5py

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/APOGEE_data.hdf5"
apogee_dataset = h5py.File(input_filename, "r")
GalR = apogee_dataset["GalR"][:]
Galz = apogee_dataset["Galz"][:]
FE_H = apogee_dataset["FE_H"][:]

output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

element_list = np.array(
    ["C", "MG", "O", "N", "OH", "OHMG", "OMGFE", "NO", "NOOH", "COOH", "CO"]
)

# compute COLIBRE assumed abundances ( Asplund et al. 2009 )
Fe_over_H = 7.5
Mg_over_H = 7.6
O_over_H = 8.69
C_over_H = 8.43
N_over_H = 7.83

Mg_over_Fe_AS09 = Mg_over_H - Fe_over_H
O_over_Fe_AS09 = O_over_H - Fe_over_H
C_over_Fe_AS09 = C_over_H - Fe_over_H
N_over_Fe_AS09 = N_over_H - Fe_over_H
O_over_H_AS09 = O_over_H
N_over_O_AS09 = N_over_H - O_over_H
C_over_O_AS09 = C_over_H - O_over_H

# tabulate/compute the same ratios from Grevesse, Asplund & Sauval (2007)
Fe_over_H_GA07 = 7.45
Mg_over_H_GA07 = 7.53
O_over_H_GA07 = 8.66
C_over_H_GA07 = 8.39
N_over_H_GA07 = 7.78

Mg_over_Fe_GA07 = Mg_over_H_GA07 - Fe_over_H_GA07
O_over_Fe_GA07 = O_over_H_GA07 - Fe_over_H_GA07
C_over_Fe_GA07 = C_over_H_GA07 - Fe_over_H_GA07
N_over_Fe_GA07 = N_over_H_GA07 - Fe_over_H_GA07
N_over_O_GA07 = N_over_H_GA07 - O_over_H_GA07
C_over_O_GA07 = C_over_H_GA07 - O_over_H_GA07

for element in element_list:

    output_filename = "APOGEE_data_{0}.hdf5".format(element)

    if "OH" in element:
        O_FE = apogee_dataset["O_FE"][:]
        O_H = O_FE + FE_H
        x = O_H + O_over_H_GA07 - O_over_H_AS09
        xlabel = "[O/H]"
        if element == "OHMG":
            MG_FE = apogee_dataset["MG_FE"][:]
            y = MG_FE + Mg_over_Fe_GA07 - Mg_over_Fe_AS09
            name = "[Mg/Fe] as a function of [O/H]".format(element)
            ylabel = "[Mg/Fe]"
        elif element == "NOOH":
            N_Fe = apogee_dataset["N_FE"][:]
            O_Fe = apogee_dataset["O_FE"][:]
            y = N_Fe - O_Fe + N_over_O_GA07 - N_over_O_AS09
            name = "[N/O] as a function of [O/H]".format(element)
            ylabel = "[N/O]"
        elif element == "COOH":
            C_Fe = apogee_dataset["C_FE"][:]
            O_Fe = apogee_dataset["O_FE"][:]
            y = C_Fe - O_Fe + C_over_O_GA07 - C_over_O_AS09
            name = "[C/O] as a function of [O/H]".format(element)
            ylabel = "[C/O]"
        else:  # OFe
            y = O_FE + O_over_Fe_GA07 - O_over_Fe_AS09
            name = "[O/Fe] as a function of [O/H]".format(element)
            ylabel = "[O/Fe]"

    elif element == "NO":
        name = "[N/O] as a function of [Fe/H]".format(element)
        x = FE_H + Fe_over_H_GA07 - Fe_over_H
        xlabel = "[Fe/H]"
        N_Fe = apogee_dataset["N_FE"][:]
        O_Fe = apogee_dataset["O_FE"][:]
        y = N_Fe - O_Fe + N_over_O_GA07 - N_over_O_AS09
        ylabel = "[N/O]".format(element)

    elif element == "CO":
        name = "[C/O] as a function of [Fe/H]".format(element)
        x = FE_H + Fe_over_H_GA07 - Fe_over_H
        xlabel = "[Fe/H]"
        C_Fe = apogee_dataset["C_FE"][:]
        O_Fe = apogee_dataset["O_FE"][:]
        y = C_Fe - O_Fe + C_over_O_GA07 - C_over_O_AS09
        ylabel = "[C/O]".format(element)

    elif element == "OMGFE":
        x = FE_H + Fe_over_H_GA07 - Fe_over_H
        xlabel = "[Fe/H]"
        MG_FE = apogee_dataset["MG_FE"][:]
        O_FE = apogee_dataset["O_FE"][:]
        correction = (
            O_over_Fe_GA07 - O_over_Fe_AS09 - (Mg_over_Fe_GA07 - Mg_over_Fe_AS09)
        )
        y = O_FE - MG_FE + correction
        name = "[O/Mg] as a function of [Fe/H]".format(element)
        ylabel = "[O/Mg]"

    else:  # O, MG, N, or C
        x = FE_H + Fe_over_H_GA07 - Fe_over_H
        xlabel = "[Fe/H]"

        el_FE = apogee_dataset[f"{element}_FE"][:]
        if element == "O":
            y = el_FE + O_over_Fe_GA07 - O_over_Fe_AS09
        if element == "MG":
            y = el_FE + Mg_over_Fe_GA07 - Mg_over_Fe_AS09
        if element == "N":
            y = el_FE + N_over_Fe_GA07 - N_over_Fe_AS09
        if element == "C":
            y = el_FE + C_over_Fe_GA07 - C_over_Fe_AS09

        name = "[{0}/Fe] as a function of [Fe/H]".format(element)
        ylabel = "[{0}/Fe]".format(element)

    x = unyt.unyt_array(x * unyt.dimensionless)
    y = unyt.unyt_array(y * unyt.dimensionless)

    # Meta-data
    description = "The APOGEE chemical abundances taken from APOGEE data access (https://www.sdss.org/dr14/irspec/spectro_data/#catalogs) "
    description += "cross-matched with AstroNN galactocentric distances (https://data.sdss.org/datamodel/files/APOGEE_ASTRONN/apogee_astronn.html). "
    description += "For more information visit ASPCAP documentation (https://www.sdss.org/dr14/irspec/aspcap/)"

    comment = "Solar abundances converted to Asplund et al. (2009)"
    citation = "Holtzman, J. A. et al. (2018); Leung, H.W. & Bovy, Jo (2019b)"
    bibcode = "2018AJ....156..125H; 2019MNRAS.483.3255L"

    details = "The Galactocentric positions (R [kpc], z [kpc], phi [rad]) were calculated assuming that "
    details += "the distance R0 to the Galactic center is 8.125 kpc (Gravity collaboration et al. 2018), the Sun is located 20.8 pc above "
    details += "the Galactic midplane (Bennett & Bovy 2019)."

    contact = "Data file generated by Camila Correa (University of Amsterdam). Email: camila.correa@uva.nl,"
    contact += " website: camilacorrea.com"

    output_path = f"{output_directory}/{output_filename}"

    if os.path.exists(output_path):
        os.remove(output_path)

    ## Output in file
    with h5py.File(output_path, "w") as data_file:

        Header = data_file.create_group("Header")

        Header.attrs["Description"] = np.string_(description)
        Header.attrs["Citation"] = np.string_(citation)
        Header.attrs["Comment"] = np.string_(comment)
        Header.attrs["Bibcode"] = np.string_(bibcode)
        Header.attrs["Contact"] = np.string_(contact)
        Header.attrs["Details"] = np.string_(details)
        Header.attrs["Data"] = np.string_(name)

        dataset = data_file.create_dataset("x", data=x)
        dataset.attrs["Description"] = np.string_(xlabel)
        dataset = data_file.create_dataset("y", data=y)
        dataset.attrs["Description"] = np.string_(ylabel)

        dataset = data_file.create_dataset("GalR", data=GalR)
        dataset.attrs["Description"] = np.string_(
            "Galactocentric radial distance. Unit: [kpc]."
        )
        dataset = data_file.create_dataset("Galz", data=Galz)
        dataset.attrs["Description"] = np.string_(
            "Galactocentric azimuthal distance. Unit: [kpc]."
        )
