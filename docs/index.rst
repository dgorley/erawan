.. image:: images/erawan_logo.png

Erawan: Automated Backup Verification for PostgreSQL
====================================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   plugins/index


What Is Erawan?
---------------

Erawan is an tool to give you confidence in the PostgreSQL backups you've
been ever-so-diligently creating and archiving.  It does this by retrieving,
decrypting, restoring, and testing your database backups, then scrubbing the
restored data and reporting the results back to you.


Where Do I Find It?
-------------------
  * Looking for the code? https://github.com/dgorley/erawan
  * Logging an issue? https://github.com/dgorley/erawan/issues


How is it Licensed?
-------------------
Erawan is licensed under the `MIT License <https://github.com/dgorley/erawan/blob/master/LICENSE>`_.


What's with the Name?
---------------------
*Erawan* is the Thai name for *Airavata*, the three-headed elephant representing
the Hindu gods **Brahma** (the creator), **Vishnu** (the keeper), and **Mahesh**
(the destroyer).  The elephant represents PostgreSQL, and the three heads follow
the process Erawan applies to backups.

..
    Indices and tables
    ==================

    * :ref:`genindex`
    * :ref:`modindex`
    * :ref:`search`
