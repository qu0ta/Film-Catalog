import random

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from keyboards import main_menu
from db.db_session import session, Film


class FilmGenre(StatesGroup):
	genre = State()
	film = State()


async def start_function(msg: Message):
	answer = "Введите название фильма или ID\n"
	"Также вы можете выбрать способ сортировки из представленных ниже"
	await msg.answer(answer, reply_markup=main_menu)


async def film_answer(msg: Message):
	response = msg.text
	if not response.isnumeric():
		query = session.query(Film).filter(Film.title.contains(response)).first()
		if query:
			await msg.answer_photo(photo=query.photo_id,
			                       caption=f"""<b>{query.title}</b>\nЖанр: <b>{query.genre}</b>\nОписание: <b>{query.description}</b>""",
			                       parse_mode='HTML')
			query.rating += 1
			session.commit()
		else:
			await msg.answer('Фильм не найден. Попробуйте еще раз.')
	else:
		response = int(response)
		query = session.query(Film).filter_by(id=response).one_or_none()

		await msg.answer_photo(photo=query.photo_id,
		                       caption=f"""<b>{query.title}</b>\nЖанр: <b>{query.genre}</b>\nОписание: <b>{query.description}</b>""",
		                       parse_mode='HTML') \
			if query else \
			await msg.answer('Фильм не найден. Попробуйте еще раз.')


async def get_random_film(call: CallbackQuery):
	_films = session.query(Film).all()
	if not _films:
		await call.message.answer('Фильмов пока нет.')
		return
	random_id = random.randint(1, len(_films))
	film = session.query(Film).filter(Film.id == random_id).one()

	await call.message.answer_photo(
		photo=film.photo_id,
		caption=f"<b>{film.title}</b>\n<b>Жанр:</b> {film.genre}\n<b>Описание</b>: {film.description}",
		parse_mode='HTML'
	)


async def get_random_film_by_command(message: Message):
	_films = session.query(Film).all()
	if not _films:
		await message.answer('Фильмов пока нет.')
		return
	random_id = random.randint(1, len(_films))
	film = session.query(Film).filter(Film.id == random_id).one()

	await message.answer_photo(
		photo=film.photo_id,
		caption=f"<b>{film.title}</b>\n<b>Жанр:</b> {film.genre}\n<b>Описание</b>: {film.description}",
		parse_mode='HTML'
	)


async def get_film_by_genre(call: CallbackQuery):
	genres = ['аниме', 'биографический', 'боевик', 'вестерн', 'военный', 'детектив', 'детский', 'документальный',
	          'драма', 'исторический', 'комедия', 'концерт', 'короткометражный', 'криминал', 'мелодрама',
	          'мистика', 'музыка', 'мультфильм', 'мюзикл', 'научный', 'приключения', 'реалити-шоу', 'семейный',
	          'спорт', 'ток-шоу', 'триллер', 'ужасы', 'фантастика', 'фэнтези', 'эротика']
	await call.message.answer(f'Введите жанр из списка ниже.\n\n{", ".join(genres)}')
	await FilmGenre.first()


async def get_genre(msg: Message, state: FSMContext):
	genre = msg.text
	films_by_genre = session.query(Film).filter(Film.genre.contains(genre.lower())).all()
	films_by_genre = set(map(lambda film: film.title, films_by_genre))
	if not films_by_genre:
		await msg.answer('Фильмы такого жанра не найдены')
		await state.reset_state()
		return
	await msg.answer(f'Введите название фильма или его начало из списка ниже.\n\n{", ".join(films_by_genre)}')
	await FilmGenre.next()


async def answer_film_by_genre(msg: Message, state: FSMContext):
	film_text = msg.text
	film = session.query(Film).filter(Film.title.contains(film_text.title())).first()
	if film:
		await msg.answer_photo(photo=film.photo_id,
		                       caption=f"""<b>{film.title}</b>\nЖанр: <b>{film.genre}</b>\nОписание: <b>{film.description}</b>""",
		                       parse_mode='HTML')
		film.rating += 1
		session.commit()
	else:
		await msg.answer('Фильм не найден. Попробуйте еще раз.')

	await state.reset_state()


async def get_popularity_films(call: CallbackQuery):
	top_5_films = session.query(Film).order_by(Film.rating)[::-1][:5]
	top_5_films = list(map(lambda film: film.title, top_5_films))
	await call.message.answer('Топ-5 популярных фильмов:\n\n{}'.format("\n".join(top_5_films)))
