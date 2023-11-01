from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from database import Database
import re
import time

db = Database('data.db')


api_id = 24948
api_hash = "5152a0"
group = '@test_bot'
session = "session"


class UserToGroupJoiner:
    def __init__(self, api_id, api_hash, group_to_join, session_name) -> None:
        self.api_id = api_id
        self.api_hash = api_hash
        self.group_to_join = group_to_join
        self.session_name = session_name
        self.client = None


    def connect(self):
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        self.client.start()


    def join_to_group(self):
        self.client(JoinChannelRequest(self.group_to_join))
        time.sleep(5)
        group = self.group_to_join
        messages = self.client.get_messages(group, limit=10) # last 10 messages
        captcha_type = None
        bots = db.get_all_bots()
        bot_captcha_types = {}
        captcha_message = None
        if bots:
            bot_captcha_types = {bot[0]: bot[1] for bot in bots}

        for message in messages:
            if message.message is not None:
                bot_id = message.from_id.user_id
                if bot_id in bot_captcha_types: # check bot in db
                    captcha_type = bot_captcha_types[bot_id]
                    captcha_message = message
                else:
                    captcha_type = None

        if captcha_type == None:
            for message in messages:
                if message.message is not None:
                    if 'please, send the solution to the arithmetic operation' in message.message.lower():
                        bot_id = message.from_id.user_id
                        captcha_type = 'shieldy_summ'
                        captcha_message = message
                        db.insert_bot(bot_id, captcha_type)
                        #print('добавлен бот к капче шилди')
                    elif 'не задают глупые вопросы, ответы на которые можно элементарно нагуглить.' in message.message.lower():
                        bot_id = message.from_id.user_id
                        captcha_type = 'rose_button'
                        captcha_message = message
                        db.insert_bot(bot_id, captcha_type)
                        #print('добавлен бот к капче роуз')
                    
        self.bypass_captcha(captcha_message, captcha_type)


    def bypass_captcha(self, message, captcha_type):
        print(message, captcha_type, sep='\n')
        if captcha_type == 'shieldy_summ':
            self.bypass_shieldy_sum_capcha(message)
        elif captcha_type == 'rose_button':
            self.bypass_rose_button_capcha(message)
            

    def bypass_rose_button_capcha(self, message):
        if message.reply_markup and message.reply_markup.rows:
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    if "бот" in button.text.lower():
                        message.click(1)


    def bypass_shieldy_sum_capcha(self, message):
        text = message.message
        matches = re.findall(r'\((.*?)\)', text)
        result = 0
        for match in matches:
            try:
                if re.match(r'^[\d\+\-\*/\(\) ]+$', match):
                    result += eval(match)
            except Exception:
                pass
        entity = self.client.get_entity(self.group_to_join)
        self.client.send_message(entity, str(result))


work = UserToGroupJoiner(api_id, api_hash, group, session)
work.connect()
work.join_to_group()

        
