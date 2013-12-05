.. figure:: /doc/images/cryptobot-large.png
   :alt: CryptoBot

   CryptoBot
CryptoBot Email is an email bot that helps people learn how to use
OpenPGP. You send CryptoBot a PGP-encrypted and signed email (probably
using GnuPG) and it responds telling you how you do, and offering
advice.

Quickstart
-----------

This is a Python project ; you can install it with `pip <http://www.pip-installer.org/en/latest/>`__:

::

   $ # get source & install
   $ git clone https://github.com/wearpants/cryptobot-email
   $ mkvirtualenv cryptobot-email # if you use virtualenv(wrapper)
   $ pip install ./cryptobot-email/

   $ # run some tests
   $ make -B -C cryptobot-email/ test

   $ # you now have a shell command, congratulations
   $ cryptobot-email --config <your_config.ini>


Relevant specs
--------------
-  `RFC 4880 - OpenPGP Message
   Format <http://tools.ietf.org/html/rfc4880>`__
-  `RFC 2045 - Multipurpose Internet Mail Extensions
   (MIME) <http://tools.ietf.org/html/rfc2045>`__
-  `RFC 3156 - MIME Security with
   OpenPGP <http://tools.ietf.org/html/rfc3156>`__

