import core.soundcloud_parses as SCParser
from core.models import Message
from mock import patch, MagicMock
from django.test import TestCase


class SoundCloudParserTests(TestCase):
    def test_register(self):
        self.assertTrue(SCParser.is_register('register'))
        self.assertTrue(SCParser.is_register('REGISTER'))
        self.assertTrue(SCParser.is_register(' REGISTER  \n'))

    def test_bad_register(self):
        self.assertFalse(SCParser.is_register(''))
        self.assertFalse(SCParser.is_register('regme'))
        self.assertFalse(SCParser.is_register('\n'))

    def test_balance(self):
        self.assertTrue(SCParser.is_get_balance('balance'))
        self.assertTrue(SCParser.is_get_balance('BALANCE'))
        self.assertTrue(SCParser.is_get_balance('  BALance  \n\n'))

    def test_get_balance(self):
        self.assertTrue(SCParser.is_get_balance('get balance'))
        self.assertTrue(SCParser.is_get_balance('getbalance'))
        self.assertTrue(SCParser.is_get_balance('GET BALANCE \n'))

    def test_bad_get_balance(self):
        self.assertFalse(SCParser.is_get_balance('gtbalancec'))
        self.assertFalse(SCParser.is_get_balance('balaance'))
        self.assertFalse(SCParser.is_get_balance('hey balance hey'))

    def test_is_tip(self):
        self.assertTrue(SCParser.is_tip('tip user 100.5'))
        self.assertTrue(SCParser.is_tip('tip user 100'))

    def test_bad_tip(self):
        self.assertFalse(SCParser.is_tip('top user 10'))
        self.assertFalse(SCParser.is_tip('tip a user 10'))
        self.assertFalse(SCParser.is_tip('tip  user 100'))
        self.assertFalse(SCParser.is_tip('tip user 100f'))

    def test_parse_tip(self):
        user, amt = SCParser.parse_tip('tip user 10.50')
        self.assertEqual(user, 'user')
        self.assertEqual(amt, '10.50')

    def test_parse_mention_tip(self):
        amt = SCParser.parse_mention_tip('@dogebot tip 100')
        self.assertEqual(amt, '100')
        amt = SCParser.parse_mention_tip('@dogebot tip 10.50')
        self.assertEqual(amt, '10.50')
