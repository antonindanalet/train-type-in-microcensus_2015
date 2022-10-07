import csv
import codecs
import datetime
from HAFAS_utils.read_zugnummer_zugart import read_zugnummer_zugart
from HAFAS_utils.read_zugart_zugtyp import read_zugart_zugtyp


def get_csv_etappen_zugtyp():
    dict_interview_day_from_hhnr = get_interview_day_from_hhnr()
    hafas_directory_2015 = 'data/input/HAFAS/2015/'
    output_directory = 'data/output/'
    dictionary_zugart_zugtyp_2015 = read_zugart_zugtyp(output_directory)
    dictionary_nummer_zugart_2015 = read_zugnummer_zugart(hafas_directory_2015, output_directory)
    hafas_directory_2016 = 'data/input/HAFAS/2016/'
    dictionary_nummer_zugart_2016 = read_zugnummer_zugart(hafas_directory_2016, output_directory)
    dictionary_zugart_zugtyp_2016 = read_zugart_zugtyp(output_directory)
    path_to_trip_legs = 'data/input/MTMC/etappen.csv'
    etappen_reader = csv.reader(codecs.open(path_to_trip_legs, 'rU', encoding='latin1'), delimiter=';')
    row_counter = 0
    list_of_new_rows = []
    for row in etappen_reader:
        if row_counter == 0:
            header = row
            col_counter = 0
            for col in header:
                if col == 'HHNR':
                    hhnr_col = col_counter
                elif col == 'etnr':
                    etnr_col = col_counter
                elif col == 'HAF_FID':
                    haf_fid_col = col_counter
                col_counter += 1
        else:
            hhnr = row[hhnr_col]
            etnr = row[etnr_col]
            haf_fid = row[haf_fid_col]
            interview_day_as_str = dict_interview_day_from_hhnr[hhnr]
            interview_day = datetime.datetime.strptime(interview_day_as_str, '%Y-%m-%d').date()
            if haf_fid != '':
                # Check what was the version of HAFAS used for the HAFAS_ID
                if haf_fid in dictionary_nummer_zugart_2015 and haf_fid not in dictionary_nummer_zugart_2016:
                    zugart = dictionary_nummer_zugart_2015[haf_fid]
                    zugtyp = dictionary_zugart_zugtyp_2015[zugart]
                    source_HAFAS = '2015'
                elif haf_fid not in dictionary_nummer_zugart_2015 and haf_fid in dictionary_nummer_zugart_2016:
                    zugart = dictionary_nummer_zugart_2016[haf_fid]
                    zugtyp = dictionary_zugart_zugtyp_2016[zugart]
                    source_HAFAS = '2016'
                elif haf_fid in dictionary_nummer_zugart_2015 and haf_fid in dictionary_nummer_zugart_2016:
                    zugart_2016 = dictionary_nummer_zugart_2016[haf_fid]
                    zugart_2015 = dictionary_nummer_zugart_2015[haf_fid]
                    source_HAFAS = 'both'
                    if zugart_2015 == zugart_2016:
                        zugart = zugart_2015
                        zugtyp_2015 = dictionary_zugart_zugtyp_2015[zugart]
                        zugtyp_2016 = dictionary_zugart_zugtyp_2016[zugart]
                        if zugtyp_2015 == zugtyp_2016:
                            zugtyp = zugtyp_2015
                        else:
                            raise Exception('Zugtyp-Zugart correspondance has changed between the years')
                    else:
                        # Different Zugart in 2015 and 2016 for the same HAFAS FAHRT ID
                        date_change_in_HAFAS_data = datetime.date(2015, 12, 14)
                        if interview_day < date_change_in_HAFAS_data:
                            zugtyp = dictionary_zugart_zugtyp_2015[zugart]
                        elif interview_day > date_change_in_HAFAS_data:
                            zugtyp = dictionary_zugart_zugtyp_2016[zugart]
                        else:
                            zugtyp = 'NA'
                else:
                    raise Exception('HAFAS ID unknown!', haf_fid, 'for HHNR', hhnr, 'and ETNR', etnr,
                                    'interviewed on', interview_day_as_str)
                new_row = hhnr + ';' + etnr + ';' + haf_fid + ';' + zugtyp + ';' + source_HAFAS + ';' + \
                          str(interview_day) + '\n'
                list_of_new_rows.append(new_row)
        row_counter += 1
    with open(output_directory + 'etappen_zugtyp.csv', 'w') as etappen_zugtyp_file:
        etappen_zugtyp_file.write('hhnr;etnr;haf_fid;zugtyp;fichier HAFAS source;Befragungstag\n')
        for new_row in list_of_new_rows:
            etappen_zugtyp_file.write(new_row)


def get_interview_day_from_hhnr():
    dict_interview_day_from_hhnr = {}
    path_to_ziel_person_csv = 'data/input/MTMC/'
    file_name = 'zp.csv'
    etappen_reader = csv.reader(codecs.open(path_to_ziel_person_csv + file_name, 'r', encoding='latin1'),
                                delimiter=';')
    row_counter = 0
    for row in etappen_reader:
        if row_counter == 0:
            header = row
            col_counter = 0
            for col in header:
                if col == 'HHNR':
                    hhnr_col = col_counter
                elif col == 'BTag':
                    btag_col = col_counter
                col_counter += 1
            row_counter += 1
        else:
            hhnr = row[hhnr_col]
            btag = row[btag_col]
            dict_interview_day_from_hhnr[hhnr] = btag
            row_counter += 1
    return dict_interview_day_from_hhnr
