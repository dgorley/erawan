"""reporting.slack tests for Erawan."""

import os
from unittest.mock import patch
from erawan.__main__ import main


def test_slack_reporting():
    os.environ["ERAWAN_DECRYPTION_KEY"] = "1234"
    main_args = [
        "-q",
        "-f",
        "sample/provinces.sql.asc",
        "-e",
        '{"plugins": {"reporting": {"name": "slack", "url": "https://hooks.slack.com/services/123123/ABCABC/123ABC", "channel": "test_channel", "username": "Erawan", "icon": ":+1:"}}}',
    ]
    with patch("requests.post") as mock:
        main(main_args)[0].split("\n")
        args, kwargs = mock.mock_calls[0][-2:]

    del os.environ["ERAWAN_DECRYPTION_KEY"]
    assert args[0] == "https://hooks.slack.com/services/123123/ABCABC/123ABC"
    assert kwargs["json"]["channel"] == "test_channel"
    assert kwargs["json"]["username"] == "Erawan"
    assert kwargs["json"]["icon_emoji"] == ":+1:"
