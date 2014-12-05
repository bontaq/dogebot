from core.soundcloud_api import SoundCloudAPI
from core.models import Conversation, Mention
from core.tests.fixture import (soundcloud_conversation_fixture, soundcloud_message_fixture,
                                soundcloud_mention_fixture)
from mock import patch, MagicMock
from django.test import TestCase


class SoundCloudTests(TestCase):
    def setUp(self):
        SoundCloudAPI.client = None

    @patch('core.soundcloud_api.soundcloud.Client')
    def test_get_mentions(self, mock_soundcloud):
        results = [
            {
                'collection': [soundcloud_mention_fixture[0]],
                'next_href': 'https://api.soundcloud.com/e1/me/activities.json?limi2t=1&cursor=41d51698-0e80-0000-68c4-d0a603b982a9'
            }, {
                'collection': [],
                'next_href': ''
            }
        ]
        m1 = MagicMock()
        m1.obj = results[0]
        m2 = MagicMock()
        m2.obj = results[1]
        mocks = [m1, m2]
        mock_soundcloud.return_value.get.side_effect = mocks
        soundcloud = SoundCloudAPI()
        res = [r for r in soundcloud.get_new_mentions()]
        self.assertEqual(len(res), 1)

    # @patch('core.soundcloud_api.soundcloud.Client')
    # def test_already_existing_mention(self, mock_soundcloud):
    #     pass

    @patch('core.soundcloud_api.soundcloud.Client')
    def test_create_mentions(self, mock_soundcloud):
        next_href = 'https://api.soundcloud.com/e1/me/activities.json?' + \
                    'limit=1&cursor=41d51698-0e80-0000-68c4-d0a603b982a9'
        results = [
            {
                'collection': [soundcloud_mention_fixture[0]],
                'next_href': next_href
            }, {
                'collection': [soundcloud_mention_fixture[1]],
                'next_href': next_href
            }, {
                'collection': [soundcloud_mention_fixture[2]],
                'next_href': next_href
            }
        ]
        m1 = MagicMock()
        m1.obj = results[0]
        m2 = MagicMock()
        m2.obj = results[1]
        m3 = MagicMock()
        m3.obj = results[2]
        mocks = [m1, m2, m3]
        mock_soundcloud.return_value.get.side_effect = mocks

        soundcloud = SoundCloudAPI()
        soundcloud.create_mentions()
        mentions = Mention.objects.all()
        self.assertEqual(len(mentions), 2)

        self.assertEqual(mentions[0].from_user_name, '666robobo777')
        self.assertEqual(mentions[0].from_user_id, '123577402')
        self.assertEqual(mentions[0].message, '@dogebot: tip 10')
        self.assertFalse(mentions[0].processed)

        self.assertEqual(mentions[1].from_user_name, '666robobo777')
        self.assertEqual(mentions[1].from_user_id, '123577402')
        self.assertEqual(mentions[1].message, '@dogebot: tip 20')
        self.assertFalse(mentions[1].processed)

    @patch('core.soundcloud_api.soundcloud.Client')
    def test_get_conversations(self, mock_soundcloud):
        results = soundcloud_conversation_fixture
        m1 = MagicMock()
        m1.obj = results[0]
        m2 = MagicMock()
        m2.obj = results[1]
        m3 = MagicMock()
        m3.obj = results[2]
        mocks = [m1, m2, m3]
        mock_soundcloud.return_value.get.return_value = mocks

        soundcloud = SoundCloudAPI()
        res = [r for r in soundcloud.get_conversations()]
        self.assertEqual(len(res), 3)

    @patch('core.soundcloud_api.soundcloud.Client')
    def test_stop_on_already_seen_convo(self, mock_soundcloud):
        results = soundcloud_conversation_fixture
        m1 = MagicMock()
        m1.obj = results[0]
        m2 = MagicMock()
        m2.obj = results[1]
        m3 = MagicMock()
        m3.obj = results[2]
        mocks = [m1, m2, m3]
        mock_soundcloud.return_value.get.return_value = mocks

        soundcloud = SoundCloudAPI()
        soundcloud.create_conversation(results[2])
        res = [r for r in soundcloud.get_conversations()]
        self.assertEqual(len(res), 2)

    @patch('core.soundcloud_api.soundcloud.Client')
    def test_conversations_up_to_date(self, mock_soundcloud):
        results = soundcloud_conversation_fixture
        m1 = MagicMock()
        m1.obj = results[0]
        m2 = MagicMock()
        m2.obj = results[1]
        m3 = MagicMock()
        m3.obj = results[2]
        mocks = [m1, m2, m3]
        mock_soundcloud.return_value.get.return_value = mocks

        soundcloud = SoundCloudAPI()
        soundcloud.create_conversation(results[0])
        res = [r for r in soundcloud.get_conversations()]
        self.assertEqual(len(res), 0)

    @patch('core.soundcloud_api.soundcloud.Client')
    def test_conversation_from_system(self, mock_soundcloud):
        soundcloud = SoundCloudAPI()
        soundcloud.create_conversation(soundcloud_conversation_fixture[2])
        convo = Conversation.objects.get(user_name='system')
        self.assertEqual(convo.user_id, 'system')

    @patch('core.soundcloud_api.soundcloud.Client')
    @patch('core.soundcloud_api.SoundCloudAPI.get_conversations')
    def test_new_conversation(self, mock_convos, mock_soundcloud):
        mock_convos.return_value = soundcloud_conversation_fixture
        soundcloud = SoundCloudAPI()
        soundcloud.create_conversations()
        conversations = Conversation.objects.all()
        self.assertEqual(len(conversations), 3)
        self.assertEqual(conversations[0].convo_id, '77871924:6924356')
        self.assertEqual(conversations[0].user_name, 'Bonbontaq')
        self.assertEqual(conversations[0].user_id, '6924356')

    # @patch('core.soundcloud_api.soundcloud.Client')
    # def test_add_messages_to_conversation(self, _):
    #     soundcloud = SoundCloudAPI()

    # def test_update_conversation(self):
    #     pass

    # def test_create_new_messages(self):
    #     pass

    # def test_get_user_id(self):
    #     soundcloud = SoundCloudAPI()
    #     soundcloud.get_user_id('doge')

    # def test_send_message(self):
    #     soundcloud = SoundCloudAPI()
    #     soundcloud.send_message('bonbontaq', 'hey')
