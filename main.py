import asyncio
import logging
import os
import sys
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton
from aiogram.utils.i18n import gettext as _, I18n, FSMI18nMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from dotenv import load_dotenv

load_dotenv('.env')

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
ADMIN_LIST = 6199875730


def menu_button():
    btn1 = KeyboardButton(text="Sherik kerak 🤝")
    btn2 = KeyboardButton(text="Ish joyi kerak 💰")
    btn3 = KeyboardButton(text="Hodim kerak 🧑")
    btn4 = KeyboardButton(text="Ustoz kerak 🤓")
    btn5 = KeyboardButton(text="Shogird kerak 🧒")
    markup = ReplyKeyboardBuilder()
    markup.add(*[btn1, btn2, btn3, btn4, btn5])
    markup.adjust(2, 2, 1)
    markup = markup.as_markup()
    markup.resize_keyboard = True
    return markup


@dp.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    ikb = InlineKeyboardBuilder()
    ikb.add(
        InlineKeyboardButton(text='Uz🇺🇿', callback_data='lang_uz'),
        InlineKeyboardButton(text='En🇬🇧', callback_data='lang_en')
    )
    await message.answer(_('Tilni tanlang!'), reply_markup=ikb.as_markup(resize_keyboard=True))


@dp.callback_query(F.data.startswith('lang_'))
async def language_handler(callback: CallbackQuery, state: FSMContext):
    lang_code = callback.data.split('lang_')[-1]
    await callback.answer(_('Til tanlandi!', locale=lang_code))
    await state.update_data(locale=lang_code)
    await callback.message.answer(
        f"Hello, {callback.message.from_user.full_name} \nUstoz-Shogird kanalining FAKE botiga Xush kelipsiz! \n\n/help 'yordam' buyrugi orqali nimalarga qodir ekanligimni bilib oling",
        reply_markup=menu_button())


class FormState1(StatesGroup):
    firt_name = State()
    texnologiya = State()
    aloqa = State()
    hudud = State()
    narxi = State()
    kasbi = State()
    time_murojat = State()
    maqsad = State()
    finish = State()


@dp.message(F.text == "Sherik kerak 🤝")
async def button1_handler(message: Message, state: FSMContext):
    await state.set_state(FormState1.firt_name)
    await message.answer(
        "Sherik topish uchun ariza berish! \n\nHozir sizga birnecha savollar beriladi. Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.",
        reply_markup=menu_button())
    await message.answer("Ism, Familiyangizni kiriting?", reply_markup=menu_button())


@dp.message(FormState1.firt_name)
async def texno_handler(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(FormState1.texnologiya)
    await message.answer(
        "📚 Texnologiya: \n\nTalab qilinadigan texnologiyalarni kiriting?Texnologiya nomlarini vergul bilan ajrating. \nMasalan: Java, C++, C#, Python")


@dp.message(FormState1.texnologiya)
async def phone_handler(message: Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await state.set_state(FormState1.aloqa)
    await message.answer("📞 Aloqa: \n\nBog`lanish uchun raqamingizni kiriting?. \nMasalan: +998 90 123 45 67")


@dp.message(FormState1.aloqa)
async def hudud_handler(message: Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await state.set_state(FormState1.hudud)
    await message.answer("🌐 Hudud: \n\nQaysi hududdansiz?. \nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")


@dp.message(FormState1.hudud)
async def narx_handler(message: Message, state: FSMContext):
    await state.update_data(hudud=message.text)
    await state.set_state(FormState1.narxi)
    await message.answer("💰 Narxi: \n\nTolov qilasizmi yoki Tekinmi? \nKerak bo`lsa, Summani kiriting?")


@dp.message(FormState1.narxi)
async def job_handler(message: Message, state: FSMContext):
    await state.update_data(narxi=message.text)
    await state.set_state(FormState1.kasbi)
    await message.answer("👨🏻‍💻 Kasbi: \n\nIshlaysizmi yoki o`qiysizmi? \nMasalan: Talaba")


@dp.message(FormState1.kasbi)
async def aloqa_handler(message: Message, state: FSMContext):
    await state.update_data(kasbi=message.text)
    await state.set_state(FormState1.time_murojat)
    await message.answer("🕰 Murojaat qilish vaqti:  \n\nQaysi vaqtda murojaat qilish mumkin? \nMasalan: 09:00-18:00")


@dp.message(FormState1.time_murojat)
async def maqsad_handler(message: Message, state: FSMContext):
    await state.update_data(time_murojat=message.text)
    await state.set_state(FormState1.maqsad)
    await message.answer("🔎 Maqsad:   \n\nMaqsadingizni qisqacha yozib bering.")


@dp.message(FormState1.maqsad)
async def sherik_handler(message: Message, state: FSMContext):
    await state.update_data(maqsad=message.text)
    await state.set_state(FormState1.finish)
    data = await state.get_data()
    text = f"""
Sherik kerak 🤝:
    
🏅 Sherik: {data['first_name']}
📚 Texnologiya: {data['texnologiya']}
🇺🇿 Telegram: {message.from_user.username}
📞 Aloqa: {data['aloqa']}
🌐 Hudud: {data['hudud']}
💰 Narxi: {data['narxi']}
👨🏻‍💻 Kasbi: {data['kasbi']}
🕰 Murojaat qilish vaqti: {data['time_murojat']}
🔎 Maqsad: {data['maqsad']}

     #sherik #{data['texnologiya']} #{data['hudud']}
 """
    await message.answer(text, reply_markup=menu_button())
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text="Xa ✅"), KeyboardButton(text="Yo'q ❌"))
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(FormState1.finish)
async def finish_handler(message: Message, state: FSMContext):
    if message.text == "Xa ✅":
        await message.answer("Adminga yuborildi!")
    else:
        await message.answer("Qabul qilinmadi!")
    await state.clear()


class FormState2(StatesGroup):
    firt_name = State()
    age = State()
    texnologiya = State()
    aloqa = State()
    hudud = State()
    narxi = State()
    kasbi = State()
    time_murojat = State()
    maqsad = State()
    finish = State()


@dp.message(F.text == "Ish joyi kerak 💰")
async def button2_handler(message: Message, state: FSMContext):
    await state.set_state(FormState2.firt_name)
    await message.answer(
        "Ish joyi topish uchun ariza berish! \n\nHozir sizga birnecha savollar beriladi. Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.",
        reply_markup=menu_button())
    await message.answer("Ism, Familiyangizni kiriting?", reply_markup=menu_button())


@dp.message(FormState2.firt_name)
async def age_handler(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(FormState2.age)
    await message.answer("🕑 Yosh: \n\nYoshingizni kiriting? \nMasalan: 19")


@dp.message(FormState2.age)
async def texno_handler(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(FormState2.texnologiya)
    await message.answer(
        "📚 Texnologiya: \n\nTalab qilinadigan texnologiyalarni kiriting?Texnologiya nomlarini vergul bilan ajrating. \nMasalan: Java, C++, C#, Python")


@dp.message(FormState2.texnologiya)
async def phone_handler(message: Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await state.set_state(FormState2.time_murojat)
    await message.answer("📞 Aloqa: \n\nBog`lanish uchun raqamingizni kiriting?. \nMasalan: +998 90 123 45 67")


@dp.message(FormState2.time_murojat)
async def hudud_handler(message: Message, state: FSMContext):
    await state.update_data(time_murojat=message.text)
    await state.set_state(FormState2.hudud)
    await message.answer("🌐 Hudud: \n\nQaysi hududdansiz?. \nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")


@dp.message(FormState2.hudud)
async def narx_handler(message: Message, state: FSMContext):
    await state.update_data(hudud=message.text)
    await state.set_state(FormState2.narxi)
    await message.answer("💰 Narxi: \n\nTolov qilasizmi yoki Tekinmi? \nKerak bo`lsa, Summani kiriting?")


@dp.message(FormState2.narxi)
async def job_handler(message: Message, state: FSMContext):
    await state.update_data(narxi=message.text)
    await state.set_state(FormState2.kasbi)
    await message.answer("👨🏻‍💻 Kasbi: \n\nIshlaysizmi yoki o`qiysizmi? \nMasalan: Talaba")


@dp.message(FormState2.kasbi)
async def aloqa_handler(message: Message, state: FSMContext):
    await state.update_data(kasbi=message.text)
    await state.set_state(FormState2.aloqa)
    await message.answer("🕰 Murojaat qilish vaqti:  \n\nQaysi vaqtda murojaat qilish mumkin? \nMasalan: 09:00-18:00")


@dp.message(FormState2.aloqa)
async def maqsad_handler(message: Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await state.set_state(FormState2.maqsad)
    await message.answer("🔎 Maqsad:   \n\nMaqsadingizni qisqacha yozib bering.")


@dp.message(FormState2.maqsad)
async def ish_joyi_handler(message: Message, state: FSMContext):
    await state.update_data(maqsad=message.text)
    await state.set_state(FormState2.finish)
    data = await state.get_data()
    text = f"""
    Ish joyi kerak 🤝:

    👨‍💼 Xodim: {data['first_name']}
    🕑 Yosh: {data['age']}
    📚 Texnologiya: {data['texnologiya']}
    🇺🇿 Telegram: {message.from_user.username}
    📞 Aloqa: {data['aloqa']}
    🌐 Hudud: {data['hudud']}
    💰 Narxi: {data['narxi']}
    👨🏻‍💻 Kasbi: {data['kasbi']}
    🕰 Murojaat qilish vaqti: {data['time_murojat']}
    🔎 Maqsad: {data['maqsad']}

         #xodim #{data['texnologiya']} #{data['hudud']}
     """
    await message.answer(text, reply_markup=menu_button())
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text="Xa ✅"), KeyboardButton(text="Yo'q ❌"))
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(FormState2.finish)
async def finish_handler(message: Message, state: FSMContext):
    if message.text == "Xa ✅":
        await message.answer("Adminga yuborildi!")
    else:
        await message.answer("Qabul qilinmadi!")
    await state.clear()


class FormState3(StatesGroup):
    idora = State()
    age = State()
    texnologiya = State()
    aloqa = State()
    hudud = State()
    masul_hodim = State()
    time_murojat = State()
    kasbi = State()
    narxi = State()
    maqsad = State()
    finish = State()


@dp.message(F.text == "Xodim kerak 🧑")
async def button3_handler(message: Message, state: FSMContext):
    await state.set_state(FormState2.idora)
    await message.answer(
        "Xodim topish uchun ariza berish! \n\nHozir sizga birnecha savollar beriladi. Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.",
        reply_markup=menu_button())
    await message.answer("🎓 Idora nomi?", reply_markup=menu_button())


@dp.message(FormState3.idora)
async def texno_handler(message: Message, state: FSMContext):
    await state.update_data(idora=message.text)
    await state.set_state(FormState1.texnologiya)
    await message.answer(
        "📚 Texnologiya: \n\nTalab qilinadigan texnologiyalarni kiriting?Texnologiya nomlarini vergul bilan ajrating. \nMasalan: Java, C++, C#, Python")


@dp.message(FormState3.texnologiya)
async def phone_handler(message: Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await state.set_state(FormState3.aloqa)
    await message.answer("📞 Aloqa: \n\nBog`lanish uchun raqamingizni kiriting?. \nMasalan: +998 90 123 45 67")


@dp.message(FormState3.aloqa)
async def hudud_handler(message: Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await state.set_state(FormState3.hudud)
    await message.answer("🌐 Hudud: \n\nQaysi hududdansiz?. \nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")


@dp.message(FormState3.hudud)
async def masul_handler(message: Message, state: FSMContext):
    await state.update_data(hudud=message.text)
    await state.set_state(FormState3.masul_hodim)
    await message.answer("✍️Mas'ul ism sharifi?")


@dp.message(FormState3.masul_hodim)
async def aloqa_handler(message: Message, state: FSMContext):
    await state.update_data(masul_hodim=message.text)
    await state.set_state(FormState3.time_murojat)
    await message.answer("🕰 Murojaat qilish vaqti:  \n\nQaysi vaqtda murojaat qilish mumkin? \nMasalan: 09:00-18:00")


@dp.message(FormState3.time_murojat)
async def jobs_time_handler(message: Message, state: FSMContext):
    await state.update_data(time_murojat=message.text)
    await state.set_state(FormState3.kasbi)
    await message.answer("🕰 Ish vaqtini kiriting?")


@dp.message(FormState3.kasbi)
async def price_handler(message: Message, state: FSMContext):
    await state.update_data(kasbi=message.text)
    await state.set_state(FormState3.narxi)
    await message.answer("💰 Maoshni kiriting?")


@dp.message(FormState3.narxi)
async def addtion_handler(message: Message, state: FSMContext):
    await state.update_data(narxi=message.text)
    await state.set_state(FormState3.maqsad)
    await message.answer("‼️ Qo`shimcha ma`lumotlar?")


@dp.message(FormState1.maqsad)
async def xodim_handler(message: Message, state: FSMContext):
    await state.update_data(maqsad=message.text)
    await state.set_state(FormState3.finish)
    data = await state.get_data()
    text = f"""
Xodim kerak 🤝:

🏢 Idora: : {data['idora']}
📚 Texnologiya: {data['texnologiya']}
🇺🇿 Telegram: {message.from_user.username}
📞 Aloqa: {data['aloqa']}
🌐 Hudud: {data['aloqa']}
✍️ Mas'ul: {data['masul_hodim']}
🕰 Murojaat qilish vaqti: {data['time_murojat']}
🕰 Ish vaqti: {data['kasbi']}
💰 Narxi: {data['hudud']}
‼️ Qo`shimcha: {data['maqsad']}

     #Ishjoyi #{data['texnologiya']}#{data['hudud']}
 """
    await message.answer(text, reply_markup=menu_button())
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text="Xa ✅"), KeyboardButton(text="Yo'q ❌"))
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(FormState3.finish)
async def finish_handler(message: Message, state: FSMContext):
    if message.text == "Xa ✅":
        await message.answer("Adminga yuborildi!")
    else:
        await message.answer("Qabul qilinmadi!")
    await state.clear()


class FormState4(StatesGroup):
    firt_name = State()
    age = State()
    texnologiya = State()
    aloqa = State()
    hudud = State()
    narxi = State()
    kasbi = State()
    time_murojat = State()
    maqsad = State()
    finish = State()


@dp.message(F.text == "Ustoz kerak 🤓")
async def button4_handler(message: Message, state: FSMContext):
    await state.set_state(FormState2.firt_name)
    await message.answer(
        "Ustoz topish uchun ariza berish! \n\nHozir sizga birnecha savollar beriladi. Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.",
        reply_markup=menu_button())
    await message.answer("Ism, Familiyangizni kiriting?", reply_markup=menu_button())


@dp.message(FormState4.firt_name)
async def age_handler(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(FormState4.age)
    await message.answer("🕑 Yosh: \n\nYoshingizni kiriting? \nMasalan: 19")


@dp.message(FormState4.age)
async def texno_handler(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(FormState4.texnologiya)
    await message.answer(
        "📚 Texnologiya: \n\nTalab qilinadigan texnologiyalarni kiriting?Texnologiya nomlarini vergul bilan ajrating. \nMasalan: Java, C++, C#, Python")


@dp.message(FormState4.texnologiya)
async def phone_handler(message: Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await state.set_state(FormState4.aloqa)
    await message.answer("📞 Aloqa: \n\nBog`lanish uchun raqamingizni kiriting?. \nMasalan: +998 90 123 45 67")


@dp.message(FormState4.aloqa)
async def hudud_handler(message: Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await state.set_state(FormState4.hudud)
    await message.answer("🌐 Hudud: \n\nQaysi hududdansiz?. \nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")


@dp.message(FormState4.hudud)
async def narx_handler(message: Message, state: FSMContext):
    await state.update_data(hudud=message.text)
    await state.set_state(FormState1.narxi)
    await message.answer("💰 Narxi: \n\nTolov qilasizmi yoki Tekinmi? \nKerak bo`lsa, Summani kiriting?")


@dp.message(FormState4.narxi)
async def job_handler(message: Message, state: FSMContext):
    await state.update_data(narxi=message.text)
    await state.set_state(FormState4.kasbi)
    await message.answer("👨🏻‍💻 Kasbi: \n\nIshlaysizmi yoki o`qiysizmi? \nMasalan: Talaba")


@dp.message(FormState4.kasbi)
async def aloqa_handler(message: Message, state: FSMContext):
    await state.update_data(kasbi=message.text)
    await state.set_state(FormState4.time_murojat)
    await message.answer("🕰 Murojaat qilish vaqti:  \n\nQaysi vaqtda murojaat qilish mumkin? \nMasalan: 09:00-18:00")


@dp.message(FormState4.aloqa)
async def maqsad_handler(message: Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await state.set_state(FormState4.maqsad)
    await message.answer("🔎 Maqsad:   \n\nMaqsadingizni qisqacha yozib bering.")


@dp.message(FormState4.maqsad)
async def ish_joyi_handler(message: Message, state: FSMContext):
    await state.update_data(maqsad=message.text)
    await state.set_state(FormState4.finish)
    data = await state.get_data()
    text = f"""
    Ustoz kerak 🤝:

    🎓 Shogird:  {data['first_name']}
    🕑 Yosh: {data['age']}
    📚 Texnologiya: {data['texnologiya']}
    🇺🇿 Telegram: {message.from_user.username}
    📞 Aloqa: {data['aloqa']}
    🌐 Hudud: {data['hudud']}
    💰 Narxi: {data['narxi']}
    👨🏻‍💻 Kasbi: {data['kasbi']}
    🕰 Murojaat qilish vaqti: {data['time_murojat']}
    🔎 Maqsad: {data['maqsad']}

         #xodim #{data['texnologiya']} #{data['hudud']}
     """
    await message.answer(text, reply_markup=menu_button())
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text="Xa ✅"), KeyboardButton(text="Yo'q ❌"))
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(FormState4.finish)
async def finish_handler(message: Message, state: FSMContext):
    if message.text == "Xa ✅":
        await message.answer("Adminga yuborildi!")
    else:
        await message.answer("Qabul qilinmadi!")
    await state.clear()


class FormState5(StatesGroup):
    firt_name = State()
    age = State()
    texnologiya = State()
    aloqa = State()
    hudud = State()
    narxi = State()
    kasbi = State()
    time_murojat = State()
    maqsad = State()
    finish = State()


@dp.message(F.text == "Shogird kerak 🧒")
async def button5_handler(message: Message, state: FSMContext):
    await state.set_state(FormState2.firt_name)
    await message.answer(
        "Shogird topish uchun ariza berish! \n\nHozir sizga birnecha savollar beriladi. Har biriga javob bering. Oxirida agar hammasi to`g`ri bo`lsa, HA tugmasini bosing va arizangiz Adminga yuboriladi.",
        reply_markup=menu_button())
    await message.answer("Ism, Familiyangizni kiriting?", reply_markup=menu_button())


@dp.message(FormState5.firt_name)
async def age_handler(message: Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await state.set_state(FormState5.age)
    await message.answer("🕑 Yosh: \n\nYoshingizni kiriting? \nMasalan: 19")


@dp.message(FormState5.age)
async def texno_handler(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await state.set_state(FormState5.texnologiya)
    await message.answer(
        "📚 Texnologiya: \n\nTalab qilinadigan texnologiyalarni kiriting?Texnologiya nomlarini vergul bilan ajrating. \nMasalan: Java, C++, C#, Python")


@dp.message(FormState5.texnologiya)
async def phone_handler(message: Message, state: FSMContext):
    await state.update_data(texnologiya=message.text)
    await state.set_state(FormState5.aloqa)
    await message.answer("📞 Aloqa: \n\nBog`lanish uchun raqamingizni kiriting?. \nMasalan: +998 90 123 45 67")


@dp.message(FormState5.aloqa)
async def hudud_handler(message: Message, state: FSMContext):
    await state.update_data(aloqa=message.text)
    await state.set_state(FormState5.hudud)
    await message.answer("🌐 Hudud: \n\nQaysi hududdansiz?. \nViloyat nomi, Toshkent shahar yoki Respublikani kiriting.")


@dp.message(FormState5.hudud)
async def narx_handler(message: Message, state: FSMContext):
    await state.update_data(hudud=message.text)
    await state.set_state(FormState5.narxi)
    await message.answer("💰 Narxi: \n\nTolov qilasizmi yoki Tekinmi? \nKerak bo`lsa, Summani kiriting?")


@dp.message(FormState5.narxi)
async def job_handler(message: Message, state: FSMContext):
    await state.update_data(narxi=message.text)
    await state.set_state(FormState5.kasbi)
    await message.answer("👨🏻‍💻 Kasbi: \n\nIshlaysizmi yoki o`qiysizmi? \nMasalan: Talaba")


@dp.message(FormState5.kasbi)
async def aloqa_handler(message: Message, state: FSMContext):
    await state.update_data(kasbi=message.text)
    await state.set_state(FormState5.time_murojat)
    await message.answer("🕰 Murojaat qilish vaqti:  \n\nQaysi vaqtda murojaat qilish mumkin? \nMasalan: 09:00-18:00")


@dp.message(FormState5.time_murojat)
async def maqsad_handler(message: Message, state: FSMContext):
    await state.update_data(time_murojat=message.text)
    await state.set_state(FormState5.maqsad)
    await message.answer("🔎 Maqsad:   \n\nMaqsadingizni qisqacha yozib bering.")


@dp.message(FormState5.maqsad)
async def ish_joyi_handler(message: Message, state: FSMContext):
    await state.update_data(maqsad=message.text)
    await state.set_state(FormState4.finish)
    data = await state.get_data()
    text = f"""
    Shogird kerak 🤝:

    🎓 Ustoz: {data['first_name']}
    🕑 Yosh: {data['age']}
    📚 Texnologiya: {data['texnologiya']}
    🇺🇿 Telegram: {message.from_user.username}
    📞 Aloqa: {data['aloqa']}
    🌐 Hudud: {data['hudud']}
    💰 Narxi: {data['narxi']}
    👨🏻‍💻 Kasbi: {data['kasbi']}
    🕰 Murojaat qilish vaqti: {data['time_murojat']}
    🔎 Maqsad: {data['maqsad']}

         #xodim #{data['texnologiya']} #{data['hudud']}
     """
    await message.answer(text, reply_markup=menu_button())
    rkb = ReplyKeyboardBuilder()
    rkb.add(KeyboardButton(text="Xa ✅"), KeyboardButton(text="Yo'q ❌"))
    await message.answer("Barcha ma'lumotlar to'g'rimi?", reply_markup=rkb.as_markup(resize_keyboard=True))


@dp.message(FormState5.finish)
async def finish_handler(message: Message, state: FSMContext):
    if message.text == "Xa ✅":
        await message.answer("Adminga yuborildi!")
    else:
        await message.answer("Qabul qilinmadi!")
    await state.clear()


async def main() -> None:
    bot = Bot(token=TOKEN)
    i18n = I18n(path='locales')
    dp.update.outer_middleware.register(FSMI18nMiddleware(i18n))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
