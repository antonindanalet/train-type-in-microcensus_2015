from pathlib import Path


def get_csv_zugart_zugtyp(year):
    hafas_directory = Path('data/input/HAFAS/' + str(year) + '/')
    # dictionnaire de correspondance entre Zugart et type de train
    list_zugart = []
    list_train_class = []
    dict_train_class_deutsch = {}
    dict_train_class_englisch = {}
    dict_train_class_italienisch = {}
    dict_train_class_franzoesisch = {}

    # ouverture du fichier ZUGART de HAFAS
    with open(hafas_directory / 'ZUGART', 'r') as ZUGART_file:
        # lecture des lignes du fichier
        lines = ZUGART_file.readlines()
        # define the data block in ZUHART-HAFAS
        data_block_zugart_text = False
        data_block_zugart = 0  # 0 = Zugart, 1 = Deutsch, 2 = Englisch, 3 = Franzoesisch, 4 = Italienisch
        # lecture de chaque ligne individuelle
        for line in lines:
            if line not in ['\n', '\r\n']:
                if data_block_zugart_text is False:
                    if line.startswith('<text>'):
                        data_block_zugart_text = True
                    elif data_block_zugart == 0:
                        zugart = line.split(' ')[0]
                        list_zugart.append(zugart)
                        if line[4] == ' ':
                            train_class = line[5]
                        else:
                            train_class = line[4:6]
                        list_train_class.append(train_class)
                    else:
                        raise Exception('Unkown data block in HAFAS-ZUGART data file!')
                else:
                    if line.startswith('<Deutsch>'):
                        data_block_zugart += 1
                    if data_block_zugart == 1:
                        train_class, train_class_name = read_train_class_and_name(line)
                        dict_train_class_deutsch[train_class] = train_class_name
                        if line.startswith('<Englisch>'):
                            data_block_zugart += 1
                    elif data_block_zugart == 2:
                        train_class, train_class_name = read_train_class_and_name(line)
                        dict_train_class_englisch[train_class] = train_class_name
                        if line.startswith('<Franzoesisch>'):
                            data_block_zugart += 1
                    elif data_block_zugart == 3:  # we enter the French data block
                        train_class, train_class_name = read_train_class_and_name(line)
                        dict_train_class_franzoesisch[train_class] = train_class_name
                        if line.startswith('<Italienisch>'):
                            data_block_zugart += 1
                    elif data_block_zugart == 4:  # we enter the Italian data block
                        train_class, train_class_name = read_train_class_and_name(line)
                        dict_train_class_italienisch[train_class] = train_class_name
                    else:
                        raise Exception('Unkown data block in HAFAS-ZUGART data file!')
        if len(list_zugart) != len(list_train_class):
            raise Exception("Erreur de lecture : le nombre de 'zugart' et de classes n'est pas identique !")

    # sauvegarde du resultat dans un fichier CSV
    output_directory = Path('data/output/' + str(year) + '/')
    with open(output_directory / 'zugart_zugtyp.csv', 'w') as zugart_zugtyp_file:
        zugart_zugtyp_file.write('zugart;'
                                 'class_nummer;'
                                 'name;'
                                 'name;'
                                 'nom;'
                                 'nome\n')
        for number_zugart in range(len(list_train_class)):
            train_class = list_train_class[number_zugart]
            zugart_zugtyp_file.write(list_zugart[number_zugart] + ';' +
                                     train_class + ';' +
                                     dict_train_class_deutsch[train_class] + ';' +
                                     dict_train_class_englisch[train_class] + ';' +
                                     dict_train_class_franzoesisch[train_class] + ';' +
                                     dict_train_class_italienisch[train_class] + '\n')


def read_train_class_and_name(line):
    if line.startswith('class0'):
        train_class = line[6]
        train_class_name = line[8:].rstrip()
        return train_class, train_class_name
    elif line.startswith('option'):
        train_class = line[6:8]
        train_class_name = line[9:].rstrip()
        return train_class, train_class_name
    else:
        return None, None