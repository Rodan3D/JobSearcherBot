"""
Модуль keyword_stats предоставляет определение моделей и настройку базы данных SQLite для хранения статистики ключевых слов и слов-исключений.

"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Создаем объект базы данных SQLite
engine = create_engine("sqlite:///keyword_stats.db")

# Создаем базовый класс для объявления моделей
Base = declarative_base()


# Определяем модель для таблицы
class KeywordStat(Base):
    """
    Модель для хранения статистики ключевых слов в базе данных.

    Attributes:
        id (int): Уникальный идентификатор записи.
        name (str): Уникальное ключевое слово.
        count (int): Количество вхождений ключевого слова.
    """

    __tablename__ = "keyword_stats"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Уникальное ключевое слово
    count = Column(Integer)


# Определяем модель для таблицы слов-исключений
class ExcludedWordStat(Base):
    """
    Модель для хранения статистики слов-исключений в базе данных.

    Attributes:
       id (int): Уникальный идентификатор записи.
       name (str): Уникальное слово-исключение.
       count (int): Количество вхождений слова-исключения.
    """

    __tablename__ = "excluded_word_stats"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # Уникальное слово-исключение
    count = Column(Integer)


# Создаем таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем сессию для работы с базой данных
Session = sessionmaker(bind=engine)
session = Session()
