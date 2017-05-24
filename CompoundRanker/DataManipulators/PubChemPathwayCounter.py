from .BasePubChemCounter import BasePubChemCounter


class PubChemPathwayCounter(BasePubChemCounter):
    @property
    def table_name(self):
        return "pubchem_pathway_counts"

    def counter(self, CID):
        return self.pubchem_counter(CID, "biosystem")