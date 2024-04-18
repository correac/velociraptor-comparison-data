import unyt
import numpy as np
import os
import sys
import h5py

# Exec the master cosmology file passed as first argument
with open(sys.argv[1], "r") as handle:
    exec(handle.read())

input_filename = "../raw/2process_APOGEE_data.hdf5"
apogee_dataset = h5py.File(input_filename, "r")
GalR = apogee_dataset["GalR"][:]
Galz = apogee_dataset["Galz"][:]

output_directory = "../"

if not os.path.exists(output_directory):
    os.mkdir(output_directory)

element_list = np.array(
    ["ASPCAP_MGHOMG","BAWLAS_MGHOMG","ASPCAP_MGHCNMG","BAWLAS_MGHCNMG",
     "ASPCAP_MGHOH","BAWLAS_MGHOH","ASPCAP_OMG","BAWLAS_OMG",
     "ASPCAP_MGFEOH","BAWLAS_MGFEOH","ASPCAP_MGFE","ASPCAP_SIFE"]
)

# compute COLIBRE assumed abundances ( Asplund et al. 2009 )
Fe_over_H_AS09 = 7.5
Mg_over_H_AS09 = 7.6
O_over_H_AS09 = 8.69
C_over_H_AS09 = 8.43
N_over_H_AS09 = 7.83
Si_over_H_AS09 = 7.51

Mg_over_Fe_AS09 = Mg_over_H_AS09 - Fe_over_H_AS09
O_over_Fe_AS09 = O_over_H_AS09 - Fe_over_H_AS09
C_over_Fe_AS09 = C_over_H_AS09 - Fe_over_H_AS09
N_over_Fe_AS09 = N_over_H_AS09 - Fe_over_H_AS09
O_over_H_AS09 = O_over_H_AS09
N_over_O_AS09 = N_over_H_AS09 - O_over_H_AS09
C_over_O_AS09 = C_over_H_AS09 - O_over_H_AS09
O_over_Mg_AS09 = O_over_H_AS09 - Mg_over_H_AS09
Si_over_Fe_AS09 = Si_over_H_AS09 - Fe_over_H_AS09

# tabulate/compute the same ratios from Grevesse, Asplund & Sauval (2007)
Fe_over_H_GA07 = 7.45
Mg_over_H_GA07 = 7.53
O_over_H_GA07 = 8.66
C_over_H_GA07 = 8.39
N_over_H_GA07 = 7.78
Si_over_H_GA07 = 7.51

Mg_over_Fe_GA07 = Mg_over_H_GA07 - Fe_over_H_GA07
O_over_Fe_GA07 = O_over_H_GA07 - Fe_over_H_GA07
C_over_Fe_GA07 = C_over_H_GA07 - Fe_over_H_GA07
N_over_Fe_GA07 = N_over_H_GA07 - Fe_over_H_GA07
N_over_O_GA07 = N_over_H_GA07 - O_over_H_GA07
C_over_O_GA07 = C_over_H_GA07 - O_over_H_GA07
O_over_Mg_GA07 = O_over_H_GA07 - Mg_over_H_GA07
Si_over_Fe_GA07 = Si_over_H_GA07 - Fe_over_H_GA07

for element in element_list:

    output_filename = "2process_APOGEE_{0}.hdf5".format(element)

    if "MGH" in element:
        MG_H = apogee_dataset["MG_H_ASPCAP_corrected"][:]
        x = MG_H + Mg_over_H_GA07 - Mg_over_H_AS09
        xlabel = "[Mg/H]"

        if element == "ASPCAP_MGHOMG":
            O_H = apogee_dataset["O_H_ASPCAP_corrected"][:]
            MG_H = apogee_dataset["MG_H_ASPCAP_corrected"][:]
            y = O_H - MG_H + O_over_Mg_GA07 - O_over_Mg_AS09
            name = "[O/Mg] as a function of [Mg/H]".format(element)
            ylabel = "[O/Mg]"
        elif element == "ASPCAP_MGHCNMG":
            CN_H = apogee_dataset["CN_H_ASPCAP_corrected"][:]
            MG_H = apogee_dataset["MG_H_ASPCAP_corrected"][:]
            y = CN_H - MG_H
            name = "[(C+N)/Mg] as a function of [Mg/H]".format(element)
            ylabel = "[(C+N)/Mg]"
        elif element == "ASPCAP_MGHOH":
            O_H = apogee_dataset["O_H_ASPCAP_corrected"][:]
            y = O_H + O_over_H_GA07 - O_over_H_AS09
            name = "[O/H] as a function of [Mg/H]".format(element)
            ylabel = "[O/H]"

        elif element == "BAWLAS_MGHOMG":
            O_H = apogee_dataset["O_H_BAWLAS_corrected"][:]
            MG_H = apogee_dataset["MG_H_ASPCAP_corrected"][:]
            y = O_H - MG_H + O_over_Mg_GA07 - O_over_Mg_AS09
            name = "[O/Mg] as a function of [Mg/H]".format(element)
            ylabel = "[O/Mg]"
        elif element == "BAWLAS_MGHCNMG":
            CN_H = apogee_dataset["CN_H_BAWLAS_corrected"][:]
            MG_H = apogee_dataset["MG_H_ASPCAP_corrected"][:]
            y = CN_H - MG_H
            name = "[(C+N)/Mg] as a function of [Mg/H]".format(element)
            ylabel = "[(C+N)/Mg]"
        elif element == "BAWLAS_MGHOH":
            O_H = apogee_dataset["O_H_BAWLAS_corrected"][:]
            y = O_H + O_over_H_GA07 - O_over_H_AS09
            name = "[O/H] as a function of [Mg/H]".format(element)
            ylabel = "[O/H]"

    elif "MGFEOH" in element:
        if element == "ASPCAP_MGFEOH":
            O_H = apogee_dataset["O_H_ASPCAP_corrected"][:]
        elif element == "BAWLAS_MGFEOH":
            O_H = apogee_dataset["O_H_BAWLAS_corrected"][:]

        x = O_H + O_over_H_GA07 - O_over_H_AS09
        MG_H = apogee_dataset["MG_H_ASPCAP_corrected"][:]
        FE_H = apogee_dataset["FE_H_ASPCAP_corrected"][:]
        correction = Mg_over_H_GA07 - Mg_over_H_AS09 - (Fe_over_H_GA07 - Fe_over_H_AS09)
        y = MG_H - FE_H + correction
        xlabel = "[O/H]"
        ylabel = "[Mg/Fe]"
        name = "[Mg/Fe] as a function of [O/H]".format(element)

    else:  # Other ..
        FE_H = apogee_dataset["FE_H_ASPCAP_corrected"][:]
        x = FE_H + Fe_over_H_GA07 - Fe_over_H_AS09
        xlabel = "[Fe/H]"
        if element == "ASPCAP_OMG":
            O_H = apogee_dataset["O_H_ASPCAP_corrected"][:]
            MG_H = apogee_dataset["MG_H_ASPCAP_corrected"][:]
            y = O_H - MG_H + O_over_Mg_GA07 - O_over_Mg_AS09
            name = "[O/Mg] as a function of [Fe/H]".format(element)
            ylabel = "[O/Mg]".format(element)
        if element == "BAWLAS_OMG":
            O_H = apogee_dataset["O_H_BAWLAS_corrected"][:]
            MG_H = apogee_dataset["MG_H_ASPCAP_corrected"][:]
            y = O_H - MG_H + O_over_Mg_GA07 - O_over_Mg_AS09
            name = "[O/Mg] as a function of [Fe/H]".format(element)
            ylabel = "[O/Mg]".format(element)
        if element == "ASPCAP_MGFE":
            MG_H = apogee_dataset["MG_H_ASPCAP_corrected"][:]
            FE_H = apogee_dataset["FE_H_ASPCAP_corrected"][:]
            correction = Mg_over_H_GA07 - Mg_over_H_AS09 - (Fe_over_H_GA07 - Fe_over_H_AS09)
            y = MG_H - FE_H + correction
            ylabel = "[Mg/Fe]"
            name = "[Mg/Fe] as a function of [Fe/H]".format(element)
        if element == "ASPCAP_SIFE":
            SI_H = apogee_dataset["SI_H_ASPCAP_corrected"][:]
            FE_H = apogee_dataset["FE_H_ASPCAP_corrected"][:]
            correction = Si_over_H_GA07 - Si_over_H_AS09 - (Fe_over_H_GA07 - Fe_over_H_AS09)
            y = SI_H - FE_H + correction
            ylabel = "[Si/Fe]"
            name = "[Si/Fe] as a function of [Fe/H]".format(element)


    x = unyt.unyt_array(x * unyt.dimensionless)
    y = unyt.unyt_array(y * unyt.dimensionless)

    # Meta-data
    description = "APOGEE chemical abundances taken from the two process residual abundance catalog (https://zenodo.org/records/10659205) "
    description += "by Sit et al. (2024) (https://ui.adsabs.harvard.edu/abs/2024arXiv240308067S/abstract). "
    description += "The corrected APOGEE data from Sit et al. (2024) has been cross-matched with AstroNN galactocentric distances (https://data.sdss.org/datamodel/files/APOGEE_ASTRONN/apogee_astronn.html). "
    description += "For more information visit ASPCAP documentation (https://www.sdss.org/dr14/irspec/aspcap/)."

    comment = "Solar abundances converted to Asplund et al. (2009)"
    citation = "Holtzman, J. A. et al. (2018); Leung, H.W. & Bovy, Jo (2019b); Sit, T., et al. (2024)"
    bibcode = "2018AJ....156..125H; 2019MNRAS.483.3255L; eprint arXiv:2403.08067"

    details = "The Galactocentric positions (R [kpc], z [kpc], phi [rad]) were calculated in AstroNN assuming that "
    details += "the distance R0 to the Galactic center is 8.125 kpc (Gravity collaboration et al. 2018), the Sun is located 20.8 pc above "
    details += "the Galactic midplane (Bennett & Bovy 2019)."

    contact = "Data file generated by Camila Correa (CEA Paris-Saclay). Email: camila.correa@cea.fr,"
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
