import core.soundcloud_parses as SCParser
from core.models import Message
from mock import patch, MagicMock
from django.test import TestCase
from decimal import Decimal


class SoundCloudParserTests(TestCase):
    def test_register(self):
        self.assertTrue(SCParser.is_register('register'))
        self.assertTrue(SCParser.is_register('REGISTER'))
        self.assertTrue(SCParser.is_register(' REGISTER  \n'))

    def test_bad_register(self):
        self.assertFalse(SCParser.is_register(''))
        self.assertFalse(SCParser.is_register('regme'))
        self.assertFalse(SCParser.is_register('\n'))

    def test_accept(self):
        self.assertTrue(SCParser.is_accept('accept'))
        self.assertTrue(SCParser.is_accept('ACCEPT'))
        self.assertTrue(SCParser.is_accept(' ACCEPT  \n'))

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

    def test_is_mention_tip(self):
        self.assertTrue(SCParser.is_mention_tip('@dogebot: tip 100'))
        self.assertTrue(SCParser.is_mention_tip('@dogebot tip 100'))
        self.assertTrue(SCParser.is_mention_tip('what a song, @dogebot tip 11'))
        self.assertTrue(SCParser.is_mention_tip('love it, @dogebot 50, great song'))

    def test_parse_mention_tip(self):
        amt = SCParser.parse_mention_tip('@dogebot tip 100')
        self.assertEqual(amt, Decimal('100'))
        amt = SCParser.parse_mention_tip('@dogebot tip 10.50')
        self.assertEqual(amt, Decimal('10.50'))
        amt = SCParser.parse_mention_tip('what a song, @dogebot tip 11')
        self.assertEqual(amt, Decimal('11'))
        amt = SCParser.parse_mention_tip('love it, @dogebot 50, great song')
        self.assertEqual(amt, Decimal('50'))

    def test_parse_mention_tip_with_colon(self):
        self.assertEqual(SCParser.parse_mention_tip('@dogebot: tip 100'), 100)

    def test_is_withdrawl(self):
        self.assertTrue(SCParser.is_withdrawl('withdrawl 100 nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))
        self.assertTrue(SCParser.is_withdrawl('withdrawal 100 to nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))
        self.assertTrue(SCParser.is_withdrawl('withdraw 100.5 nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))
        self.assertTrue(SCParser.is_withdrawl('withdrawl all nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))
        self.assertTrue(SCParser.is_withdrawl('withdrawal all to nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))
        self.assertTrue(SCParser.is_withdrawl('withdraw all nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))

    def test_bad_withdraw(self):
        self.assertFalse(SCParser.is_withdrawl('withdrawl 100. nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))
        self.assertFalse(SCParser.is_withdrawl('withdraw100 nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))
        self.assertFalse(SCParser.is_withdrawl('withdraw100 to nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))
        self.assertFalse(SCParser.is_withdrawl('withdraw 100 to '))

    def test_parse_withdrawl(self):
        self.assertEqual(SCParser.parse_withdrawl('withdrawl 100 nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'),
                         (100, 'nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))
        self.assertEqual(SCParser.parse_withdrawl('withdrawl 50.5 nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'),
                         (50.5, 'nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))
        self.assertEqual(SCParser.parse_withdrawl('withdraw all nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'),
                         ('all', 'nq5DWtga2zdK78s1Y1SQFyVmJqKJqZrEwy'))

    def test_parse_help(self):
        self.assertTrue(SCParser.is_help(' help '))
        self.assertTrue(SCParser.is_help(' help \n'))
        self.assertTrue(SCParser.is_help('help'))

    def test_bad_help(self):
        self.assertFalse(SCParser.is_help('helpme'))
        self.assertFalse(SCParser.is_help('list help'))
