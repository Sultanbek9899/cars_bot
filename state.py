from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State



class CarsSearchState(StatesGroup):
    search_by_name = State()
    price_start = State()
    price_end = State()
