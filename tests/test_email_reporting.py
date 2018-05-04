"""reporting.email tests for Erawan."""

import email.message
import os
from unittest.mock import patch
from erawan.__main__ import main


def test_email_reporting_without_auth():
    os.environ["ERAWAN_DECRYPTION_KEY"] = "1234"
    main_args = [
        "-q",
        "-f",
        "sample/provinces.sql.asc",
        "-e",
        '{"plugins": {"reporting": {"name": "email", "smtp_server": "smtp.example.com", "subject": "Erawan Backup Verification Report", "from": "erawan@example.com", "to": "dba@example.com"}}}',
    ]
    with patch("smtplib.SMTP") as mock:
        main(main_args)[0].split("\n")
        init_args, send_args, _ = [n[1] for n in mock.mock_calls]

    del os.environ["ERAWAN_DECRYPTION_KEY"]

    assert init_args[0] == "smtp.example.com"
    assert type(send_args[0]) is email.message.EmailMessage
    assert send_args[0]["Subject"] == "Erawan Backup Verification Report"
    assert send_args[0]["To"] == "dba@example.com"
    assert send_args[0]["From"] == "erawan@example.com"
