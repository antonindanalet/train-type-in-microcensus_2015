def read_zugart_zugtyp(hafas_directory):
    dictionary_zugart_zugtyp = {}

    # ouverture du fichier zugart_zugtyp de HAFAS
    with open(hafas_directory + 'zugart_zugtyp.csv', 'r') as zugart_zugtype_file:
        # lecture des lignes du fichier
        lines = zugart_zugtype_file.readlines()
        # lecture de chaque ligne individuelle
        for line in lines[1:]:
            line_split = line.split(';')
            zugart = line_split[0]
            zugtyp = line_split[1]
            dictionary_zugart_zugtyp[zugart] = zugtyp
    return dictionary_zugart_zugtyp
