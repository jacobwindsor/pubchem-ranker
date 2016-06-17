import csv, sys
from ..database import query_db, get_db


class DataGatherer(object):
    def __init__(self, input_file):
        self.input_file = input_file
        self.reader = csv.reader(self.input_file, delimiter='$') # Must use delimiter that is not in file to accomadte for IUPC names

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.input_file.close()

    def harvest(self, limit=None, offset=None):
        """

        Harvest the data from the file
        :param offset: Integer offset for the row - starts from 0
        :param limit: Interger limit of the rows to iterate over - starts from 0
        :return: list of tuples containing CAS number and IUPAC name
        """
        response = []
        for i, row in enumerate(list(self.reader)[offset:]):
            if limit:
                if i == limit:
                    break

            cas = row[0].split(' ', 1)[0]
            cut_start_iupac = str(row[0].split('(', 1)[1])
            iupac = cut_start_iupac.rsplit(')', 1)[0]

            response.append({
                "CAS": cas,
                "IUPAC": iupac
            })

        return response

    def save(self, data, dataset):
        query = "INSERT INTO datasets(name) VALUES (?)"
        dataset_id = query_db(query, args=[dataset])

        query = "INSERT INTO metabolites(CAS, IUPAC, dataset_id) VALUES (:CAS,:IUPAC, {dataset_id})"\
            .format(dataset_id=dataset_id)
        rv = query_db(query, data, many=True)