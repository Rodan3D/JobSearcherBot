from models import KeywordStat, session, ExcludedWordStat


# Функция для добавления ключевых слов и их статистики
def add_keyword_stat(name, count):
    keyword = session.query(KeywordStat).filter_by(name=name).first()
    if keyword:
        # Если ключевое слово уже существует, обновляем статистику
        keyword.count += count
    else:
        # Если ключевое слово не существует, создаем новую запись
        keyword = KeywordStat(name=name, count=count)
        session.add(keyword)
    session.commit()


# Функция для добавления слов-исключений и их статистики
def add_excluded_word_stat(name, count):
    excluded_word = session.query(ExcludedWordStat).filter_by(name=name).first()
    if excluded_word:
        # Если слово-исключение уже существует, обновляем статистику
        excluded_word.count += count
    else:
        # Если слово-исключение не существует, создаем новую запись
        excluded_word = ExcludedWordStat(name=name, count=count)
        session.add(excluded_word)
    session.commit()


def get_popular_keywords_from_database():
    # Извлеките популярные ключевые слова из базы данных
    keywords = session.query(KeywordStat).order_by(KeywordStat.count.desc()).limit(5)
    return [keyword.name for keyword in keywords]


def get_popular_excluded_words_from_database():
    # Извлеките популярные слова-исключения из базы данных
    excluded_words = session.query(ExcludedWordStat).order_by(ExcludedWordStat.count.desc()).limit(5)
    return [word.name for word in excluded_words]
