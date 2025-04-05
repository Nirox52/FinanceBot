from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="➕ Додати операцію")],
        [KeyboardButton(text="📋 Подивитись усі операціїї")],
        [KeyboardButton(text="📅 Фільтр по датам")],
        [KeyboardButton(text="Видалити операцію")],
        [KeyboardButton(text="✏️ Редагувати запис")],
    ],
    resize_keyboard=True
)

operation_type_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📈 Прибуток"), KeyboardButton(text="📉 Витрата")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

edit_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="type"), KeyboardButton(text="amount")],
        [KeyboardButton(text="description"), KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True
)
confirm_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Так"), KeyboardButton(text="Ні")]
    ],
    resize_keyboard=True
)

