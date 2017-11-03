"""Test that a restored database has at least one table in the public schema."""

import os

import psycopg2

def verify(config):
    """Check that the DB has at least one table in the public schema."""
    os.environ['PGPASSFILE'] = os.path.join(config['working_path'], '.password')
    conn = psycopg2.connect(
        host=os.path.join(config['working_path'], 'sockets'),
        user='postgres',
        dbname='erawan'
    )
    cur = conn.cursor()
    cur.execute("""
        SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';
    """)
    result = cur.fetchone()[0]
    conn.close()
    del os.environ['PGPASSFILE']
    return [
        {
            'test_name': 'has_tables',
            'result': bool(result > 0)
        }
    ]
