from requests import get, exceptions
from .BaseCounter import BaseCounter
import sys

class BasePubChemCounter (BaseCounter):
    def pubchem_counter(self, cid, collection):
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