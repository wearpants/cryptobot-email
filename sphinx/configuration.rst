Configuration
=============

Cryptobot uses `INI-style
<http://docs.python.org/2/library/configparser.html>`__ configuration files.
By default, it looks for ``/etc/cryptobot.ini``, but a custom file may be
passed on command line using ``--config``. The config file should have a section named ``cryptobot``, with the following recognized options:

GPG options
-----------

.. envvar:: PGP_NAME

human-readable name to use in ``From:`` of response emails

.. envvar:: PGP_EMAIL

email address for the bot itself

.. envvar:: GPG_HOMEDIR

Directory where the bot's GPG keyring is stored

Receiving options
-----------------

You can either use a maildir or an IMAP server (only SSL on the default port is supported).

.. envvar:: USE_MAILDIR

use a maildir for incoming emails. If false, use IMAP

.. envvar:: MAILDIR

path to maildir directory

.. envvar:: IMAP_SERVER

hostname of IMAP server

.. envvar:: IMAP_USERNAME

username of IMAP server

.. envvar:: IMAP_PASSWORD

password of IMAP server

Sending options
---------------

SMTP server (only SSL on the default port is supported)

.. envvar:: SMTP_SERVER

hostname of SMTP server

.. envvar:: SMTP_USERNAME

username of SMTP server

.. envvar:: SMTP_PASSWORD

password of SMTP server

Logging
-------
The config file may also contain sections for configuring `Python logging <http://docs.python.org/2/library/logging.config.html#configuration-file-format>`__.