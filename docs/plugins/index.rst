Erawan Plugins
==============

Erawan is designed for flexibility, utilizing plugins to perform it's key
functions.  These plugins are categorized below.

.. _plugins-retrieval:

Retrieval Plugins
-----------------

Retrieval plugins identify the backups to be fed to Erawan for verification.

singlefile
~~~~~~~~~~

The singlefile plugin processes a single PostgreSQL backup file, specified
on the command line with the ``-f`` flag.

Example::

    $ erawan -f mybackup.bak.enc


.. _plugins-decryption:

Decryption Plugins
------------------

Decryption plugins decrypt encrypted backups, so that they can be restored and
verified.

gnupg2
~~~~~~

The gnupg2 plugin uses GnuPG2 symmetric encryption to decrypt a backup.  To
prevent snooping of encryption keys, the key is not provided as a command line
argument; set the environment variable ``ERAWAN_DECRYPTION_KEY`` to the key
which should be used for decryption.

Parameters
''''''''''
  * ``gpg2_path``: The full path to the ``gpg2`` executable.
  * ``mode``: The type of encryption to use.  Only ``symmetric`` is currently
    supported.


.. _plugins-verification:

Verification Plugins
--------------------

Verification plugins provide the tests to confirm whether or not a backup is
"valid".  This could range from simply confirming that the database is
restorable to examining data in the restored database.

has_tables
~~~~~~~~~~

The has_tables plugin simply tests that there is a non-zero number of tables
in the database's public schema.


.. _plugins-scrubbing:

Scrubbing Plugins
-----------------

Scrubbing plugins securely remove the retrieved backups, along with the
PostgreSQL cluster used for verification, from the filesystem.

scrub
~~~~~

The scrub plugin uses the ``scrub`` utility to securely remove the backup files
and PostgreSQL cluster from the filesystem.

Parameters
''''''''''
  * ``scrub_path``: The full path to the ``scrub`` executable.
  * ``pattern``: The type of scrubbing pattern to use.  For a list of available
    patterns, see ``man scrub``.


.. _plugins-reporting:

Reporting Plugins
-----------------

Reporting plugins provide the output from the verification process.

console
~~~~~~~

The console plugin prints a simple table with the verification and scrubbing
results to stdout.
