from pyrogram import Client
from configparser import ConfigParser
 
config_file = 'config.ini'
config = ConfigParser()
config.read(config_file)
bot_token = config['pyrogram']['bot_token']

Client(
    "emmenyou bot",
    bot_token=bot_token,
).run()
