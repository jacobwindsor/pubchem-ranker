import sqlite3
from flask import g

from CompoundRanker import app


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    if app.config['DATABASE_LOG']:
        rv.set_trace_callback(print)
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    db = get_db()
    with open(app.config['SCHEMA'], mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

def query_db(query, args=(), one=False, many=False):
    if many:
        cur = get_db().executemany(query, args)
    else:
        cur = get_db().execute(query, args)
    get_db().commit()
    rv = cur.fetchall() or cur.lastrowid # Returns the last row ID if inserted
    cur.close()
    return (rv[0] if rv else None) if one else rv