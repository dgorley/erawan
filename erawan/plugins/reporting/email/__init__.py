"""Email output reporting."""

import email.message
import smtplib
from erawan.plugins.reporting.console import generate_report_table


def report(config, backup_file, verification_result, scrubbing_result):
    """Generate a table of results, and send it via email."""
    report_body = generate_report_table(
        backup_file, verification_result, scrubbing_result
    )
    email_message = email.message.EmailMessage()
    email_message.set_content(report_body)
    email_message["Subject"] = config["plugins"]["reporting"]["subject"]
    email_message["From"] = config["plugins"]["reporting"]["from"]
    email_message["To"] = config["plugins"]["reporting"]["to"]
    smtp_server = smtplib.SMTP(config["plugins"]["reporting"]["smtp_server"])
    smtp_server.send_message(email_message)
    smtp_server.quit()
    return report_body
