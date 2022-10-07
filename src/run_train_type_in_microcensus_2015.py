from get_train_category_from_train_number import get_csv_zugnummer_zugart
from get_csv_zugart_zugtyp import get_csv_zugart_zugtyp
from get_csv_etappen_zugtyp import get_csv_etappen_zugtyp


def run_train_type_in_microcensus_2015():
    get_csv_zugnummer_zugart()
    get_csv_zugart_zugtyp(2015)
    get_csv_zugart_zugtyp(2016)
    get_csv_etappen_zugtyp()


if __name__ == '__main__':
    run_train_type_in_microcensus_2015()
