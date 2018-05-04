"""Slack output reporting."""

import requests
from erawan.plugins.reporting.console import generate_report_table


def report(config, backup_file, verification_result, scrubbing_result):
    """Report backup verification results via Slack.

    Required configuration settings:
      - url: Slack webhook URL
      - channel: Slack channel in which to post
      - username: User under which to post
      - icon: Slack icon to use (bookended with colons)
    """
    report_body = generate_report_table(
        backup_file, verification_result, scrubbing_result
    )
    payload = {
        "channel": config["plugins"]["reporting"]["channel"],
        "text": "```" + report_body + "```",
        "username": config["plugins"]["reporting"]["username"],
        "icon_emoji": config["plugins"]["reporting"]["icon"],
    }
    response = requests.post(config["plugins"]["reporting"]["url"], json=payload)
    response.raise_for_status()
    return report_body
