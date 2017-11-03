"""Retrieval plugin to fetch a single file."""

import logging
import os.path
import shutil
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def fetch(config):
    """Retrieve a single file, specified on the command line."""
    try:
        shutil.copy(config['filename'], config['working_path'])
        logger.info('Retrieved backup file %s', config['filename'])
    except:
        logger.critical('Unable to rerieve backup file %s', config['filename'])
        sys.exit(1)
    backup = os.path.join(config['working_path'], os.path.basename(config['filename']))
    yield backup
