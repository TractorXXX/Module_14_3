from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

import asyncio

from keyboards import *
import texts

api = '***' # Удалил реальный ключ, как было сказано в задании.
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands='start')
async def start(message):
    await message.answer(texts.welcome, reply_markup=start_kb)

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in range(1, 5):
        with open(f'{i}.png', 'rb') as img:
            await message.answer(f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')
            await message.answer_photo(img)
    await message.answer(texts.choice_product, reply_markup=inline_menu)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(texts.buy_product)
    await call.answer()

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer(texts.info_bot)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer(texts.choice_option, reply_markup=kb_in)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer(texts.formula)
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer(texts.age, reply_markup=start_kb)
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer(texts.growth, reply_markup=start_kb)
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer(texts.weight, reply_markup=start_kb)
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()

# Упрощённая формула Миффлина - Сан Жеора

    calculator_calories = 10 * int(data['third']) + 6.25 * int(data['second']) - 5 * int(data['first']) + 5
    await message.answer(f'Для похудения или сохранения нормального веса, '
                         f'Вам нужно потреблять не более {calculator_calories} калорий', reply_markup=start_kb)
    await state.finish()

# Следующий хендлер перехватывает все остальные сообщения

@dp.message_handler()
async def start(message):
    await message.answer(texts.start)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
