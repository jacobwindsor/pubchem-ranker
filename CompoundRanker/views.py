from flask import render_template, request

from CompoundRanker import app
from .database import query_db


@app.route('/', defaults={'page': 1})
@app.route('/rank/pubchem_pathways/', defaults={'page': 1})
@app.route('/rank/pubchem_pathways/page/<int:page>')
def index(page):
    limit = 15
    offset = (page-1)*limit
    datasets_query = "SELECT name from datasets"
    datasets_objects = query_db(datasets_query)
    datasets = []
    # TODO: This is really inefficient. Find a way to just return a list straight from the query
    for dataset in datasets_objects:
        datasets.append(dataset['name'])


    if request.args.get('dataset'):
        query_dataset = "SELECT id from datasets WHERE name = ? "
        dataset_id = str(query_db(query_dataset, [request.args.get('dataset')])[0]['id'])
        cur_dataset = request.args.get('dataset')
    else:
        query_dataset =  "SELECT id from datasets LIMIT 1"
        dataset_id = str(query_db(query_dataset)[0]['id'])
        cur_dataset = query_db("SELECT name from datasets WHERE id = ?", dataset_id)[0]['name']


    query = "SELECT id, IUPAC, CAS, max_count, " \
            "GROUP_CONCAT(concat) AS CID_counts " \
            "from (" \
                "SELECT t1.id, t1.IUPAC, t1.CAS, " \
                "t2.CID || '#' || t3.count AS concat, " \
                "t3.count as max_count " \
                "FROM metabolites t1 " \
                "LEFT JOIN pubchem_compounds t2 ON t2.metab_ID = t1.id " \
                "LEFT JOIN pubchem_pathway_counts t3 on t3.compound_id = t2.id " \
                "WHERE t1.dataset_id = {dataset_id}" \
            ") " \
            "GROUP BY id ORDER BY max_count DESC LIMIT {limit} OFFSET {offset}".\
        format(limit=limit, offset=offset, dataset_id=dataset_id)
    context = query_db(query)
    return render_template('list.html', rankedBy='PubChem Pathways', rankedCompounds=context, datasets=datasets,
                           cur_dataset=cur_dataset, page=page, next=(page+1), prev=(page-1))


