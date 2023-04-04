
import logging
import markup as mar
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import InputFile
import datetime
vremya = datetime.datetime.now()

str_vremya = str(vremya)

API_TOKEN = '5710585164:AAEaTFvVDGLiOUegwKha3bQG68iD95QjZCU'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Questions(StatesGroup):
    name = State()
    phone = State()
    it = State()
    email = State() # стан для запитання "Ваш email"
    city = State() # стан для запитання "З якого ви міста?"


@dp.message_handler(commands=['start'])
async def start_cmd_handler(message: types.Message):
    """
    Обробник команди /start. Ініціалізує запити.
    """
    await bot.send_message(message.from_user.id, 'Привіт . Хочемо дізнатись про тебе більше, перед тим як надіслати актуальні умови вступу')
    await message.reply("Як тебе звати?")
    await Questions.name.set()


@dp.message_handler(state=Questions.name)
async def process_name(message: types.Message, state: FSMContext):
    """
    Обробник відповіді на запитання "Ваше ПІБ"
    """
    async with state.proxy() as data:
        data['name'] = message.text

    await message.reply("Цікавишся ІТ?🧑‍💻")
    await Questions.it.set()


@dp.message_handler(state=Questions.it)
async def process_phone(message: types.Message, state: FSMContext):
    """
    Обробник відповіді на запитання "Ваш номер телефону"
    """
    async with state.proxy() as data:
        data['it'] = message.text

    await message.reply("З якого ти міста?")
    await Questions.city.set()


@dp.message_handler(state=Questions.city)
async def process_email(message: types.Message, state: FSMContext):
    """
    Обробник відповіді на запитання "Ваш email"
    """
    async with state.proxy() as data:
        data['city'] = message.text

    await message.reply("Щоб завжди отримувати інформацію щодо вступу залиш свій номер")
    await Questions.phone.set()


@dp.message_handler(state=Questions.phone)
async def process_email(message: types.Message, state: FSMContext):
    """
    Обробник відповіді на запитання "Ваш email"
    """
    async with state.proxy() as data:
        data['phone'] = message.text

    await message.reply("Та електронну пошту")
    await Questions.email.set()

@dp.message_handler(state=Questions.email)
async def process_email(message: types.Message, state: FSMContext):
    """
    Обробник відповіді на запитання "З якого ви міста?"
    """
    async with state.proxy() as data:
        data['email'] = message.text
        user_id = message.from_user.username
        user_id1 = message.from_user.full_name

        await bot.send_message(message.from_user.id, 'Оберіть👇', reply_markup=mar.mainMenu)
#        await message.reply_document(open('vstup2023.pdf', 'rb'))
#        await bot.send_message(message.from_user.id,'Лови презентацію')

        # Виводимо відповіді в консоль
        print("************************")
        print(f"Ім'я: {data['name']}")
        print(f"Номер телефону: {data['phone']}")
        print(f"Цікавишся ІТ: {data['it']}")
        print(f"Email: {data['email']}")
        print(f"Місто: {data['city']}")
        print("Нік в тг @", user_id)
        print("Ім'я в тг:",user_id1)
        print(vremya)
        print("************************")
        with open("logs.txt", "a") as file:

            file.write("\n")
            file.write(f" {data['name']}")
            file.write(f"; {data['phone']}")
            file.write(f"; {data['it']}")
            file.write(f"; {data['email']}")
            file.write(f"; {data['city']}")
            file.write("; @")
            file.write(user_id)
            file.write("; ")
            file.write(user_id1)
            file.write("; ")
            file.write(str_vremya)
            file.write(" ")
#            file.write("************************")
            file.close()


    await state.finish() # завершаем процесс вопросов
@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text=='➡️Презентація⬅️':
        await message.reply_document(open('vstup2023.pdf', 'rb'))
    elif message.text=='🌐Канал Вступника':
        await bot.send_message(message.from_user.id,'https://t.me/donNTU_vstup_2023')
    elif message.text=='logsss':
        await message.reply_document(open('logs.txt', 'rb'))






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)