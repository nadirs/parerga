import os
import time
import sqlite3
from flask import g
from config import *

def init_db():
    dest = os.path.join(PARERGA_STATIC_DIR, 'parerga.db')
    creation_script = "sqlite3 {} < schema.sql".format(dest)
    os.system(creation_script)

def connect_db():
    return sqlite3.connect(PARERGA_DB)

def before_request():
    g.db = connect_db()

def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def do_query(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def add_entry(path):
    full_path = os.path.abspath(path)
    fname = os.path.basename(path)
    if os.path.dirname(full_path) != PARERGA_ENTRY_DIR:
        if fname:
            newpath = os.path.join(PARERGA_ENTRY_DIR, fname)
            os.system('cp {} {}'.format(path, newpath))
        else:
            print("File name is missing or invalid. Please check the file path.")
            sys.exit(-1);
    date_added = time.time()
    query = 'INSERT INTO entries(path, date_added) VALUES(?, ?)'
    with connect_db() as temp_db:
        result = temp_db.execute(query, (fname, date_added))
    return result.lastrowid

def get_entry_field(entry_id, fieldname):
    assert isinstance(entry_id, int)
    query = 'SELECT {field} FROM entries ORDER BY :id LIMIT :id,1'.format(field=fieldname)
    query_args = {'id': entry_id}
    entry = do_query(query, args=query_args, one=True)
    field = entry[fieldname] if entry else None
    return field

def get_entry_date(entry_id):
    date_ticks = get_entry_field(entry_id, 'date_added')
    date = time.gmtime(date_ticks)
    return date

def get_entry_path(entry_id):
    filename = get_entry_field(entry_id, 'path')
    return os.path.join(PARERGA_ENTRY_DIR, filename)

def get_all_entry_ids():
    query = 'SELECT COUNT(id) as id_num FROM entries'
    result = do_query(query, one=True)
    return range(int(result['id_num']))

'''def get_all_entry_ids():
    query = 'SELECT id FROM entries ORDER BY id ASC'
    result = do_query(query)
    ids = [entry['id'] for entry in result]
    return ids
'''

def get_last_entry_id():
    query = 'SELECT MAX(id) AS last_id FROM entries'
    last_id = do_query(query, one=True)['last_id']
    return last_id

