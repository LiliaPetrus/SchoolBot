from aiogram.dispatcher.filters.state import State, StatesGroup


class BotStates(StatesGroup):
    start_state = State()
    view_section_state = State()
    enrollment_state = State()
    enroll_get_section = State()
    enroll_get_lastname = State()
    enroll_get_firstname = State()
    enroll_get_patronymic = State()
    enroll_get_birthdate = State()
    enroll_get_gender = State()
    enrollment_finish = State()
