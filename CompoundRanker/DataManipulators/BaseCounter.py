from ..database import query_db
import sys
import time

class BaseCounter (object):

    @property
    def table_name(self):
        raise Exception("table_name property must be defined")

    def __init__(self):
        self.data = []

    def counter(self, CID):
        raise Exception("counter must be implemented")

    def count(self, dataset_id):
        query = "SELECT t2.id as compound_id, t2.cid from metabolites t1 " \
                "LEFT JOIN pubchem_compounds t2 ON t2.metab_ID = t1.id " \
                "LEFT JOIN pubchem_counts t3 ON t3.compound_id = t2.id " \
                "WHERE t3.compound_id is NULL AND t1.dataset_id is ? AND t2.cid is NOT NULL"
        results = query_db(query, dataset_id)
        sys.stdout.write(str(results))
        sys.stdout.flush()
        count = len(results)

        response = []
        for i, result in enumerate(results):
            compound_id = result['compound_id']
            cid = result['cid']
            sys.stdout.write("Getting counts for CID: %s \n" % cid)
            sys.stdout.flush()

            response.append({
                'compound_id': compound_id,
                'count': self.counter(cid),
            })

            # Progress
            perc = ((i+1)/count) * 100
            sys.stdout.write("%s%% \n" % perc)
            sys.stdout.flush()

        self.data = response
        return self


    def save(self):
        query = "INSERT OR REPLACE INTO {tableName}(compound_id, id, count)" \
                "VALUES (" \
                "COALESCE((SELECT compound_id from pubchem_counts WHERE compound_id = :compound_id), :compound_id), " \
                "(SELECT id from {tableName} WHERE compound_id = :compound_id)," \
                ":count" \
                ")".format(tableName = self.table_name)
        query_db(query, self.data, many=True)