"""PostgreSQL utility functions."""

import logging
import os
import os.path
import pathlib
import subprocess
import uuid

import magic

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def create_cluster(config):
    """Create a PostgreSQL cluster for verification.

    Once the cluster is initialized, access should be strictly controlled.
    The postgresql.conf and pg_hba.conf should be set, and a random
    password set for the postgres user.
    """
    cluster_path = os.path.join(config['working_path'], 'pgsql_cluster')
    initdb = os.path.join(config['postgresql']['bin_path'], 'initdb')

    password_file = os.path.join(config['working_path'], '.password')
    password = str(uuid.uuid4())
    pathlib.Path(password_file).touch(mode=0o600, exist_ok=False)
    with open(password_file, 'w') as pw_fh:
        pw_fh.write('{}\n'.format(password))

    args = '{} --auth-host=reject --auth-local=md5 --username=postgres --pwfile={} --pgdata={}'.format(
        initdb, password_file, cluster_path
    )
    subprocess.run(args, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    with open(password_file, 'w') as pw_fh:
        pw_fh.write('*:*:*:*:{}\n'.format(password))

    # Set the UNIX socket directory to be used.
    socket_path = os.path.join(config['working_path'], 'sockets')
    os.makedirs(socket_path, exist_ok=True)

    with open(os.path.join(cluster_path, 'postgresql.conf'), 'a') as conf:
        conf.write('# Custom settings.\n')
        conf.write("listen_addresses = ''\n")
        conf.write("unix_socket_directories = '{}'\n".format(socket_path))

def create_database(config):
    """Create a database on the new cluster for restoration."""
    socket_path = os.path.join(config['working_path'], 'sockets')
    os.environ['PGPASSFILE'] = os.path.join(config['working_path'], '.password')
    createdb = os.path.join(config['postgresql']['bin_path'], 'createdb')
    args = '{} --username=postgres -h {} erawan "Erawan verification database."'.format(
        createdb,
        socket_path
    )
    subprocess.run(args, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    del os.environ['PGPASSFILE']

def start(config):
    """Start the new DB cluster."""
    pg_ctl = os.path.join(config['postgresql']['bin_path'], 'pg_ctl')
    cluster_path = os.path.join(config['working_path'], 'pgsql_cluster')
    args = '{} -D {} -l {} start'.format(
        pg_ctl,
        cluster_path,
        os.path.join(cluster_path, 'postgresql.log')
    )
    subprocess.run(args, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def stop(config):
    """Stop the DB cluster."""
    pg_ctl = os.path.join(config['postgresql']['bin_path'], 'pg_ctl')
    cluster_path = os.path.join(config['working_path'], 'pgsql_cluster')
    args = '{} -D {} stop'.format(
        pg_ctl,
        cluster_path
    )
    subprocess.run(args, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def restore(config):
    """Restore a PostgreSQL backup.

    Attempt to determine whether the file is a plain dump (where psql should)
    be used), or a custom dump (requiring pg_restore).
    """
    socket_path = os.path.join(config['working_path'], 'sockets')
    backup = os.path.join(config['working_path'], 'decrypted_backup')
    # Test whether or not this is a binary file.
    if magic.from_file(backup).startswith('ASCII text'):
        restore_command = '{} --username=postgres --file={} --dbname=erawan --host={}'.format(
            os.path.join(config['postgresql']['bin_path'], 'psql'),
            backup,
            socket_path
        )
    else:
        restore_command = '{} --username=postgres --file={} --dbname=erawan ==host={}'.format(
            os.path.join(config['postgresql']['bin_path'], 'pg_restore'),
            backup,
            socket_path
        )
    os.environ['PGPASSFILE'] = os.path.join(config['working_path'], '.password')
    subprocess.run(restore_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    del os.environ['PGPASSFILE']
