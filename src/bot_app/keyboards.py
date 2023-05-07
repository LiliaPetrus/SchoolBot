from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


button_view_section = KeyboardButton('Спортивні секції')
button_enrollment = KeyboardButton('Запис до секції')

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True) #one_time_keyboard=True - hide keyboard
main_kb.row(button_view_section, button_enrollment)

button_yes = KeyboardButton('Так')
button_no = KeyboardButton('Ні')
yesno_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
yesno_kb.row(button_yes, button_no)


async def make_inline_enrollment_kb(sections: list) -> InlineKeyboardMarkup:
    inline_kb = InlineKeyboardMarkup()

    for section in sections:
        inline_kb.add(InlineKeyboardButton(section['name'], callback_data='section_'+str(section['id'])))

    return inline_kb

