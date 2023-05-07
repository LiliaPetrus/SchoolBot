from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from datetime import datetime
import json


from . app import dp
from . import messages
from . states import BotStates
from . data_service import get_sections_json, get_sections, post_enrollment
from . keyboards import main_kb, make_inline_enrollment_kb, yesno_kb


@dp.message_handler(commands='start', state='*')
async def send_welcome_command(message: types.Message):
    await BotStates.start_state.set()
    await message.answer(messages.WELCOME_MESSAGE, reply_markup=main_kb)


@dp.message_handler(Text("Спортивні секції"), state='*')
async def view_sections_command(message: types.Message, state: FSMContext):
    await BotStates.view_section_state.set()
    res = await get_sections_json()

    async with state.proxy() as data:
        sections = ''
        for r in res:
            sections = sections + r.get('code') + ' ' + r.get('name') + ' (вільних місць: '\
                       + str(r.get('free_places')) + ')' + '\n'

        return await message.answer(sections, reply_markup=main_kb)


@dp.message_handler(Text('Запис до секції'), state='*')
async def enrollment_command(message: types.Message, state: FSMContext):
    await BotStates.enrollment_state.set()
    s = await get_sections()
    kb = await make_inline_enrollment_kb(s)
    return await message.answer('Виберіть секцію:', reply_markup=kb)


@dp.callback_query_handler(Text(startswith='section_'), state=[BotStates.enrollment_state])
async def section_choose(call: types.CallbackQuery, state: FSMContext):
    await BotStates.enroll_get_section.set()
    async with state.proxy() as data:
        data['section_id'] = call.data.lstrip('section_')
        data['chat_id'] = call.message.chat.id
        await call.message.answer('Ваше прізвище:')
        await BotStates.next()


@dp.message_handler(state=BotStates.enroll_get_lastname)
async def get_lastname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lastname'] = message.text
        await message.answer('Ваше ім\'я:')
        await BotStates.next()


@dp.message_handler(state=BotStates.enroll_get_firstname)
async def get_firstname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['firstname'] = message.text
        await message.answer('По батькові:')
        await BotStates.next()


@dp.message_handler(state=BotStates.enroll_get_patronymic)
async def get_patronymic(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['patronymic'] = message.text
        await message.answer('Ваша дата народження (у форматі ДД.ММ.РРРР):')
        await BotStates.next()


@dp.message_handler(state=BotStates.enroll_get_birthdate)
async def get_birthdate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['birthdate'] = datetime.strftime(datetime.strptime(message.text, '%d.%m.%Y').date(), '%Y-%m-%d')
        await message.answer('Ваша стать (чол або жін):')
        await BotStates.next()


@dp.message_handler(state=BotStates.enroll_get_gender)
async def get_birthdate(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.strip() == 'чол':
            data['gender'] = 'm'
        elif message.text.strip() == 'жін':
            data['gender'] = 'f'
        else:
            data['gender'] = ''

        await BotStates.next()
        await message.answer('Записатись на секцію?', reply_markup=yesno_kb)


@dp.message_handler(text='Так', state=BotStates.enrollment_finish)
async def enrollment_finish(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['status'] = 1
        data_json = json.dumps(data.as_dict())
        result = await post_enrollment(data_json)

        if (result >= 200) and (result < 300):
            await message.answer('Ваша заявка прийнята.', reply_markup=main_kb)
            await state.finish()
        else:
            await message.answer('Не вдалось зберегти заявку! Спробувати ще раз?', reply_markup=yesno_kb)


@dp.message_handler(text='Ні', state=BotStates.enrollment_finish)
async def cancel_enrollment(message: types.Message, state: FSMContext):
    await message.answer('Заявку скасовано!', reply_markup=main_kb)
    await state.finish()
