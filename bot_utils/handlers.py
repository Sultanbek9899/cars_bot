from aiogram import types
from aiogram.dispatcher import FSMContext

from .keybords import get_menu_button, get_post_url_button, get_pagination_button
from state import CarsSearchState
from db.database import manager

# Аннотация переменных или объектов
# Сообщает к какому классу или объекту относится данная переменная
# или аргумент 

async def welcome_message(message: types.Message):
    text = "Привет, я бот для поиска машин для покупки!"
    markup = get_menu_button()
    await message.answer(text, reply_markup=markup)


async def get_categories(callback: types.CallbackQuery):
    await callback.message.answer("Вы нажали кнопку категорий")


async def get_cars_by_name(message: types.Message):
    text = """
    Пожалуйста отправьте название модели или марки машины,
    которую хотите найти.
    """
    await CarsSearchState.search_by_name.set()
    await message.answer(text)


async def search_by_name(message: types.Message, state: FSMContext):
    print(message.text)
    cars = manager.search_by_name(message.text)
    await state.finish()
    if cars:
        text=""
        for i,car in enumerate(cars, start=1):        
            text += f"{i}) {car[1]}-{car[2]}-{car[3]}-{car[4]} \n\n"
        # markup = get_post_url_button(car[-2])
        pagination = get_pagination_button(offset=0)
        await message.answer(text, parse_mode="HTML", reply_markup=pagination)
    else:
        await message.answer("По данному имени на найдены совпадение в базе.")


from parser.main import main
import asyncio

async def update_db(message: types.Message):
    asyncio.create_task(main())
    await message.answer("Обновление базы данных запущено успешно!")
    

# ПОИСК ПО ЦЕНАМ.

async def get_by_price(message: types.Message):
    text = "Введите пожалуйста цену ОТ которой будет производится поиск"
    await CarsSearchState.price_start.set()
    await message.answer(text)

async def get_start_price(message: types.Message, state: FSMContext):
    start_price = message.text
    async with state.proxy() as data:
        data["start_price"] = start_price
    await CarsSearchState.price_end.set()
    await message.answer("Введите пожалуйста ДО какой цены будет производится поиск")

async def get_end_price(message: types.Message, state: FSMContext):
    end_price = message.text
    start_price = 0
    async with state.proxy() as data:
        start_price = data["start_price"]
    await state.finish()
    cars=manager.search_by_price(start=start_price, end=end_price)
    print(f"{start_price} - {end_price}")
    if cars:
        for car in cars:
            text = f"""
                Название: {car[1]},
                Стоимость: 
                    1) {car[2]}сом
                    2) {car[3]}$
                Номер телефона: {car[4]} 
            """
            markup =get_post_url_button(car[-2])
            await message.answer(text, reply_markup=markup)
    else:
        await message.answer("По данному имени на найдены совпадение в базе.")


# Удаление старых постов
from datetime import datetime, timedelta

async def delete_old_posts(message: types.Message):
    old_time = datetime.now() - timedelta(days=7)
    manager.delete_post(old_time)
    await message.answer("Посты созданные более 30дней назад удалены!")

