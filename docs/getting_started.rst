Getting Started with Erawan
===========================

Impatient? Try this...
----------------------
::
    
    $ sudo apt install postgresql python python3 gnupg2
    $ git clone https://github.com/dgorley/erawan.git
    $ python3 -m venv erawan.venv
    $ source erawan.venv/bin/activate
    $ cd erawan
    $ pip install -r requirements.txt
    $ pip install .
    $ vim config.yml  # Set postgresql.bin_path
    $ ERAWAN_DECRYPTION_KEY=1234 erawan -f sample/provinces.sql.asc

Prerequisites
-------------

In order to run Erawan, at a minimum you'll need the following:

  * Python 3.5+
  * PostgreSQL 9.x or 10
  * GnuPG 2 (for the sample database)

Installing Erawan
-----------------

In order to install Erawan, you'll first need to download or clone the git repo.
The easiest way to do this is as follows::

    $ git clone https://github.com/dgorley/erawan.git

Next, if you're going to run Erawan in a virtualenv, create that now.
**This is strongly encouraged, but not mandatory**, so use your judgement.
::

    $ python3 -m venv erawan.venv

Now, load the virtualenv, and install the project requirements::

    $ source erawan.venv/bin/activate
    $ pip install -r requirements.txt

Finally, from the cloned repository, use ``pip`` to install Erawan itself.
::

    $ pip install .

This will create an entry point named ``erawan`` which will be accessible
in your path.
::

    $ erawan --help


Configuring Erawan
------------------

A basic Erawan configuration file (``config.yml``) looks like this:

.. code-block:: yaml
   :caption: config.yml
   :name: config-yml

    # Erawan Configuration File
    ---
    plugins:
        retrieval:
            name: singlefile
        decryption:
            name: gnupg2
            gpg2_path: /usr/bin/gpg2
            mode: symmetric
        verification:
            name: has_tables
        scrubbing:
            name: scrub
            scrub_path: /usr/bin/scrub
            pattern: fillzero
        reporting:
            name: console

    working_path: /tmp/erawan

    postgresql:
        bin_path: /usr/lib/postgresql/9.6/bin

    # ========================================================================
    # Logging Settings
    # ----------------
    # These should remain mostly static; the only fields which you may choose
    # to change are the logging level, and the output format.
    # ========================================================================
    logging:
        # ---------------------------
        # Debug Level   Numeric value
        # ---------------------------
        # CRITICAL      50
        # ERROR         40
        # WARNING       30
        # INFO          20
        # DEBUG         10
        # ---------------------------
        level: &logging_level 30
        version: 1
        formatters:
            f:
                format: "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        handlers:
            h:
                class: logging.StreamHandler
                formatter: f
                level: *logging_level
        root:
            handlers: h
            level: *logging_level

Plugins
~~~~~~~
Erawan uses five different types of plugins to direct its behaviour.  They are:

Retrieval Plugins
    These identify the backups to be fed to Erawan for verification.

Decryption Plugins
    These decrypt encrypted backups.

Verification Plugins
    These provide the tests to confirm whether or not a backup is "valid".

Scrubbing Plugins
    These securely remove the retrieved backups, along with the PostgreSQL
    cluster used for verification, from the filesystem.

Reporting Plugins
    These provide the output from the verification process.

Working Path
~~~~~~~~~~~~

The *working path* is a location in the filesystem that Erawan will use for
all of its verification work.  When a backup file is retrieved, it will be
written to this directory, then decrypted there.  The PostgreSQL cluster used
for restoring and verifying the database will also be located here.  For this
reason, it is recommended that:

  * This directory is mounted on an encrypted volume;
  * An OS-level user is created specifically for running Erawan; and
  * The working directory is owned by, and restricted to, the Erawan user.

PostgreSQL
~~~~~~~~~~

Erawan uses the PostgreSQL command-line utilities to perform a number of
functions during the verification process.  To do this, it needs the location
PostgreSQL's ``bin/`` folder.

Logging
~~~~~~~

Erawan uses's Python's ``logging`` module to log events during it's operation.
The configuration for this is stored in the ``config.yml`` file.  Under normal
circumstances, the default settings here should suffice.  If you wish to change
settings, refer to the `documentation for the logging module
<https://docs.python.org/3/library/logging.html>`_.

Running Erawan
--------------

Erawan should work out-of-the-box, provided the prerequisites are installed
and the working path and PostgreSQL bin path are set correctly.  Erawan
ships with a small, encrypted, sample database which can be used to smoke
test the installation.
::

    $ ERAWAN_DECRYPTION_KEY=1234 erawan -f sample/provinces.sql.asc
    Backup File       | sample/provinces.sql.asc
    Report Timestamp  | 2017-11-03T22:25:16.762390
    Test: has_tables  | True
    Scrub Successful? | True
