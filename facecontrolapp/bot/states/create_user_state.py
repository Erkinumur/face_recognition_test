from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateUserState(StatesGroup):
    username = State()
    password = State()
    first_name = State()
    last_name = State()
    image = State()


class CompareFaceState(StatesGroup):
    input = State()
