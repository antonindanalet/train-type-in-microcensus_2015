from pathlib import Path


def get_csv_zugnummer_zugart():
    hafas_directory = Path('data/input/HAFAS/')
    dictionary_nummer_zugart = read_zugnummer_zugart(hafas_directory)
    write_zugnummer_zugart_as_csv(dictionary_nummer_zugart)


def read_zugnummer_zugart(hafas_directory):
    # dictionnaire de correspondance entre numero et type de train
    dictionary_nummer_zugart = {}

    # ouverture du fichier FPLAN de HAFAS
    with open(hafas_directory / 'FPLAN', 'r') as FPLAN_file:
        # lecture des lignes du fichier
        lines = FPLAN_file.readlines()
        # lecture de chaque ligne individuelle
        for line in lines:
            if line.startswith('*G'):
                zugart = line.split(' ')[1]
                nummer = line.split('%')[0].split(zugart)[1].lstrip().rstrip()
                dictionary_nummer_zugart[nummer] = zugart
    return dictionary_nummer_zugart


def write_zugnummer_zugart_as_csv(dictionary_nummer_zugart):
    output_directory = Path('data/output/')
    with open(output_directory / 'nummer_zugart.csv', 'w') as nummer_zugart_file:
        nummer_zugart_file.write('nummer;zugart\n')
        for nummer in dictionary_nummer_zugart:
            nummer_zugart_file.write(nummer + ';' + dictionary_nummer_zugart[nummer] + '\n')


if __name__ == '__main__':
    get_csv_zugnummer_zugart()
