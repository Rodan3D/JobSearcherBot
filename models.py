"""
Модуль models предоставляет определение моделей и настройку
базы данных SQLite для хранения статистики ключевых слов и слов-исключений.
"""
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///keyword_stats.db')
Base = declarative_base()


class BaseStat(Base):
    """
    Базовый класс для хранения статистики в базе данных.

    Args:
        id (int): Уникальный идентификатор записи.
        name (str): Уникальное ключевое слово или слово-исключение.
        count (int): Количество вхождений ключевого слова или слова-исключения.
    """

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    count = Column(Integer)


class KeywordStat(BaseStat):
    """
    Модель для хранения статистики ключевых слов в базе данных.
    """
    __tablename__ = 'keyword_stats'


class ExcludedWordStat(BaseStat):
    """
    Модель для хранения статистики слов-исключений в базе данных.
    """
    __tablename__ = 'excluded_word_stats'


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
