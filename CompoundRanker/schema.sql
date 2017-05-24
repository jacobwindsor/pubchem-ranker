drop table if exists metabolites;
create table metabolites (
  id integer primary key AUTOINCREMENT,
  CAS string NOT NULL UNIQUE ,
  IUPAC text not null,
  dataset_id integer NOT NULL,
  FOREIGN KEY(dataset_id) REFERENCES datasets(id)
);

drop table if exists pubchem_compounds;
create table pubchem_compounds (
--   Can't use the CID as the primary key because of some compounds listed as stereisomers and other not
--   While CAS numbers differ for stereoisomers of the same compound, Some CIDs do not.
  id integer PRIMARY KEY AUTOINCREMENT,
  metab_ID integer NOT NULL,
  CID integer NOT NULL,
  FOREIGN KEY(metab_ID) REFERENCES metabolites(ID)
);

drop table if exists pubchem_pathway_counts;
CREATE TABLE pubchem_pathway_counts (
  id integer PRIMARY KEY AUTOINCREMENT,
  count integer DEFAULT 0 NOT NULL,
  compound_id integer UNIQUE NOT NULL,
  FOREIGN KEY(compound_id) REFERENCES pubchem_compounds(id)
);

drop table if exists pubchem_assay_counts;
CREATE TABLE pubchem_assay_counts (
  id integer PRIMARY KEY AUTOINCREMENT,
  count integer DEFAULT 0 NOT NULL,
  compound_id integer UNIQUE NOT NULL,
  FOREIGN KEY(compound_id) REFERENCES pubchem_compounds(id)
);

DROP TABLE IF EXISTS datasets;
CREATE TABLE datasets (
  id integer PRIMARY KEY AUTOINCREMENT,
  name string NOT NULL UNIQUE
);