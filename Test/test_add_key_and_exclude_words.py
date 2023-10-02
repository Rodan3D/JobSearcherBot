import unittest
from unittest.mock import patch
from add_key_and_exclude_words import (
    add_keyword_stat,
    add_excluded_word_stat,
    get_popular_keywords_from_database,
    get_popular_excluded_words_from_database,
)

from models import KeywordStat, ExcludedWordStat


class TestDatabaseFunctions(unittest.TestCase):

    @patch('add_key_and_exclude_words.session')
    def test_add_keyword_stat(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        add_keyword_stat("test_keyword", 3)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch('add_key_and_exclude_words.session')
    def test_add_excluded_word_stat(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        add_excluded_word_stat("test_excluded_word", 2)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch('add_key_and_exclude_words.session')
    def test_get_popular_keywords_from_database(self, mock_session):
        mock_query = mock_session.query.return_value
        mock_query.order_by.return_value.limit.return_value = [
            KeywordStat(name="keyword1", count=10),
            KeywordStat(name="keyword2", count=8),
        ]
        popular_keywords = get_popular_keywords_from_database()
        self.assertEqual(popular_keywords, ["keyword1", "keyword2"])

    @patch('add_key_and_exclude_words.session')
    def test_get_popular_excluded_words_from_database(self, mock_session):
        mock_query = mock_session.query.return_value
        mock_query.order_by.return_value.limit.return_value = [
            ExcludedWordStat(name="excluded_word1", count=5),
            ExcludedWordStat(name="excluded_word2", count=4),
        ]
        popular_excluded_words = get_popular_excluded_words_from_database()
        self.assertEqual(popular_excluded_words, ["excluded_word1", "excluded_word2"])

    @patch('add_key_and_exclude_words.session')
    def test_add_keyword_stat_existing_keyword(self, mock_session):
        mock_keyword = KeywordStat(name="existing_keyword", count=5)
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_keyword
        add_keyword_stat("existing_keyword", 3)
        self.assertEqual(mock_keyword.count, 8)
        mock_session.add.assert_not_called()
        mock_session.commit.assert_called_once()

    @patch('add_key_and_exclude_words.session')
    def test_add_excluded_word_stat_existing_word(self, mock_session):
        mock_word = ExcludedWordStat(name="existing_word", count=3)
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_word
        add_excluded_word_stat("existing_word", 2)
        self.assertEqual(mock_word.count, 5)
        mock_session.add.assert_not_called()
        mock_session.commit.assert_called_once()

    @patch('add_key_and_exclude_words.session')
    def test_get_popular_keywords_from_empty_database(self, mock_session):
        mock_query = mock_session.query.return_value
        mock_query.order_by.return_value.limit.return_value = []
        popular_keywords = get_popular_keywords_from_database()
        self.assertEqual(popular_keywords, [])

    @patch('add_key_and_exclude_words.session')
    def test_get_popular_excluded_words_from_empty_database(self, mock_session):
        mock_query = mock_session.query.return_value
        mock_query.order_by.return_value.limit.return_value = []
        popular_excluded_words = get_popular_excluded_words_from_database()
        self.assertEqual(popular_excluded_words, [])

    @patch('add_key_and_exclude_words.session')
    def test_add_keyword_stat_new_keyword(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        add_keyword_stat("new_keyword", 4)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @patch('add_key_and_exclude_words.session')
    def test_add_excluded_word_stat_new_word(self, mock_session):
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        add_excluded_word_stat("new_word", 3)
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()


if __name__ == '__main__':
    unittest.main()
