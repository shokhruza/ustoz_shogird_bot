# import asyncio
# import json
# import logging
# import sys
#
# import aiofiles
# from aiogram import Bot, Dispatcher, html, F
#
# from aiogram.filters import CommandStart, Command
# from aiogram.types import Message, InlineKeyboardButton, CallbackQuery, KeyboardButton, FSInputFile
# from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
#
# TOKEN = "6533700115:AAHUF1ZgrfHFDDZifx-pbaY5JrdXQW2rFZs"
#
# dp = Dispatcher()
#
# ADMIN_LIST = 6199875730
#
#
#
# @dp.message(CommandStart())
# async def start_handler(message: Message):
#     rkb = ReplyKeyboardBuilder()
#     rkb.add(KeyboardButton(text="Uz🇺🇿"), KeyboardButton(text="En🇬🇧"))
#     await message.answer("Tilni tanlang 👇", reply_markup=rkb.as_markup(resize_keyboard=True))
#
#
# @dp.message(F.text=="Uz🇺🇿")
# async def uzb_handler(message: Message):
#     rkb1 = ReplyKeyboardBuilder()
#     rkb1.add(KeyboardButton(text="Menu 📄"), KeyboardButton(text="Sozlarmalar ⚙"), KeyboardButton(text="Ma'lumot 📊"))
#     rkb1.adjust(3,1)
#     await message.answer("O'zbek tili tanlandi!",  reply_markup=rkb1.as_markup(resize_keyboard=True))
#
#
# @dp.message(F.text=="En🇬🇧")
# async def eng_handler(message: Message):
#     rkb2 = ReplyKeyboardBuilder()
#     rkb2.add(KeyboardButton(text="Menu 📄"), KeyboardButton(text="Settings ⚙"), KeyboardButton(text="Info 📊"))
#     rkb2.adjust(3,1)
#     await message.answer("English is selected!", reply_markup=rkb2.as_markup(resize_keyboard=True))
#
# async def main() -> None:
#     bot = Bot(token=TOKEN)
#     await dp.start_polling(bot)
#
#
# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)
#     asyncio.run(main())

















import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, \
    CallbackQuery, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.i18n import I18n, FSMI18nMiddleware, gettext as _, lazy_gettext as __
from aiogram.utils.keyboard import ReplyKeyboardBuilder

TOKEN = "6533700115:AAHUF1ZgrfHFDDZifx-pbaY5JrdXQW2rFZs"

dp = Dispatcher()

admin = 6199875730


class Form(StatesGroup):
    button = ""
    full_name = State()
    age = State()
    technologies = State()
    phone_number = State()
    address = State()
    price = State()
    work_place = State()
    goal = State()


def menu_btn():
    btn = ReplyKeyboardBuilder()
    btn.add(*[KeyboardButton(text=_("Sherik kerak")), KeyboardButton(text=_("Ish joyi kerak"))])
    btn.add(*[KeyboardButton(text=_("Hodim kerak")), KeyboardButton(text=_("Ustoz kerak"))])
    btn.add(KeyboardButton(text=_("Shogird kerak")))
    btn.adjust(2, repeat=True)
    return btn.as_markup(resize_keyboard=True)


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(_("Assalomu alaykum ") + message.from_user.full_name, reply_markup=menu_btn())


@dp.message(
    F.text.in_([__("Ish joyi kerak"), __("Sherik kerak"), __("Hodim kerak"), __("Ustoz kerak"), __("Shogird kerak")]))
async def ish_handler(message: Message, state: FSMContext):
    button = message.text.split("kerak")[0].strip()
    await state.set_state(Form.full_name)
    await state.update_data(button=button)
    await message.answer(button + _(" kerak Bunga oid sizga bir nechta savollar beriladi"),
                         reply_markup=ReplyKeyboardRemove())
    if button == _("Hodim"):
        await message.answer(_("🏢 Idora: \n🎓 Idora nomi?"))
        return
    await message.answer(button + _("\nIsm, familiyangizni kiriting?"))


@dp.message(Form.full_name)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    data = await state.get_data()
    await state.set_state(Form.age)
    if data['button'] == _("Hodim"):
        await message.answer(_("✍️ Mas'ul: \n\n✍️Mas'ul ism sharifi?"))
        return
    await message.answer(_("""🕑 Yosh: \nYoshingizni kiriting? \nMasalan, 19"""))


@dp.message(Form.age)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.technologies)
    await state.update_data(age=message.text)
    await message.answer(
        _("📚 Texnologiya:\nTalab qilinadigan texnologiyalarni kiriting?\nTexnologiya nomlarini vergul bilan ajrating. Masalan, \nJava, C++, C#"))


@dp.message(Form.technologies)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.phone_number)
    await state.update_data(technologies=message.text)
    await message.answer(_("📞 Aloqa: \n\nBog`lanish uchun raqamingizni kiriting?\nMasalan, +998 90 123 45 67"))


@dp.message(Form.phone_number)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.address)
    await state.update_data(phone_number=message.text)
    await message.answer(
        _("🌐 Hudud: \n\nQaysi hududdansiz?\nViloyat nomi, Toshkent shahar yoki Respublikani kiriting."))


@dp.message(Form.address)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.price)
    await state.update_data(address=message.text)
    data = await state.get_data()
    if data['button'] == _("Hodim"):
        await message.answer(_("💰 Maosh: \n\n💰 Maoshni kiriting?"))
        return
    await message.answer(_("💰 Narxi:\n\nTolov qilasizmi yoki Tekinmi?\nKerak bo`lsa, Summani kiriting?"))


@dp.message(Form.price)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.work_place)
    await state.update_data(price=message.text)
    data = await state.get_data()
    if data['button'] == _("Hodim"):
        await message.answer(_("🕰 Ish vaqti: \n\n🕰 Ish vaqtini kiriting?"))
        return
    await message.answer(_("👨🏻‍💻 Kasbi: \n\nIshlaysizmi yoki o`qiysizmi?\nMasalan, Talaba"))


@dp.message(Form.work_place)
async def full_name(message: Message, state: FSMContext):
    await state.set_state(Form.goal)
    await state.update_data(work_place=message.text)
    data = await state.get_data()
    if data['button'] == _("Hodim"):
        await message.answer(_("""‼️ Qo`shimcha: 
‼️ Qo`shimcha ma`lumotlar?"""))
        return
    await message.answer(_("🔎 Maqsad: \n\nMaqsadingizni qisqacha yozib bering."))


@dp.message(Form.goal)
async def full_name(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    data = await state.get_data()
    xodim = '👨‍💼' + _("Xodim")
    Yosh = _("Yosh")
    Narxi = _("Narxi")
    Kasbi = _("Kasbi")
    Maqsad = _("Maqsad")
    hudud = _("Hudud")
    aloqa = _("Aloqa")
    texnologiya = _("Texnologiya")
    button = data['button']
    if button == __("Sherik"):
        xodim = '👨‍💼' + _("Sherik")
    elif button == _("Hodim"):
        xodim = _("🏢 Idora")
        Yosh = _("✍️ Mas'ul")
        Narxi = _("Maosh")
        Kasbi = _("Ish vaqti")
        Maqsad = _("Qo`shimcha")
    await message.answer(f"""{data["button"]}:
{xodim}: {data['full_name']}
🕑 {Yosh}: {data['age']}
📚 {texnologiya}: {data['technologies']}
📞 {aloqa}: {data['phone_number']}
🌐 {hudud}: {data['address']}
💰 {Narxi}: {data['price']}
👨🏻‍💻 {Kasbi}: {data['work_place']}
🔎 {Maqsad}: {data['goal']}""", reply_markup=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=_("Ha "), callback_data="confirm")],
            [InlineKeyboardButton(text=_("Yoq "), callback_data="cancel")]
        ]))


@dp.callback_query(F.data.in_({"confirm", "cancel"}))
async def confirm_or_cancel_handler(call: CallbackQuery, state: FSMContext):
    if call.data == "confirm":
        await call.message.send_copy(chat_id=admin, reply_markup=None)
        await call.message.delete()
        await call.message.answer(_("adminga yuborildi"), reply_markup=menu_btn())
        return
    await call.message.delete()
    await state.clear()
    await call.message.answer(_("Bekor qilindi"), reply_markup=menu_btn())


async def main() -> None:
    i18n = I18n(path="locales", default_locale="uz")
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.update.outer_middleware(FSMI18nMiddleware(i18n))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())