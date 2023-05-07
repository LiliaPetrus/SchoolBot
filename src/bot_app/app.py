from . settings import API_TOKEN
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=JSONStorage('botstorage.json'))



