"""Driver module for Erawan Backup Verification."""

import argparse
import importlib
import logging
from logging.config import dictConfig
import os
import os.path
import sys
import time

import yaml

import erawan.postgresql

logger = None

def read_command_line(args):
    """Parse arguments supplied on the command line."""
    parser = argparse.ArgumentParser(description="PostgreSQL backup verification")
    parser.add_argument('-C', '--config', default=None, help='Config file (default config.yml in working dir)')
    parser.add_argument('-f', '--filename', help="Backup filename (for singlefile mode)")
    parser.add_argument('-q', '--quiet', action='store_true', help="Quiet mode (don't print results to stdout)")
    return parser.parse_args(args)

def read_config_file(config_file=None):
    """Read the contents of the configuration file."""
    if config_file is None:
        config_file = os.path.join(os.getcwd(), 'config.yml')
    try:
        config = yaml.load(open(config_file, 'r'))
    except FileNotFoundError:
        config = {}
    return config

def merge_configs(cmdline, config):
    """Merge the command line and config parameters."""
    cmdline = vars(cmdline)
    for key in cmdline:
        if cmdline[key] is not None:
            config[key] = cmdline[key]
    return config

def load_plugins(config):
    """Import the plugins required by the application."""
    plugin = {}
    for p in ('retrieval', 'decryption', 'verification', 'scrubbing', 'reporting'):
        try:
            module_name = 'erawan.plugins.{}.{}'.format(p, config['plugins'][p]['name'])
        except KeyError:
            logger.critical('Could not import %s plugin; is it set in config?', p)
            sys.exit(1)
        try:
            plugin[p] = importlib.import_module(module_name)
        except ImportError:
            logger.critical('Unable to load plugin "%s"', module_name)
            sys.exit(1)
    return plugin

def process_backup(config, backup_file):
    """Processing of PostgreSQL backups."""
    plugin = config['plugin_obj']
    plugin['decryption'].decrypt(config, backup_file)
    erawan.postgresql.create_cluster(config)
    time.sleep(2)
    erawan.postgresql.start(config)
    time.sleep(2)
    erawan.postgresql.create_database(config)
    erawan.postgresql.restore(config)
    verification_result = plugin['verification'].verify(config)
    erawan.postgresql.stop(config)
    scrubbing_result = plugin['scrubbing'].scrub(config)
    return plugin['reporting'].report(config, verification_result, scrubbing_result)

def main(args=None):
    """The main routine."""
    # Process configuration.
    if args is None:
        args = sys.argv[1:]
    clargs = read_command_line(args=args)
    config_file = read_config_file(clargs.config)
    config = merge_configs(clargs, config_file)

    # Initiate logging
    dictConfig(config['logging'])
    global logger
    logger = logging.getLogger()
    logger.debug('Configuration: %s', config)

    logger.info('Loading plugins')
    plugin = load_plugins(config)
    config['plugin_obj'] = plugin

    # Create the working directory (if it doesn't exist.)
    os.makedirs(config['working_path'], exist_ok=True)

    # Backup processing loop
    result_set = []
    for backup_file in plugin['retrieval'].fetch(config):
        result = process_backup(config, backup_file)
        if not config['quiet']:
            print(result)
        result_set.append(result)
    return result_set

def entrypoint_main(args=None):
    main(args)
    return

if __name__ == "__main__":
    main(sys.argv[1:])
