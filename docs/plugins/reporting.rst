Reporting Plugins
-----------------

Reporting plugins provide the output from the verification process.

console
~~~~~~~

The console plugin prints a simple table with the verification and scrubbing
results to stdout.

email
~~~~~

The email plugin uses the same table output as the console plugin, but delivers
it via email.

Parameters
''''''''''
  * ``smtp_server``: The URL of the SMTP server used to deliver email.
  * ``username``: The username to connect to the SMTP server. (optional)
  * ``password``: The password to connect to the SMTP server. (optional)
  * ``subject``: The subject line of the email.
  * ``from``: The reported sender of the email.
  * ``to``: The recipient(s) of the email.

slack
~~~~~

The Slack plugin uses the same table output as the console plugin, but delivers
it via email.

Parameters
''''''''''
  * ``url``: Slack webhook URL
  * ``channel``: Slack channel in which to post
  * ``username``: User under which to post
  * ``icon``: Slack icon to use (bookended with colons)
