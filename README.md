# PubChem Ranker
This is a simple application built on top of Flask that allows for the ranking of compounds by the amount of BioAssays
and BioSystems found in PubChem. A web-based interface is provided for viewing the ranked compounds and some commands
for setting up and running the ranker.


## Setup
1. Clone this repository
2. Make sure you have python3 installed
3. cd into the project directory and run `pip install -r requirements.txt`
4. Go to `VOCRanker/__init__.py` and fill in the "ADMIN_EMAIL" setting. Required for Pubchem
4. run `python manage.py initdb` to intitialize the database
5. run `python manage.py fillmetabs <path> <name>` where path is the absolute path to the CSV file containing the dataset
and name is the name you wish to call the dataset
6. run `python manage.py fillcounts <name>` to fill the counts table where name is the name of the dataset you wish to count. Takes a long time
7. run `python manage.py runserver` to run the server

## Dataset format
Datasets must be in CSV format with each compound on one row. The CAS number takes the first position followed by the
IUPAC name in brackets. This data must be in the first column, anything in other columns will be ignored

    <CAS> (<IUPAC>)
