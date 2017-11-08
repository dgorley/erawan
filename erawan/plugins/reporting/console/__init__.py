"""Console output reporting."""

import datetime
import texttable

def report(config, backup_file, verification_result, scrubbing_result):
    """Print a table of results."""
    table = texttable.Texttable()
    table.set_deco(table.VLINES)
    table.add_row(['Backup File', backup_file])
    table.add_row(['Report Timestamp', datetime.datetime.utcnow().isoformat()])
    for t in verification_result:
        table.add_row(['Test: {}'.format(t['test_name']), str(t['result'])])
    table.add_row(['Scrub Successful?', str(scrubbing_result['scrub_successful'])])
    result = table.draw()
    return result
