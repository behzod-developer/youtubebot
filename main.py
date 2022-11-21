import logging
import os.path
import random
import pytube
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandHelp
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

TOKEN = "5612120533:AAGIt3CyvrLXEJDMx1qQ__sFO8wLkGOyY8E"

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class DownloadVideoStater(StatesGroup):
    sending_url = State()


@dp.message_handler(commands=['download_youtube_video'], state=None)
async def her_url (msg: types.Message):
    await DownloadVideoStater.sending_url.set()
    await bot.send_message(msg.from_user.id, 'toduu...')


@dp.message_handler(state=DownloadVideoStater.sending_url)
async def uploadMediaFiles(message: types.Message, state: FSMContext):
    file_name = str(random.randint(0, 100000))
    await bot.send_message(message.chat.id, 'dowloasja')

    try:
        yt = pytube.YouTube(message.text)
        yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        path = './videos'
        if not os.path.exists(path):
            os.makedirs(path)
        file_name += '.mp4'
        yt.download(path, filename=file_name)

        logging.info(f'Started processing {file_name}')


        with open(os.path.join(path, file_name), 'rb') as file:
            await bot.send_video(message.chat.id, file, disable_notification=True )
        await bot.send_message(message.chat.id, 'Successful')
    except Exception  as ex:
        print(ex)
        await bot.send_message(message.chat.id, 'Something wrong. Please, check the link for correct or try again ' )
    finally:
        await state.finish()


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer("You can use /download_youtube_video for downloading YoutubeVideo")

@dp.message_handler(commands=['start'])
async def bot_start(msg: types.Message):
    await bot.send_message(msg.from_user.id, "Hello you can use bot to download YOUTUBE Videos by sending URL\n/start-to start the bot\n/help-we can help you\n/download_youtube_video-TO Download Video from YOUTUBE")



if __name__ =="__main__":
     logging.basicConfig(level=logging.INFO)
     executor.start_polling(dp)
