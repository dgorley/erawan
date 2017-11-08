"""retrieval.poll_directory tests for Erawan."""

import multiprocessing
import os
import shutil
import time
from erawan.__main__ import main

def test_directory_polling():
    os.environ['ERAWAN_DECRYPTION_KEY'] = '1234'
    os.makedirs('/tmp/erawan_backups', exist_ok=True)
    main_args = ['-q', '-e', '{"plugins": {"retrieval": {"name": "poll_directory", "backup_path": "/tmp/erawan_backups", "stop_file": "erawan_stop"}}}']
    queue = multiprocessing.SimpleQueue()
    p = multiprocessing.Process(target=main, kwargs={'args': main_args, 'result_queue': queue})
    p.start()
    time.sleep(2)
    # Copy two backup files to the polling dir, then the kill file.
    shutil.copyfile('sample/provinces.sql.asc', '/tmp/erawan_backups/provinces_1.sql.asc')
    shutil.copyfile('sample/provinces.sql.asc', '/tmp/erawan_backups/provinces_2.sql.asc')
    with open('/tmp/erawan_backups/erawan_stop', 'w') as fh:
        fh.write('')
    p.join()
    del os.environ['ERAWAN_DECRYPTION_KEY']

    assert not queue.empty()

    res_1 = queue.get().split('\n')
    assert 'Backup File' in res_1[0]
    assert 'provinces_1.sql.asc' in res_1[0]
    assert 'True' in res_1[2]
    assert 'True' in res_1[3]

    res_2 = queue.get().split('\n')
    assert 'Backup File' in res_2[0]
    assert 'provinces_2.sql.asc' in res_2[0]
    assert 'True' in res_2[2]
    assert 'True' in res_2[3]
