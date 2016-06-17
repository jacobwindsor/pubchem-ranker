import sys, json
from collections import OrderedDict

import time
from requests import get, exceptions

from ..database import query_db
from CompoundRanker import app


class Counter(object):

    def _pubchem_counter(self, cid, collection):
        """
        Use the SDQAgent that PubChem uses on their compound pages to get counts for a collection.

        cid: integer. The pubchem compound identifier
        Collection. String. One of the pubchem collections. E.g. "bioactivity" or "biocollection"

        Returns: Integer count
        """

        uri = 'https://pubchem.ncbi.nlm.nih.gov/sdq/sdqagent.cgi?' \
              'infmt=json&outfmt=json' \
              '&query={"select":["*"],"collection":"%s",' \
              '"where":{"ors":{"cid":"%s"}},"start":1,"limit":1}' % (collection, cid)

        try:
            response = get(uri).json()
            try:
                count = response['SDQOutputSet'][0]['totalCount']
                sys.stdout.write(str(count) + "\n")
                sys.stdout.flush()
                return count
            except KeyError:
                return None

        except (exceptions.ConnectionError, TimeoutError, exceptions.Timeout,
                exceptions.ConnectTimeout, exceptions.ReadTimeout) as e:
            # Error. return the error and the CID number that this error occured on
            # Save what have so far
            sys.stderr.write("Error: %s. Occurred on CID: %s", (e, cid))
            sys.stderr.flush()
            sys.stdout.flush()
            quit()
        except exceptions.ChunkedEncodingError as e:
            sys.stderr.write("Error: %s. Occurred on CID: %s", (e, cid))
            sys.stderr.flush()
            quit()

    def assay_count(self, cid):
        # Use pubchem to count the number of assays
        return self._pubchem_counter(cid, collection="bioactivity")

    def pathway_count(self, cid):
        # Use PubChem to count the number of pathways
        return self._pubchem_counter(cid, collection="biosystem")

    def count(self, dataset_id):
        """
        Precount the hits for the metabolites to reduce page load
        :return: list of dicts
        """

        # Only run counts for the compounds that have no counts
        # If want to run all counts again then must first truncate the tables
        query = "SELECT t2.id as compound_id, t2.cid from metabolites t1 " \
                "LEFT JOIN pubchem_compounds t2 ON t2.metab_ID = t1.id " \
                "LEFT JOIN pubchem_counts t3 ON t3.compound_id = t2.id " \
                "WHERE t3.compound_id is NULL AND t1.dataset_id is ?"
        results = query_db(query, dataset_id)
        count = len(results)

        response = []
        since_wait = 0
        for i, result in enumerate(results):
            if since_wait > 2:
                sys.stdout.write("Waiting for 1 second\n")
                sys.stdout.flush()
                time.sleep(1)

                since_wait = 0
            since_wait += 1
            compound_id = result['compound_id']
            cid = result['cid']
            sys.stdout.write("Getting counts for CID: %s \n" % cid)
            sys.stdout.flush()
            response.append({
                'compound_id': compound_id,
                'assay_count': self.assay_count(cid),
                'pathway_count': self.pathway_count(cid)
            })

            # Progress
            perc = ((i+1)/count) * 100
            sys.stdout.write("%s%% \n" % perc)
            sys.stdout.flush()

        return response

    def save(self, data):
        query = "INSERT OR REPLACE INTO pubchem_counts(compound_id, id, assay_count, pathway_count)" \
                "VALUES (" \
                "COALESCE((SELECT compound_id from pubchem_counts WHERE compound_id = :compound_id), :compound_id), " \
                "(SELECT id from pubchem_counts WHERE compound_id = :compound_id)," \
                ":assay_count," \
                ":pathway_count" \
                ")"
        return query_db(query, data, many=True)
