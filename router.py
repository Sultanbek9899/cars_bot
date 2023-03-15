from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN 
from bot_utils import handlers as hs 
from state import CarsSearchState

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# Router
# Commands
dp.register_message_handler(hs.welcome_message, commands=["start"])

dp.register_message_handler(hs.update_db, commands=["update_db"])


# text message
dp.register_message_handler(
    hs.search_by_name, 
    content_types=["text"], 
    state=CarsSearchState.search_by_name
    )

dp.register_message_handler(hs.get_cars_by_name, commands=["search_by_name"])
dp.register_message_handler(hs.get_by_price, commands=["search_by_price"])
dp.register_message_handler(hs.delete_old_posts, commands=["delete_posts"])

dp.register_message_handler(hs.get_start_price, state=CarsSearchState.price_start)
dp.register_message_handler(hs.get_end_price, state=CarsSearchState.price_end)