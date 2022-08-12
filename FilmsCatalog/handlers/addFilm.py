from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import CantParseEntities

from keyboards import update_data

from db.db_session import session, Film


class FSMFilm(StatesGroup):
	preview = State()
	data = State()
	title = State()
	genre = State()
	description = State()


async def admin_function(msg: Message):
	answer = "Отправьте фото для добавления фильма\nДля отмены: /cancel"
	await msg.answer(answer)
	await FSMFilm.preview.set()


async def get_preview(msg: Message, state: FSMContext):
	if msg.photo:
		await state.update_data(data={'preview': msg.photo[-1].file_id})
		await msg.answer('Фото добавлено.')
		data = await state.get_data()
		title = data.get('title', 'Не выбрано')
		genre = data.get('genre', 'Не выбрано')
		description = data.get('description', 'Не выбрано')
		message_to_answer = (f"<b>{title}</b>\n"
		                     f"<b>Жанр:</b> {genre}\n"
		                     f"<b>Описание:</b> {description}")
		await msg.answer_photo(data['preview'], caption=message_to_answer, parse_mode='HTML', reply_markup=update_data)
		await state.reset_state(with_data=False)
	else:
		if msg.text == '/cancel':
			await state.reset_state()
			await msg.answer('Действие отменено.')
			return
		for f_type in ('title', 'genre', 'description'):
			if f_type in await state.get_state():
				await state.update_data({f_type: msg.text.capitalize()})
				break
		data = await state.get_data()
		title = data.get('title', 'Не выбрано')
		genre = data.get('genre', 'Не выбрано')
		description = data.get('description', 'Не выбрано')
		message_to_answer = (f"<b>{title}</b>\n"
		                     f"<b>Жанр:</b> {genre}\n"
		                     f"<b>Описание:</b> {description}")
		try:
			await msg.answer_photo(data['preview'], caption=message_to_answer, parse_mode='HTML',
			                       reply_markup=update_data)
			await state.reset_state(with_data=False)
		except CantParseEntities:
			await msg.answer('Недопустимые символы. Попробуйте еще раз.')
			await msg.answer_photo(data['preview'], caption=message_to_answer, parse_mode='HTML',
			                       reply_markup=update_data)
			await state.reset_state(with_data=False)


async def update_film_data(call: CallbackQuery, state: FSMContext):
	data = await state.get_data()
	calldata = call.data.replace('add_', '')
	if calldata == 'title':
		await call.message.answer(
			f'Введите новое название фильма. Текущее название: {data.get("title", "Не выбрано")}')
		await FSMFilm.title.set()
	elif calldata == 'genre':
		await call.message.answer(
			f'Введите новый жанр фильма. Текущий жанр: {data.get("genre", "Не выбрано")}')
		await FSMFilm.genre.set()
	elif calldata == 'description':
		await call.message.answer(
			f'Введите новое описание фильма. Текущее описание: {data.get("description", "Не выбрано")}')
		await FSMFilm.description.set()


async def add_film_db(call: CallbackQuery, state: FSMContext):
	data = await state.get_data()
	title = data.get('title', 'Не выбрано')
	genre = data.get('genre', 'Не выбрано')
	description = data.get('description', 'Не выбрано')
	photo_id = data.get('preview')
	film = Film(title=title, genre=genre, description=description, photo_id=photo_id)
	session.add(film)
	
	await call.message.answer('Фильм успешно добавлен.')
	await state.reset_state()
