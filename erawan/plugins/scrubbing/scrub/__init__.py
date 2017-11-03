"""Use "scrub" to remove all files in the working folder."""

import glob
import logging
import os
import os.path
import shutil
import subprocess

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def scrub(config):
    """Scrub all files from disk."""
    try:
        objects = glob.glob(os.path.join(config['working_path'], '**'), recursive=True)[1:]
        objects.append(os.path.join(config['working_path'], '.password'))
        logger.info('Scrubbing files from working directory')
        for obj in objects:
            if os.path.isfile(obj):
                args = '{} -p {} {}'.format(
                    config['plugins']['scrubbing']['scrub_path'],
                    config['plugins']['scrubbing']['pattern'],
                    obj
                )
                logger.debug('Scrubbing %s', obj)
                subprocess.run(args, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                os.unlink(obj)
        tl_dirs = glob.glob(os.path.join(config['working_path'], '*'))
        for d in tl_dirs:
            logger.debug('Removing %s', d)
            shutil.rmtree(d)
        logger.info('Scrubbing complete')
        return {'scrub_successful': True}
    except:
        logger.warning('Something went wrong while scrubbing')
        return {'scrub_successful': False}
