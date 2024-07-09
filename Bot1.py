import asyncio
import re
from telebot.async_telebot import AsyncTeleBot
import EdgeGPT

BOT_TOKEN = '7023556545:AAEHY3J8oFb-8uvCippEwbH39iv0n2IRG3g'
bot = AsyncTeleBot(BOT_TOKEN)


async def bing_chat(prompt):
    # Надо создать файл cookies.json в папке. ПУТЬ НЕ МЕНЯТЬ, ФАЙЛ cookies.json ДОЛЖЕН БЫТЬ В ПАПКЕ С СКРИПТОМ!
    gbot = EdgeGPT.Chatbot(cookiePath='./data/cookies.json')
    response_dict = await gbot.ask(prompt=prompt)
    return re.sub(r'\[\^\d\^\]', '', response_dict['item']['messages'][1]['text'])


@bot.message_handler(func=lambda message: True)
async def ask(message):
    try:
        prompt = message.text
        if not prompt:
            await bot.reply_to(message, "Пустой запрос")
        else:
            sent_message = await bot.reply_to(message, "Обработка запроса, ожидайте")
            bot_response = await bing_chat(prompt)
            await bot.edit_message_text(chat_id=sent_message.chat.id, message_id=sent_message.message_id,
                                        text=bot_response.replace('?\n\n', ''))
    except Exception as e:
        await bot.reply_to(message,
                           f"{e} Bing по каким-то причинам решил остановить с вами диалог! Проверьте cookie!")  # Такое случается, когда поднимается тема, которую Bing не хочет обсуждать


async def main():
    await bot.infinity_polling()


if __name__ == "__main__":
    asyncio.run(main())
