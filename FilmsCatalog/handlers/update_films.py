from aiogram.types import Message
from db.db_session import session, Film


async def add_many_films(msg: Message):
	from parser_films import uniq_f
	for film_info in uniq_f:
		m = await msg.answer_photo(film_info['photo_url'])
		film = Film(title=film_info['title'], genre=film_info['genre'], description=film_info['description'],
		            photo_id=m.photo[-1].file_id, rating=0)
		session.add(film)
		session.commit()

	else:
		await msg.answer('Операция выполнена.')
