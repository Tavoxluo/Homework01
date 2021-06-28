#机器人测试代码

from chatterbot import ChatBot

bot = ChatBot(
    'Bob',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter'
)

def r(s):return bot.get_response(s).text

while True:  # 当输入不为exit时打印出机器人的输出，否则退出
    i = input('>>> ').strip()
    if i != 'exit':
        print(r(i))
    else:
        break