import vk_api
import requests
import json
import random
import logging


# token = '1fb38556c5dab475cfd727554e1d04f26462f3631c6c15e1dd97c2743def06de18d0dccdd9020b238911e'

#


class VkBot:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)
        logging.basicConfig(filename='bot.log', level=logging.INFO)

    def write_msg(self, peer_id, s):
        self.vk_session.method('messages.send', {'peer_id': peer_id, 'random_id': random.randint(0, 1 << 31), 'message': s})

    def get_conversation_members(self, peer_id):
        answer = self.vk_session.method('messages.getConversationMembers', {'peer_id': peer_id})
        try:
            return answer['profiles']
        except:
            logging.error('Fuck')

    def parse_message(self, message):
        try:
            if '@channel' in message['text']:
                self.channel(message)
            elif '@here' in message['text']:
                self.here(message)
        except vk_api.exceptions.ApiError:
            logging.error('No access')

    def get_long_poll(self):
        return self.vk_session.method('groups.getLongPollServer', {'group_id': 177225451})

    def channel(self, message):
        if '[id457265466|@channel]' in message['text']:
            useful = ''.join(message['text'].split('[id457265466|@channel]'))
        else:
            useful = ''.join(message['text'].split('[id3696360|@channel]'))
        profiles = self.get_conversation_members(message['peer_id'])
        text = []
        for profile in profiles:
            text.append('@' + profile['screen_name'] + ' (_)')
        self.write_msg(message['peer_id'], useful + '\n' + ''.join(text))

    def here(self, message):
        if '[id457265466|@here]' in message['text']:
            useful = ''.join(message['text'].split('[id457265466|@here]'))
        else:
            useful = ''.join(message['text'].split('@here'))
        profiles = self.get_conversation_members(message['peer_id'])
        text = []
        for profile in profiles:
            if profile['online'] == 1:
                text.append('@' + profile['screen_name'] + ' (_)')
        self.write_msg(message['peer_id'], useful + '\n' + ''.join(text))
        return

    def new_bot_processing(self):
        response = self.get_long_poll()
        logging.info(response)
        key = response['key']
        server = response['server']
        ts = int(response['ts'])
        while True:
            try:
                req = json.loads(requests.get(server, params=dict(act='a_check', key=key, ts=ts, wait=25)).text)
                logging.info(req)
                if 'ts' in req:
                    if ts == int(req['ts']):
                        continue
                    ts += 1
                if 'updates' in req:
                    message = req['updates'][0]['object']
                    self.parse_message(message)
                if 'failed' in req:
                    code = int(req['failed'])
                    if code == 1:
                        ts = int(req['ts'])
                    else:
                        response = self.get_long_poll()
                        logging.info(response)
                        key = response['key']
                        server = response['server']
                        ts = int(response['ts'])
            except KeyboardInterrupt:
                logging.info('Stopping')
                return


vk_bot = VkBot('e0042caaa2fec97509415bab21c261b48d1447c7f57b15d18a0b04e226519e6d5221d064b32ac5ae1a02f')
vk_bot.new_bot_processing()
