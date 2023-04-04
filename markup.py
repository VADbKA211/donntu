from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

#----main-------
buttonmain= KeyboardButton('Головне меню')



#------menu--------

b1 = KeyboardButton('➡️Презентація⬅️')
b2 = KeyboardButton('🌐Канал Вступника')


mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(b1, b2)


