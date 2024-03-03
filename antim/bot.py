import os, telebot, tempfile, cv2, win10toast
from PIL import ImageGrab

API_TOKEN = '...' # вместо точек апи бота
ALLOWED_USER = [] # в скобках написать свой айди
bot = telebot.TeleBot(API_TOKEN)

def photo(id):
    path0 = tempfile.gettempdir() + 'photo.png'
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    ret, frame = cap.read()
    frame = cv2.convertScaleAbs(frame, beta=50)
    cv2.imwrite(path0, frame)
    cap.release()
    bot.send_photo(id, open(path0, 'rb'))

bot.send_message(ALLOWED_USER[0], 'Компьютер работает')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Сделать скриншот")
    markup.add("Выключить")
    markup.add("Перезагрузить")
    markup.add("Вебка")
    markup.add("Уведомление")
    bot.send_message(message.chat.id, 'Доброго времени суток! :3 👋', reply_markup=markup)

@bot.message_handler(regexp='выключить')
def echo_message(message):
    user_id = message.from_user.id
    if user_id in ALLOWED_USER:
        bot.send_message(message.chat.id, 'Выключаю...')
        os.system("shutdown -s -t 0")
        pass
    else:
        bot.send_message(message.chat.id, 'У вас нет прав! Если вы хотите такого же бота пишите @rikwf')

@bot.message_handler(regexp='перезагрузить')
def echo_message(message):
    user_id = message.from_user.id
    if user_id in ALLOWED_USER:
        bot.send_message(message.chat.id, 'Перезапускаю...')
        os.system("shutdown -r -t 0")
        pass
    else:
        bot.send_message(message.chat.id, 'У вас нет прав! Если вы хотите такого же бота пишите @rikwf')

@bot.message_handler(regexp='сделать скриншот')
def echo_message(message):
    user_id = message.from_user.id
    if user_id in ALLOWED_USER:
        path = tempfile.gettempdir() + 'screenshot.png'
        screenshot = ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=True)
        screenshot.save(path, 'PNG')
        bot.send_photo(message.chat.id, open(path, 'rb'))
        pass
    else:
        bot.send_message(message.chat.id, 'У вас нет прав! Если вы хотите такого же бота пишите @rikwf')

@bot.message_handler(regexp='help')
def echo_message(message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_USER:
        bot.send_message(message.chat.id, 'Пользователь сейчас online! Если вы хотите такого же бота пишите @rikwf')
    else:
        bot.send_message(message.chat.id, 'bot is online')

@bot.message_handler(regexp='вебка')
def echo_message(message):
    user_id = message.from_user.id
    if user_id in ALLOWED_USER:
        photo(message.chat.id)
        pass
    else:
        bot.send_message(message.chat.id, 'У вас нет прав! Если вы хотите такого же бота пишите @rikwf')

@bot.message_handler(regexp='уведомление')
def start_notification(message):
   user_id = message.from_user.id
   if user_id in ALLOWED_USER:
       bot.send_message(message.chat.id, 'Введите текст уведомления:')
       bot.register_next_step_handler(message, get_notification_text)
   else:
       bot.send_message(message.chat.id, 'У вас нет прав! Если вы хотите такого же бота пишите @rikwf')

def get_notification_text(message):
    user_id = message.from_user.id
    if user_id in ALLOWED_USER:
        msg = message.text
        bot.send_message(message.chat.id, f'Вы указали текст уведомления: {msg}')
        bot.send_message(message.chat.id, 'Вы уверены, что хотите отправить это уведомление?')
        bot.register_next_step_handler(message, send_notification, msg)
    else:
        bot.send_message(message.chat.id, 'У вас нет прав! Если вы хотите такого же бота пишите @rikwf')

def send_notification(message, msgu):
    user_id = message.from_user.id
    if user_id in ALLOWED_USER:
        if message.text.lower() == 'да':
            toast = win10toast.ToastNotifier()
            toast.show_toast(title='Владелец компьютера говорит:', msg=msgu, duration=10)
            bot.send_message(message.chat.id, 'Уведомление отправлено.')
        elif message.text.lower() == 'нет':
            bot.send_message(message.chat.id, 'Уведомление не отправлено.')
        else:
            bot.send_message(message.chat.id, 'Неверный ответ. Введите "да" или "нет".')
            bot.register_next_step_handler(message, send_notification, msgu)
    else:
        bot.send_message(message.chat.id, 'У вас нет прав! Если вы хотите такого же бота пишите @rikwf')    

bot.infinity_polling()
