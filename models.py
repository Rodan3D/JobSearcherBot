from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Создаем объект базы данных SQLite
engine = create_engine('sqlite:///keyword_stats.db')

# Создаем базовый класс для объявления моделей
Base = declarative_base()


# Определяем модель для таблицы
class KeywordStat(Base):
    __tablename__ = 'keyword_stats'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Уникальное ключевое слово
    count = Column(Integer)


# Определяем модель для таблицы слов-исключений
class ExcludedWordStat(Base):
    __tablename__ = 'excluded_word_stats'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Уникальное слово-исключение
    count = Column(Integer)


# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()
