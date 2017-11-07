"""retrieval.singlefile tests for Erawan."""

import os
from erawan.__main__ import main

def test_singlefile_backup():
    os.environ['ERAWAN_DECRYPTION_KEY'] = '1234'
    result = main(['-q', '-f', 'sample/provinces.sql.asc'])[0].split('\n')
    del os.environ['ERAWAN_DECRYPTION_KEY']
    assert 'Backup File' in result[0]
    assert 'True' in result[2]
    assert 'True' in result[3]

def test_singlefile_extravars():
    os.environ['ERAWAN_DECRYPTION_KEY'] = '1234'
    result = main(['-q', '-e', '{"filename": "sample/provinces.sql.asc"}'])[0].split('\n')
    del os.environ['ERAWAN_DECRYPTION_KEY']
    assert 'Backup File' in result[0]
    assert 'True' in result[2]
    assert 'True' in result[3]
