import logging
from aiogram import Bot, Dispatcher, executor, types
from ikea import *

API_TOKEN = '1947128628:AAEXzb7_wow19ZResCNcV1Yh4BaRgSafx6w'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	"""
    This handler will be called when user sends `/start` or `/help` command
    """
	await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=['curtains'])
async def ikea_curtain_catalog(message: types.Message):
	await message.answer(curtains.get_data())


@dp.message_handler(commands=['echo'])
async def echo(message: types.Message):
	await message.answer(message.text[5:])


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
