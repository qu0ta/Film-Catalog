import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import Integer, Column, String, Text
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()
conn_str = f'sqlite:///data/films.db?check_same_thread=True'

engine = create_engine(conn_str, echo=True, pool_pre_ping=True)


class Film(SqlAlchemyBase):
	__tablename__ = 'films'

	id = Column(Integer, primary_key=True)
	title = Column(Text(200))
	genre = Column(Text(200))
	description = Column(Text(1000))
	photo_id = Column(Text(200))
	rating = Column(Integer)

	def __repr__(self):
		return f"<Film(Title: {self.title}, Genre: {self.genre}, Description: {self.description})>"


SqlAlchemyBase.metadata.create_all(engine)
session = Session(engine, autocommit=False)
