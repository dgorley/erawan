Retrieval Plugins
-----------------

Retrieval plugins identify the backups to be fed to Erawan for verification.

singlefile
~~~~~~~~~~

The singlefile plugin processes a single PostgreSQL backup file, specified
on the command line with the ``-f`` flag.

Example::

    $ erawan -f mybackup.bak.enc

poll_directory
~~~~~~~~~~~~~~

The poll_directory plugin uses ``inotify`` to monitor a directory for changes.
When a file is *closed* in that directory (indicating file creation or edit is
complete), the file is processed as a backup file.  The monitoring can be
terminated by creating a "stop file" in the folder, with a specified name.
All files, including the stop file, will be processed in the order in which
they were closed, meaning that backup files closed prior to the stop file will
still be processed.

Parameters
''''''''''
  * ``backup_path``: The full path to the directory which should be monitored
    for new backup files.
  * ``stop_file``: The name of a file which, when placed in the backup path,
    will act a a signal to Erawan to stop backup processing and exit.
