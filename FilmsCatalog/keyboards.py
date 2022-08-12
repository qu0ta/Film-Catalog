from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
kb_arr = [('Случайный фильм', 'random'), ('Поиск по жанрам', 'genres_search'),
          ('Популярные фильмы', 'popularity')]
main_menu = InlineKeyboardMarkup(row_width=1)
main_menu.add(
	*[InlineKeyboardButton(text, callback_data=cd) for text, cd in kb_arr]
)
add_menu_kb = InlineKeyboardMarkup(row_width=2)
add_menu_kb.add(
	InlineKeyboardButton('Добавить', callback_data='add_film'),
	InlineKeyboardButton('Отменить', callback_data='deny_film')
)
update_data = InlineKeyboardMarkup(row_width=1)
update_data.add(
	InlineKeyboardButton('Добавить название', callback_data='add_title'),
	InlineKeyboardButton('Добавить жанр', callback_data='add_genre'),
	InlineKeyboardButton('Добавить описание', callback_data='add_description'),
	InlineKeyboardButton('Добавить фильм', callback_data='film_accept')
)