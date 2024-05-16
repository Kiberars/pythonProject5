import asyncio

import aiogram
from aiogram import Bot,Dispatcher, types

from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram import F

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


settings = InlineKeyboardMarkup(inline_keyboard=[

    [InlineKeyboardButton(text='Записаться на пробное занятие', callback_data='prob')]
])


phone_request_keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить номер',
                                                           request_contact=True)]],
                                 resize_keyboard=True)

bot = Bot(token='6608481519:AAG56sZq8xV5adEZD--1M3Uek9Ms7kA0eqI')
dp=Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer_photo(photo='AgACAgIAAxkBAAOOZkWooLl3M8VCTf7YrnGHzB8yuEUAAoDhMRvq-zBKSDkHjArADZoBAAMCAAN5AAM1BA',
                               caption="👋 Добро пожаловать в к *KIBERone*", parse_mode="Markdown")
    await message.answer("предлагаем записаться на *Бесплатное* пробное занятие",
                     parse_mode="Markdown", reply_markup=settings)

@dp.callback_query(F.data == 'prob')
async def zayvka(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Данные для заявки будут сформированны автоматически!')
    await callback.message.answer("Нажмите на кнопку ниже, чтобы поделиться номером телефона.",
                         reply_markup=phone_request_keyboard)


@dp.message(lambda message: message.contact)
async def contact_shared(message: types.Message):

    user_info = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    user_id = user_info.user.id
    first_name = user_info.user.first_name
    last_name = user_info.user.last_name
    full_name = user_info.user.full_name
    user_name = user_info.user.username
    phone_number = message.contact.phone_number
    chat_id = message.chat.id

    lid = (f"ID: tg://user?id=<{user_id}>\nИмя: {first_name}\nФамилия: {last_name}\nПолное имя: {full_name}"
                         f"\nНикнейм: {user_name} \nномер телефона: {phone_number} \n Ссылка на пользователя: tg://openmessage?user_id={chat_id}")

    await bot.send_message("-1002001787978", lid,)
    await message.answer('''*Заявка принята* \nтакже можете посетить наш сайт для более подробного ознакомления https://k-ur.kiber-one.com/''',
                          parse_mode="Markdown", reply_markup=ReplyKeyboardRemove())








async def main():
    # dp.include_router(router)
    await dp.start_polling(bot)

if __name__ =='__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
