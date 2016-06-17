import sys

from CompoundRanker.database import get_db,query_db
from CompoundRanker import app
from requests import exceptions, get


class CIDGatherer(object):
    def harvest(self):
        """
        Harvest all of the CIDs from PubChem
        :return: List of tuples [(cid, metab_id),]
        """
        # Query only returns the metabolites that don't already have CIDs associated
        query = "SELECT t1.id, t1.cas from metabolites t1 " \
                "LEFT JOIN pubchem_compounds t2 ON t2.metab_ID = t1.id " \
                "WHERE t2.metab_ID is NULL "
        results = query_db(query)
        count = len(results)

        since_wait = 0
        since_report = 0

        cid_metab_id_map = [] # List of tuples
        for i, result in enumerate(results):
            since_wait += 1
            since_report += 1


            if since_wait > 2:
                sys.stdout.write("Waiting 1 second \n")
                sys.stdout.flush()
                since_wait = 0

            if since_report > 49:
                sys.stdout.write(str(cid_metab_id_map))
                sys.stdout.write("\n")
                sys.stdout.flush()
                since_report = 0

            cids = self.get_cids(result['cas'])
            metab_id = result['id']
            if cids:
                for cid in cids:
                    cid_metab_id_map.append((cid, metab_id))

            # Progress
            perc = ((i+1)/count) * 100
            sys.stdout.write("%s%% \n" % perc)
            sys.stdout.flush()

        return cid_metab_id_map



    def get_cids(self, cas):
        """
        Use the PubChem API to get the CID
        :param cas: string - CAS identifier
        :return: list of CIDs
        """
        uri = "http://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/%s/cids/json" \
              "?email=%s"

        try:
            response = get((uri % (cas, app.config['ADMIN_EMAIL']))).json()
            try:
                cids = response['IdentifierList']['CID']
                return cids
            except KeyError:
                return None

        except (exceptions.ConnectionError, TimeoutError, exceptions.Timeout,
                exceptions.ConnectTimeout, exceptions.ReadTimeout) as e:
            # Error. return the error and the CAS number that this error occured on
            sys.stderr.write("Error: %s. Occurred on CAS: %s", (e, cas))
            sys.stderr.flush()
            sys.stdout.flush()

    def save(self, cid_metab_id_map):
        insert_query = "INSERT INTO pubchem_compounds(CID, metab_ID) VALUES (?, ?)"
        return query_db(insert_query, cid_metab_id_map, many=True)
