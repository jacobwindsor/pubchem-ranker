import sys
from flask_script import Manager
from CompoundRanker import app
from CompoundRanker.DataManipulators.CIDGatherer import CIDGatherer
from CompoundRanker.DataManipulators.PubChemAssayCounter import PubChemAssayCounter
from CompoundRanker.DataManipulators.PubChemPathwayCounter import PubChemPathwayCounter
from CompoundRanker.DataManipulators.DataGatherer import DataGatherer
from CompoundRanker.database import init_db, query_db

manager = Manager(app)


@manager.command
def initdb():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@manager.command
def fillmetabs(path, dataset):
    """
    Fill the metabolites table with data.
    """
    # Get the CAS with CIDs
    file = open(path, 'r')
    gatherer = DataGatherer(file)
    data = gatherer.harvest()

    # Insert
    gatherer.save(data, dataset)
    print("Saved")


@manager.command
def fillcids(dataset):
    """Gather the CIDs from PubChem for the metabolites and save to pubchem_compounds table"""
    query = "SELECT id FROM datasets WHERE name = ?"
    try:
        dataset_id = str(query_db(query, [dataset])[0]['id'])
    except TypeError:
        raise TypeError("No dataset with name '%s'" % dataset)

    gatherer = CIDGatherer()
    data = gatherer.harvest(dataset_id)
    gatherer.save(data)
    print("Saved!")

@manager.command
def fillcounts(dataset):
    """Run the counter (ranker) for the metabolites and save to database"""
    query = "SELECT id FROM datasets WHERE name = ?"
    try:
        dataset_id = str(query_db(query, [dataset])[0]['id'])
    except TypeError:
        raise TypeError("No dataset with name '%s'" % dataset)

    PubChemPathwayCounter().count(dataset_id).save()
    PubChemAssayCounter().count(dataset_id).save()
    print("Saved!")


if __name__ == "__main__":
    manager.run()
