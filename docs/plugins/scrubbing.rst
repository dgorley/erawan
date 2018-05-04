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
