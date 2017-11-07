"""Poll a directory, and every time a new file appears, return it."""

import inotify.adapters
import logging
import os.path
import shutil
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def fetch(config):
    """Watch the designated folder for changes."""
    i = inotify.adapters.Inotify()
    watch_dir = bytes(config['plugins']['retrieval']['backup_path'], 'utf8')
    i.add_watch(watch_dir)
    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                logger.debug("WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s WATCH-PATH=[%s] FILENAME=[%s]", header.wd, header.mask, header.cookie, header.len, type_names, watch_path.decode('utf-8'), filename.decode('utf-8'))
                if type_names == ['IN_CLOSE_WRITE']:
                    backup_path = os.path.join(watch_path.decode('utf-8'), filename.decode('utf-8'))
                    logger.info('Found new backup file %s', backup_path)
                    yield backup_path
    finally:
        i.remove_watch(watch_dir)
