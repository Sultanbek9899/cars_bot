from aiogram import types


def get_menu_button(): 
    # Настройки кнопок
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Кнопки
    category = types.InlineKeyboardButton(
        "Категории", callback_data="category")
    search_by_name = types.InlineKeyboardButton(
        "Поиск по имени", callback_data="search_by_name"
    )
    search_by_price = types.InlineKeyboardButton(
        "Поиск по цене", callback_data="search_by_price"
    )
    markup.add(category, search_by_name, search_by_price)
    
    return markup


def get_post_url_button(link):
    markup = types.InlineKeyboardMarkup()
    url = types.InlineKeyboardButton("Перейти на сайт", url=link)
    markup.add(url)
    return markup


def get_pagination_button(offset):
    markup = types.InlineKeyboardMarkup()
    back = types.InlineKeyboardButton("<<<", callback_data="back")
    forward = types.InlineKeyboardButton(">>>", callback_data="forward")
    markup.add(back, forward)
    return markup