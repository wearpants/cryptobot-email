#!/usr/bin/env python

import os
import unittest
import cryptobot_email
import email
import random

class GnuPGTest(unittest.TestCase):
    def setUp(self):
        # test keys
        self.public_key = open('test-data/keys/public.key').read()
        self.private_key = open('test-data/keys/private.key').read()
        # set up test keyring
        self.gpg = cryptobot_email.GnuPG("test-data/homedir")
        self.gpg.import_keys(self.public_key)
        self.gpg.import_keys(self.private_key)
        # load configuration
        cryptobot_email.load_config('test/cryptobot.ini')

    def tearDown(self):
        pass

    def test_export_keys_valid(self):
        pubkey = self.gpg.export_keys('0D4AF6E8D289BDE46594D41255BB44BA0D3E5387')
        self.assertEqual(pubkey, self.public_key)

    def test_export_keys_invalid(self):
        pubkey = self.gpg.export_keys('0000000000000000000000000000000000000000')
        self.assertFalse(pubkey)

    def test_import_keys_valid(self):
        rms_pubkey = open('test-data/keys/rms.asc').read()
        fingerprint = self.gpg.import_keys(rms_pubkey)
        self.assertTrue(fingerprint)
        self.assertEqual(fingerprint.upper(), '6F818B215E159EF3FA26B0BE624DC565135EA668')

    def test_import_keys_invalid(self):
        fingerprint = self.gpg.import_keys('fail')
        self.assertFalse(fingerprint)

    def test_decrypt_valid(self):
        ciphertext = open('test-data/keys/test_decrypt_valid.asc').read()
        plaintext, signed = self.gpg.decrypt(ciphertext)
        self.assertEqual(plaintext, 'This is a test message.\n')

    def test_decrypt_invalid(self):
        ciphertext = open('test-data/keys/test_decrypt_invalid.asc').read()
        plaintext, signed = self.gpg.decrypt(ciphertext)
        self.assertFalse(plaintext)

    def test_encrypt(self):
        ciphertext = self.gpg.encrypt('test', '0D4AF6E8D289BDE46594D41255BB44BA0D3E5387')
        self.assertFalse(ciphertext == False)
        self.assertTrue(cryptobot_email.PGP_ARMOR_HEADER_MESSAGE in ciphertext)

    def test_sign(self):
        sig = self.gpg.sign('test')
        self.assertTrue(cryptobot_email.PGP_ARMOR_HEADER_SIGNATURE in sig)

    def test_has_secret_key_with_uid(self):
        self.assertEqual('0D4AF6E8D289BDE46594D41255BB44BA0D3E5387', self.gpg.has_secret_key_with_uid('OpenPGPBot Test Suite (insecure) <invalid_and_insecure@openpgpbot.eff.org>'))
        self.assertEqual('0D4AF6E8D289BDE46594D41255BB44BA0D3E5387', self.gpg.has_secret_key_with_uid('invalid_and_insecure@openpgpbot.eff.org'))
        self.assertFalse(self.gpg.has_secret_key_with_uid('fluff'))

    def test_has_public_key_with_uid(self):
        expected_uid = 'OpenPGPBot Test Suite (insecure) <invalid_and_insecure@openpgpbot.eff.org>'
        self.assertTrue(self.gpg.has_public_key_with_uid('0D4AF6E8D289BDE46594D41255BB44BA0D3E5387', expected_uid))
        self.assertFalse(self.gpg.has_public_key_with_uid('0D4AF6E8D289BDE46594D41255BB44BA0D3E5387', 'fluff'))

    def test_gen_key(self):
        random.seed()
        r = random.random()
        name = 'Test '+str(r)
        expected_uid = name+' <test@example.com>'
        fingerprint = self.gpg.gen_key(name, 'test@example.com', 1024)
        self.assertTrue(self.gpg.has_secret_key_with_uid(expected_uid))

class BotTest(unittest.TestCase):

    def setUp(self):
        # test keys
        self.public_key = open('test-data/keys/public.key').read()
        self.private_key = open('test-data/keys/private.key').read()
        # set up test keyring
        self.gpg = cryptobot_email.GnuPG("test-data/homedir")
        self.gpg.import_keys(self.public_key)
        self.gpg.import_keys(self.private_key)

        # set up tester
        self.emails = {}
        for filename in os.listdir('test-data/emails/'):
            self.emails[filename] = email.message_from_string(open('test-data/emails/'+filename).read())

    def tearDown(self):
        pass

    def test_unencrypted(self):
        msg = cryptobot_email.OpenPGPMessage(self.emails['unencrypted_thunderbird'],
                                 gpg=self.gpg)
        self.assertFalse(msg.encrypted_right)
        self.assertFalse(msg.encrypted_wrong)

    def test_signed(self):
        msg = cryptobot_email.OpenPGPMessage(self.emails['signed'],
                                 gpg=self.gpg)
        self.assertTrue(msg.signed)

    def test_unsigned(self):
        # todo finish
        pass

    def test_encrypted_correct_key(self):
        result_text = "encrypted text"
        msg = cryptobot_email.OpenPGPMessage(self.emails['encrypted_correctly'],
                                 gpg=self.gpg)
        self.assertTrue(msg.encrypted_right)
        self.assertFalse(msg.encrypted_wrong)
        self.assertEquals(result_text, msg.decrypted_text.split("quoted-printable")[1].strip())

    def test_encrypted_wrong_key(self):
        msg = cryptobot_email.OpenPGPMessage(self.emails['encrypted_to_wrong_key'],
                                 gpg=self.gpg)
        self.assertFalse(msg.encrypted_right)
        self.assertTrue(msg.encrypted_wrong)

    def test_encrypted_and_signed_pgp_mime(self):
        result_text = "this message is encrypted and signed and uses pgp/mime"
        msg = cryptobot_email.OpenPGPMessage(self.emails['encrypted_signed_pgp_mime'], gpg=self.gpg)
        self.assertTrue(msg.encrypted_right)
        self.assertFalse(msg.encrypted_wrong)
        self.assertTrue(msg.decrypted_text.find(result_text) > 0)
        self.assertTrue(msg.signed)

    def test_pubkey_included_attached_text_plain(self):
        msg = cryptobot_email.OpenPGPMessage(self.emails['pubkey_attached_text-plain'], gpg=self.gpg)
        self.assertTrue(msg.pubkey_included)

    def test_pubkey_included_attached_application_pgpkeys(self):
        msg = cryptobot_email.OpenPGPMessage(self.emails['pubkey_attached_application-pgpkeys'], gpg=self.gpg)
        self.assertTrue(msg.pubkey_included)

    def test_pubkey_included_inline(self):
        msg = cryptobot_email.OpenPGPMessage(self.emails['pubkey_inline'], gpg=self.gpg)
        self.assertTrue(msg.pubkey_included)

    def test_encrypted_pubkey_included_attached_text_plain(self):
        msg = cryptobot_email.OpenPGPMessage(self.emails['encrypted_pubkey_attached_text-plain'], gpg=self.gpg)
        self.assertTrue(msg.encrypted_right)
        self.assertTrue(msg.pubkey_included)

    def test_encrypted_pubkey_included_attached_application_pgpkeys(self):
        msg = cryptobot_email.OpenPGPMessage(self.emails['encrypted_pubkey_attached_application-pgpkeys'], gpg=self.gpg)
        self.assertTrue(msg.encrypted_right)
        self.assertTrue(msg.pubkey_included)

    def test_encrypted_pubkey_included_inline(self):
        msg = cryptobot_email.OpenPGPMessage(self.emails['encrypted_pubkey_inline'], gpg=self.gpg)
        self.assertTrue(msg.encrypted_right)
        self.assertTrue(msg.pubkey_included)

if __name__ == '__main__':
    unittest.main()
