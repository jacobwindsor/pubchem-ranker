import os
import sys
from flask import Flask, g

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({
    'DATABASE': os.path.join(app.root_path, 'database.db'),
    'DATABASE_LOG': False,
    'SCHEMA': os.path.join(app.root_path, 'schema.sql'),
    'ADMIN_EMAIL': ''
})

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

import CompoundRanker.views
