# VOC Project
This is an application built to aid the identification of an ~800 strong list of VOCs given for the 3000 level MSP project.
The application ranks VOCs by data gathered on PubChem in order to make identification easier.

##Web Page
Visit http://jacobwindsor.pythonanywhere.com to view an example of this application.

## Setup
1. Clone this repository
2. Make sure you have python3 installed
3. cd into the project directory and run `pip install -r requirements.txt`
4. Go to VOCRanker/__init__.py and fill in the "ADMIN_EMAIL" setting. Required for Pubchem
4. run `python manage.py initdb` to intitialize the database
5. run `python manage.py fillmetabs <path> <name>` where path is the absolute path to the CSV file containing the dataset
and name is the name you wish to call the dataset
6. run `python manage.py fillcounts` to fill the counts table. Takes a long time
7. run `python manage.py runserver` to run the server


Note: You may also run `python manage.py runall <path> <name> to run all of the commands to set up the application.
However, this will destroy  any data previously in the tables`

## Dataset format
Datasets must be in CSV format with each compound on one row. The CAS number takes the first position followed by the
IUPAC name in brackets. This data must be in the first column, anything in other columns will be ignored

    <CAS> (<IUPAC>)

## DUPLICATE DATA
One Duplicate CAS ID with different IUPAC names was found when inserting into database. Log of SQLite query:

    INSERT INTO metabolites(CAS, IUPAC) VALUES ('1072-43-1','methylthiirane ')
    INSERT INTO metabolites(CAS, IUPAC) VALUES ('1072-43-1','propylenesulfide ')
    
The `methyliirane` row was removed from the dataset to reslove the issue (row 168)
