#聊天机器人训练代码
#请不要修改文件名为chatterbot，否则会导致导入模块出错
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
chatbot = ChatBot("Bob")
from chatterbot.trainers import ListTrainer
bot = ChatBot(
    'Bob',
    storage_adapter='chatterbot.storage.MongoDatabaseAdapter'
)
trainer = ChatterBotCorpusTrainer(bot)
trainer.train("chatterbot.corpus.chinese")
trainer.train("chatterbot.corpus.english")
