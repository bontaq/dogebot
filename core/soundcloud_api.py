from django.conf import settings
import soundcloud
from core.models import Mention, Conversation, Message
from dateutil import parser
from urlparse import urlparse, parse_qs
import logging
import time

logger = logging.getLogger(__name__)


class SoundCloudAPI():
    def __init__(self):
        self.client = soundcloud.Client(
            client_id=settings.SOUNDCLOUD_CLIENT_ID,
            client_secret=settings.SOUNDCLOUD_CLIENT_SECRET,
            username=settings.SOUNDCLOUD_USERNAME,
            password=settings.SOUNDCLOUD_PASSWORD
        )
        self.user_id = settings.SOUNDCLOUD_USER_ID

    def get_new_mentions(self):
        """Returns a generator for new mentions -- stops when we encounter a mention w/
        the latest uuid we already have stored.  Note: the API call is not documented, so
        keep an eye on this."""

        url = '/activities'
        try:
            uuid = Mention.objects.latest('timestamp').uuid
        except Mention.DoesNotExist:
            uuid = None

        curr_uuid = None
        while curr_uuid is None or curr_uuid != uuid:
            res = self.client.get(url, use_v2=True)

            res_obj = res.obj
            collection = res_obj['collection']
            next_href = res_obj.get('next_href')
            for item in collection:
                curr_uuid = item['uuid']
                if curr_uuid == uuid:
                    return
                elif item['type'] in ['user-mention', 'comment']:
                    yield item

            if next_href:
                url = next_href
            else:
                return

    def create_mentions(self):
        mentions = self.get_new_mentions()
        for mention in mentions:
            if not Mention.objects.filter(uuid=mention['uuid']).exists():
                # TODO: support for tipping specific comments
                Mention(
                    uuid=mention['uuid'],
                    timestamp=parser.parse(mention['created_at']),
                    message=mention['comment']['body'],
                    from_user_name=mention['user']['username'],
                    from_user_id=mention['user']['id'],
                    to_user_name=mention['comment']['track']['user']['username'],
                    to_user_id=mention['comment']['track']['user']['id'],
                    on_track_url=mention['comment']['track']['permalink_url']
                ).save()
                logger.info('created mention: uuid: %s, username: %s, userid: %s, messages: %s',
                            mention['uuid'],
                            mention['user']['username'],
                            mention['user']['id'],
                            mention['comment']['body'])
            else:
                logger.warning('mention already exists: uuid: %s, username: %s, userid: %s, messages: %s',
                               mention['uuid'],
                               mention['user']['username'],
                               mention['user']['id'],
                               mention['comment']['body'])

    def get_messages(self, convo_id):
        results = self.client.get('/me/conversations/{convo_id}/messages'.format(
            convo_id=convo_id)
        )
        return [result.obj for result in results]

    def create_messages(self, convo_obj):
        messages = self.get_messages(convo_obj.convo_id)
        for message in messages:
            message_time = parser.parse(message['sent_at'])
            if Message.objects.filter(conversation=convo_obj,
                                      sent_at=message_time).exists() is not True:
                Message(
                    conversation=convo_obj,
                    user_id=convo_obj.user_id,
                    user_name=convo_obj.user_name,
                    sent_at=message_time,
                    message=message['content']
                ).save()
                logger.info('created message: username: %s, userid: %s, sent_at: %s, message: %s',
                            convo_obj.user_name,
                            convo_obj.user_id,
                            message_time,
                            message['content'])

    def get_conversations(self):
        try:
            most_recent_time = Conversation.objects.latest('last_message_time').last_message_time
        except Conversation.DoesNotExist:
            most_recent_time = None

        most_recent_found = False
        offset = 0
        while not most_recent_found:
            results = self.client.get('/me/conversations', limit=10, offset=offset)
            times = [parser.parse(res.obj['last_message']['sent_at']) for res in results]
            results_times = zip(results, times)
            if len(results) < 10:
                most_recent_found = True

            for res, time in results_times:
                if time != most_recent_time:
                    yield res.obj
                else:
                    most_recent_found = True
                    return

            offset += 10

    def create_conversation(self, convo):
        convo_id = convo['id']
        # id looks like: u'77871924:6924356'
        # our id is first
        from_user_id = convo_id.split(':')[1]
        # username from conversation list of users
        try:
            from_user_name = (user['username'] for user in convo['users']
                              if str(user['id']) == from_user_id).next()
        except KeyError as e:
            if from_user_id == 'system':
                from_user_name = 'system'
            else:
                raise e

        last_message_time = parser.parse(convo['last_message']['sent_at'])
        try:
            convo = Conversation.objects.get(convo_id=convo_id)
            convo.needs_update = convo.last_message_time != last_message_time
            convo.save()
        except Conversation.DoesNotExist:
            Conversation(
                convo_id=convo_id,
                user_name=from_user_name,
                user_id=from_user_id,
                last_message_time=last_message_time
            ).save()

    def create_conversations(self):
        conversations = self.get_conversations()
        for convo in conversations:
            self.create_conversation(convo)

    def get_user_id(self, profile_name):
        """Get the user id from a url / permalink."""
        url = 'https://soundcloud.com/{profile}'.format(profile=profile_name)
        results = self.client.get('/resolve', url=url)
        return results.obj['id']

    def send_message(self, to_user_id, message):
        self.client.post('/me/conversations',
                         id='{me}:{them}'.format(me=self.user_id,
                                                 them=to_user_id),
                         content=message)

    def update_soundcloud(self):
        self.create_mentions()
        # self.create_conversations()
        # for convo_obj in Conversation.objects.filter(needs_update=True):
        #     try:
        #         self.create_messages(convo_obj)
        #         convo_obj.needs_update = False
        #         convo_obj.save()
        #     except Exception as e:
        #         raise e
