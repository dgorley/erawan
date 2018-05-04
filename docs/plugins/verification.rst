Verification Plugins
--------------------

Verification plugins provide the tests to confirm whether or not a backup is
"valid".  This could range from simply confirming that the database is
restorable to examining data in the restored database.

has_tables
~~~~~~~~~~

The has_tables plugin simply tests that there is a non-zero number of tables
in the database's public schema.
