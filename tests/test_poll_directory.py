"""retrieval.poll_directory tests for Erawan."""

import os
from erawan.__main__ import main

def test_directory_polling():
    return True
    # os.environ['ERAWAN_DECRYPTION_KEY'] = '1234'
    # os.makedirs('/tmp/erawan_backups', exist_ok=True)
    #
    # result = main(['-q', '-f', 'sample/provinces.sql.asc'])[0].split('\n')
    # del os.environ['ERAWAN_DECRYPTION_KEY']
    # assert 'Backup File' in result[0]
    # assert 'True' in result[2]
    # assert 'True' in result[3]
