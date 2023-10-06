import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import ExcludedWordStat, KeywordStat

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)


class TestKeywordStatsDatabase(unittest.TestCase):
    def setUp(self):
        KeywordStat.metadata.create_all(engine)
        ExcludedWordStat.metadata.create_all(engine)
        self.session = Session()

    def tearDown(self):
        KeywordStat.metadata.drop_all(engine)
        ExcludedWordStat.metadata.drop_all(engine)
        self.session.close()

    def test_add_keyword_stat(self):
        keyword = KeywordStat(name='test_keyword', count=3)
        self.session.add(keyword)
        self.session.commit()

        keyword_from_db = (
            self.session.query(KeywordStat).filter_by(name='test_keyword').
            first()
        )
        self.assertIsNotNone(keyword_from_db)
        self.assertEqual(keyword_from_db.name, 'test_keyword')
        self.assertEqual(keyword_from_db.count, 3)

    def test_add_excluded_word_stat(self):
        excluded_word = ExcludedWordStat(name='test_excluded_word', count=2)
        self.session.add(excluded_word)
        self.session.commit()

        excluded_word_from_db = (
            self.session.query(ExcludedWordStat)
            .filter_by(name='test_excluded_word')
            .first()
        )
        self.assertIsNotNone(excluded_word_from_db)
        self.assertEqual(excluded_word_from_db.name, 'test_excluded_word')
        self.assertEqual(excluded_word_from_db.count, 2)


if __name__ == '__main__':
    unittest.main()
