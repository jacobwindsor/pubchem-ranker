from .BasePubChemCounter import BasePubChemCounter


class PubChemAssayCounter (BasePubChemCounter):
    @property
    def table_name(self):
        return "pubchem_assay_counts"

    def counter(self, CID):
        return self.pubchem_counter(CID, "bioactivity")