from aiogram import Dispatcher, Bot, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import dotenv_values

from handlers.addFilm import *
from handlers.other import *
from handlers.update_films import *
config = dotenv_values('config.env')
ADMIN_LIST = config['ADMIN_LIST']
db_file = config['DB_FILE']


def register_handlers(dp):
	# Admin handlers
	dp.register_message_handler(admin_function, lambda msg: str(msg.from_user.id) in ADMIN_LIST, commands='admin')
	dp.register_callback_query_handler(add_film_db, lambda call: call.data == 'film_accept')
	dp.register_callback_query_handler(update_film_data, lambda call: call.data.startswith('add'))
	dp.register_message_handler(add_many_films, commands='add')
	dp.register_message_handler(get_preview, state=[FSMFilm.genre, FSMFilm.title, FSMFilm.description, FSMFilm.data,
	                                                FSMFilm.preview], content_types=['photo', 'text'])
	# User handlers
	dp.register_message_handler(start_function, commands='start')
	dp.register_message_handler(get_random_film_by_command, commands='random')
	dp.register_callback_query_handler(get_random_film, lambda call: call.data == 'random')
	dp.register_callback_query_handler(get_film_by_genre, lambda call: call.data == 'genres_search')
	dp.register_message_handler(get_genre, state=FilmGenre.genre)
	dp.register_message_handler(answer_film_by_genre, state=FilmGenre.film)
	dp.register_callback_query_handler(get_popularity_films, lambda call: call.data == 'popularity')

	dp.register_message_handler(film_answer)


TOKEN = config['BOT_TOKEN']
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
register_handlers(dp)


async def start_up(_):
	print('==================Бот запущен==================')


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True, on_startup=start_up)
