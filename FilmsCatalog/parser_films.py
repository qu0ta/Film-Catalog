import requests
from bs4 import BeautifulSoup
from db.db_session import session, Film


def get_unique_photos(films_list: list[dict]):
	return [film for film in films_list
	        if film['title'] not in
	        [q_film.title for q_film in set(session.query(Film).all())]]


films = []
for i in range(1, 10):

	url = f"https://www.kinoafisha.info/rating/movies/?page={i}"
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	film_cards = soup.find_all('div', class_='movieItem')
	_all_films = set(map(lambda f: f.title, session.query(Film).all()))
	for film_card in film_cards:
		info = film_card.find('div', class_='movieItem_info')
		title = info.find('a', class_='movieItem_title').text.replace("'", '')
		if title in _all_films:
			continue
		genre = info.find('div', class_='movieItem_details').find('span', class_="movieItem_genres").text.replace("'",
		                                                                                                          '')
		img = film_card.find('a').find('picture', class_='picture').find('source', {'type': 'image/jpeg'})['srcset']

		req = requests.get(film_card.find('a')['href'])
		new_soup = BeautifulSoup(req.text, 'html.parser')
		try:
			description = new_soup.find('div', class_="visualEditorInsertion filmDesc_editor more_content").find(
				'p').text.replace("'", '')
		except AttributeError:
			continue

		film = {
			'title': title, 'genre': genre, 'photo_url': img, 'description': description
		}
		films.append(film)
		print(f'Фильм №{film_cards.index(film_card) + 1} {film["title"]} обработан')
uniq_f = get_unique_photos(films)
