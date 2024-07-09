# pip install EdgeGPT aiogram.
# Создание виртуального окружения: py -m venv venv, 
# активируем его с помощью команды: venv/Scripts/activate

import EdgeGPT
from aiogram import Bot, types
import aiogram.dispatcher
import aiogram.utils

# import aiogram
# from aiogram import Bot, Dispatcher, executor, types

telegram_token = '7023556545:AAEHY3J8oFb-8uvCippEwbH39iv0n2IRG3g'


async def bing_chat(prompt):
    # Функция получения ответа от BingAI с использованием cookies.
    bing_ai = await EdgeGPT.Chatbot.create(cookie_path='./data/cookies.json')
    response_dict = await bing_ai.ask(prompt)
    return response_dict['item']['messages'][1]['text'].replace("[^\\d^]", "")


bot = Bot(telegram_token)
dp = aiogram.dispatcher.Dispatcher(bot)


@dp.message_handler(lambda message: message.from_user.id != bot.id)
async def send(message: types.Message):
    try:
        prompt = message.text
        if not prompt:
            await message.answer('Вы задали пустой запрос.')
        else:
            await message.answer('Ожидание ответа на ваш запрос...')
            await message.answer_chat_action('typing')
            bot_response = await bing_chat(prompt=prompt)
            await message.answer(bot_response, parse_mode='markdown')
    except Exception as ex:
        await message.answer(f'BingAI не хочет общаться с Вами, ошибка: {ex}. Попробуйте снова.')


if __name__ == '__main__':
    aiogram.utils.executor.start_polling(dp, skip_updates=True)
