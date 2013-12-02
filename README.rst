.. figure:: /doc/images/cryptobot-large.png
   :alt: CryptoBot

   CryptoBot
CryptoBot Email is an email bot that helps people learn how to use
OpenPGP. You send CryptoBot a PGP-encrypted and signed email (probably
using GnuPG) and it responds telling you how you do, and offering
advice.

Getting Started
---------------

Start by copying ``config_template.py`` into ``config.py`` and editing
it.

::

    $ cp config_template.py config.py

Set all of these settings:

-  ``PGP_NAME``: The name part of the user ID for for the bot's OpenPGP
   keypair
-  ``PGP_EMAIL``: The email part of the user ID for for the bot's
   OpenPGP keypair. This should be the email address that users are
   expected to email.
-  ``GPG_HOMEDIR``: The directory in which the bot's keyring will be
   stored (it will be created by the bot if it does not exist). This
   should be in a location that is writeable by the bot.
-  ``USE_MAILDIR``: You can either use a Maildir or IMAP; set to False
   to use IMAP
-  ``MAILDIR``: If you're using a Maildir, this is the path to it
-  ``IMAP_SERVER``: The IMAP server to connect to, e.g.
   ``imap.gmail.com``
-  ``IMAP_USERNAME``: The IMAP username
-  ``IMAP_PASSWORD``: The IMAP password
-  ``SMTP_SERVER``: The SMTP server to connect to, e.g.
   ``smtp.gmail.com``
-  ``SMTP_USERNAME``: The SMTP username
-  ``SMTP_PASSWORD``: The SMTP password

This is a Python project with some external dependencies. We recommend
using virtualenv:

::

    $ virtualenv env
    $ . env/bin/activate
    (env) $ pip install -r requirements.txt
    (env) $ ./bot.py
    # when you're done
    (env) $ deactivate

Dev Notes
---------

To run the tests:

::

    $ ./test.py

Relevant specs:

-  `RFC 4880 - OpenPGP Message
   Format <http://tools.ietf.org/html/rfc4880>`__
-  `RFC 2045 - Multipurpose Internet Mail Extensions
   (MIME) <http://tools.ietf.org/html/rfc2045>`__
-  `RFC 3156 - MIME Security with
   OpenPGP <http://tools.ietf.org/html/rfc3156>`__

