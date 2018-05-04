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
