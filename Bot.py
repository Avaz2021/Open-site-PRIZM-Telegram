# Bot.py

# Импортируем нужные библиотеки
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.markdown import hlink
from BotToken import bot_token
import importlib
import curs, curs_usd
import sqlite3
from datetime import datetime

# Регистрируем бота
bot = Bot(token = bot_token)
db = Dispatcher(bot)


# Создание клавиатуры
keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)

# Первая линия кнопок(Кошелёк, Paramining, Офиц. сайт)
kb_wallet = types.KeyboardButton("Кошелёк")
kb_paramining = types.KeyboardButton("Paramining")
kb_official = types.KeyboardButton("Офиц. сайт")

# Вторая линия кнопок(Telegram канал, Paratax, Блокчейн)
kb_telegram = types.KeyboardButton("Telegram канал")
kb_paratax = types.KeyboardButton("Paratax")
kb_blockchain = types.KeyboardButton("Блокчейн")

# Третья линия кнопок(GitHub, Структура, BitTeam)
kb_github = types.KeyboardButton("GitHub")
kb_structure = types.KeyboardButton("Структура")
kb_bitteam = types.KeyboardButton("BitTeam")

# Четвёртая линия кнопок(Курс)
kb_curs = types.KeyboardButton("Курс")

# Добавление кнопок на клавиатуру
keyboard.add(kb_wallet).insert(kb_paramining).insert(kb_official).add(
			kb_telegram).insert(kb_paratax).insert(kb_blockchain).add(
			kb_github).insert(kb_structure).insert(kb_bitteam).add(
			kb_curs)


# Приветствие пользователя
@db.message_handler(commands = ["start"])
async def welcome(message: types.Message):
	await message.answer(f"Приветсвую вас, {message.from_user.first_name}!\nЯ могу прислать вам 10 ссылок, связанные с криптовалютой PRIZM.\nДайте мне одну из десяти комманд👇", 
						reply_markup = keyboard)

	try:
		connect = sqlite3.connect("OSP users.db")
		db = connect.cursor()
		db.execute(f'INSERT INTO Пользователи VALUES("{message.from_user.id}", "@{message.from_user.username}")')
		connect.commit()
		connect.close()
		print(f"@{message.from_user.username} запустил бота")
	
	except sqlite3.IntegrityError:
		pass


# Работа бота
@db.message_handler()
async def send_message(message: types.Message):
	if message.text == "Кошелёк":
		wallet = hlink("Официальный кошелёк", "https://wallet.prizm.space/index.html")
		await message.answer(f"{wallet} PRIZM", 
							parse_mode = "HTML")

	elif message.text == "Paramining":
		paramining = hlink("Paramining", "https://tool-prizm.space/")
		await message.answer(f"Узнать свой {paramining}", 
							parse_mode = "HTML")

	elif message.text == "Офиц. сайт":
		official_site = hlink("Официальный сайт", "https://pzm.space/")
		await message.answer(f"{official_site} PRIZM", 
							parse_mode = "HTML", 
							disable_web_page_preview = True)

	elif message.text == "Telegram канал":
		await message.answer("@prizmdev")

	elif message.text == "Paratax":
		paratax = hlink("Paratax", "https://www.prizm.network/services/real-paratax")
		await message.answer(f"Узнать свой реальный {paratax}", 
							parse_mode = "HTML",
							disable_web_page_preview = True)

	elif message.text == "Блокчейн":
		blockchain =  hlink("Блокчейн", "https://prizmexplorer.com/")
		await message.answer(f"{blockchain} PRIZM", 
							parse_mode = "HTML",
							disable_web_page_preview = True)

	elif message.text == "GitHub":
		github = hlink("GitHub", "https://github.com/prizmspace/PrizmCore")
		await message.answer(f"{github} PRIZM", 
							parse_mode = "HTML",
							disable_web_page_preview = True)

	elif message.text == "Структура":
		structure = hlink("структуру", "https://prizmbank.ru/blockchain/prizm-struktura.php")
		await message.answer(f"Узнать свою {structure}", 
							parse_mode = "HTML",
							disable_web_page_preview = True)

	elif message.text == "BitTeam":
		bitteam = hlink("BitTeam", "https://p2p.bit.team/ru/buy/pzm")
		await message.answer(f"Купить PRIZM на {bitteam}", 
							parse_mode = "HTML",
							disable_web_page_preview = True)

	elif message.text == "Курс":
		importlib.reload(curs)
		importlib.reload(curs_usd)
		coinmc = hlink("CoinMarketCap", "https://coinmarketcap.com/ru/currencies/prizm/")
		await message.answer(f"Курс PRIZM по {coinmc}\n\nPZM/RUB: ₽{curs.pzm_curs}\nPZM/USD: ${curs_usd.pzm_curs}", 
							parse_mode = "HTML", 
							disable_web_page_preview = True)

	else:
		await message.answer("Команда не найдена", reply_markup = keyboard)


# Запуск бота
time_now = datetime.today()
print(f"[{str(time_now)[:19]}]: Бот успешно запущен")

executor.start_polling(db)
