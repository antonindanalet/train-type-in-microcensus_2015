import os.path


def read_zugnummer_zugart(hafas_directory, output_directory):
    if os.path.isfile(output_directory + 'nummer_zugart.csv'):
        dictionary_nummer_zugart = read_zugnummer_zugart_from_csv(output_directory)
    elif os.path.isfile(hafas_directory + 'FPLAN'):
        dictionary_nummer_zugart = read_zugnummer_zugart_from_HAFAS(hafas_directory)
    else:
        raise Exception('No readable file in', hafas_directory)
    return dictionary_nummer_zugart


def read_zugnummer_zugart_from_HAFAS(hafas_directory):
    # dictionnaire de correspondance entre numero et type de train
    dictionary_nummer_zugart = {}

    # ouverture du fichier FPLAN de HAFAS
    with open(hafas_directory + 'FPLAN', 'r') as FPLAN_file:
        # lecture des lignes du fichier
        lines = FPLAN_file.readlines()
        # lecture de chaque ligne individuelle
        for line in lines:
            if line.startswith('*G'):
                # Old form for nummer (with spaces)
                zugart = line.split(' ')[1]
                nummer = line.split('%')[0].split(zugart)[1].lstrip().rstrip()
                dictionary_nummer_zugart[nummer] = zugart
    return dictionary_nummer_zugart


def read_zugnummer_zugart_from_csv(output_directory):
    dictionary_nummer_zugart = {}

    # ouverture du fichier nummer_zugart
    with open(output_directory + 'nummer_zugart.csv', 'r') as nummer_zugart_file:
        # lecture des lignes du fichier
        lines = nummer_zugart_file.readlines()
        # lecture de chaque ligne individuelle
        for line in lines[1:]:
            line_split = line.split(';')
            nummer = line_split[0]
            zugart = line_split[1].rstrip()
            dictionary_nummer_zugart[nummer] = zugart
    return dictionary_nummer_zugart
