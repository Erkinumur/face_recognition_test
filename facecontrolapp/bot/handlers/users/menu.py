import os

import requests
from aiogram.dispatcher import filters, FSMContext
from aiogram.types import Message, ContentType
from django.contrib.auth import get_user_model

from facecontrolapp.bot.keyboards.default.menu import menu
from facecontrolapp.bot.loader import dp
from facecontrolapp.bot.states.create_user_state import CreateUserState, \
    CompareFaceState

from facecontrolapp.models import Profile, Image
from facecontrolapp.utils import get_face_encoding_string

User = get_user_model()


@dp.message_handler(filters.Text(['Меню', 'меню', 'menu', 'Menu']), state='*')
async def main_menu(message: Message, state: FSMContext):
    markup = menu
    await state.reset_state()
    await message.answer('Главное меню', reply_markup=markup)


@dp.message_handler(text='Создать пользователя')
async def create_user(message: Message, state: FSMContext):
    await CreateUserState.next()
    await message.answer('Введите username')


@dp.message_handler(state=CreateUserState.username)
async def input_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await CreateUserState.next()
    await message.answer('Введите пароль')


@dp.message_handler(state=CreateUserState.password)
async def input_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await CreateUserState.next()
    await message.answer('Введите Имя')


@dp.message_handler(state=CreateUserState.first_name)
async def input_first_name(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await CreateUserState.next()
    await message.answer('Введите Фамилию')


@dp.message_handler(state=CreateUserState.last_name)
async def input_last_name(message: Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await CreateUserState.next()
    await message.answer('Отправьте фото')
    state_ = await state.get_state()
    data = await state.get_data()
    print(state_, data, sep='\n')


@dp.message_handler(content_types=ContentType.PHOTO,
                    state=CreateUserState.image)
async def input_image(message: Message, state: FSMContext):
    image = await message.photo[-1].get_file()
    path = image.to_python().get('file_path')
    await image.download(path)

    print(f'image: {path}')
    file = open(path, 'rb')
    data = await state.get_data()
    files = {'file': (file.name, file, 'image/jpeg')}
    response = requests.post('http://127.0.0.1:8000/api/profile/create/',
                             data=data, files=files)
    await state.reset_state()
    if response.status_code == 201:
        await message.answer('Сохранено')
    else:
        await message.answer('Произошл ошибка, попробуйте еще раз')
    os.remove(path)


@dp.message_handler(text='Распознвание')
async def create_user(message: Message, state: FSMContext):
    await CompareFaceState.next()
    await message.answer('Отправьте фото')


@dp.message_handler(content_types=ContentType.PHOTO,
                    state=CompareFaceState.input)
async def input_image(message: Message, state: FSMContext):
    image = await message.photo[-1].get_file()
    path = image.to_python().get('file_path')
    await image.download(path)
    file = open(path, 'rb')
    files = {'file': (file.name, file, 'image/jpeg')}
    response = requests.post('http://127.0.0.1:8000/api/image/compare/',
                             files=files)
    print(response.json())
    photo = open(response.json().get('file')[1:], 'rb')
    await message.answer_photo(photo)
    await state.reset_state()

    os.remove(path)