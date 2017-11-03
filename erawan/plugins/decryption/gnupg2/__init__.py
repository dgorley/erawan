"""Erawan GnuPG2 Decryption Plugin"""

import logging
import os
import os.path
import subprocess
import sys

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def decrypt(config, enc_file):
    """Decrypt the encrypted backup using gpg2."""
    output_file = os.path.join(config['working_path'], 'decrypted_backup')
    args = '{} --batch --decrypt --passphrase {} --output {} {}'.format(
        config['plugins']['decryption']['gpg2_path'],
        os.environ['ERAWAN_DECRYPTION_KEY'],
        output_file,
        enc_file
    )
    try:
        subprocess.run(args, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info('%s successfully decrypted', enc_file)
    except subprocess.CalledProcessError:
        logger.critical('Unable to decrypt %s', enc_file)
        sys.exit(1)
    return output_file
