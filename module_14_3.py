"""
coding: utf-8
Дегтярев Виталий (группа 22/08)
Домашнее задание №14.3
Домашнее задание по теме "Доработка бота"
"""

import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

logging.basicConfig(level=logging.INFO)
api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage= MemoryStorage())


# Определение класса состояний
class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Инициализация главной клавиатуры
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
button3 = KeyboardButton(text='Купить')
kb.add(button)
kb.insert(button2)
kb.add(button3)

# Инициализация инлайн клавиатуры1
kb_inl = InlineKeyboardMarkup()
button4 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button5 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_inl.add(button4)
kb_inl.insert(button5)

# Инициализация инлайн клавиатуры2
kb_inl2 = InlineKeyboardMarkup()
button6 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button7 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button8 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button9 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb_inl2.add(button6)
kb_inl2.insert(button7)
kb_inl2.insert(button8)
kb_inl2.insert(button9)


# Стартовая функция
@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью", reply_markup = kb)


# Главное меню
@dp.message_handler(text="Рассчитать")
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=kb_inl)

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('https://www.calc.ru/Formula-Mifflinasan-Zheora.html')

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'files/product{i}.png', "rb") as img:
            await message.answer(f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')
            await message.answer_photo(img)
    await message.answer('Выбери продукт для покупки:', reply_markup=kb_inl2)


# Блок функций машины состояний для расчета калорий
@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer("Введите свой рост")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer("Введите свой вес")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    data['calories'] = 10*int(data['weight'])+6.25*int(data['growth'])-5*int(data['age'])+5
    await message.answer(f"Ваша норма калорий (для мужчины) составляет: {data['calories']} кал")
    await state.finish()


# Функция показа формулы расчета калорий
@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer("для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5")
    await call.answer()


# Функция покупки продукта
@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer("Вы успешно приобрели продукт!")
    await call.answer()


# Реакция на прочие сообщения пользователя
@dp.message_handler()
async def all_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")


# Запуск Телеграм-бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)