"""
Модуль, представляющий собой набор функций для работы с базой данных,
включая добавление статистики для ключевых слов и слов-исключений,
а также получение популярных ключевых слов и слов-исключений из базы данных

"""
from typing import List
from logger import logger
from models import ExcludedWordStat, KeywordStat, session


class DatabaseManager:
    @staticmethod
    @logger.catch
    def add_keyword_stat(name: str, count: int) -> None:
        """
        Добавляет статистику для ключевых слов в базу данных.

        Args:
            name: Строка с ключевым словом.
            count: Количество вхождений ключевого слова.
        """
        keyword = session.query(KeywordStat).filter_by(name=name).first()
        if keyword:
            keyword.count += count
        else:
            keyword = KeywordStat(name=name, count=count)
            session.add(keyword)
        session.commit()

    @staticmethod
    @logger.catch
    def add_excluded_word_stat(name: str, count: int) -> None:
        """
        Добавляет статистику для слов-исключений в базу данных.

        Args:
            name: Строка с словом-исключением.
            count: Количество вхождений слова-исключения.
        """
        excluded_word = session.query(
            ExcludedWordStat).filter_by(name=name).first()
        if excluded_word:
            excluded_word.count += count
        else:
            excluded_word = ExcludedWordStat(name=name, count=count)
            session.add(excluded_word)
        session.commit()

    @staticmethod
    @logger.catch
    def get_popular_keywords_from_database() -> List[str]:
        """
        Извлекает популярные ключевые слова из базы данных.

        Returns:
            Список популярных ключевых слов.
        """
        keywords = session.query(KeywordStat).order_by(
            KeywordStat.count.desc()).limit(5)
        return [keyword.name for keyword in keywords]

    @staticmethod
    @logger.catch
    def get_popular_excluded_words_from_database() -> List[str]:
        """
        Извлекает популярные слова-исключения из базы данных.

        Returns:
            Список популярных слов-исключений.
        """
        excluded_words = session.query(ExcludedWordStat).order_by(
            ExcludedWordStat.count.desc()).limit(5)
        return [word.name for word in excluded_words]


if __name__ == '__main__':
    database_manager = DatabaseManager
