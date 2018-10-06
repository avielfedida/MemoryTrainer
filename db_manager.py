import sqlite3
import time
from collections import defaultdict
from itertools import groupby


class DbManager:
    conn = None

    def __init__(self):
        self.conn = self.connect()
        self.construct()

    def construct(self):
        with self.conn:
            c = self.conn.cursor()
            c.execute("""
            CREATE TABLE IF NOT EXISTS Terms 
            (category text, term text, answer text, appeared integer, wrong integer, insert_time text)
            """)
            c.execute("""
            CREATE TABLE IF NOT EXISTS Statistics 
            (sum_of_appeared integer, sum_of_wrongs integer, num_of_terms integer, for_date text)
            """)

    def connect(self):
        return sqlite3.connect("trainer.db")

    def get_stats(self, days):
        res = self.conn.cursor().execute(
            """
            SELECT (CAST(sum_of_wrongs AS FLOAT) / sum_of_appeared) AS wrong_rate_day_sum, strftime('%d/%m', for_date) as date FROM Statistics ORDER BY for_date DESC LIMIT ?

            """,
            (days,)).fetchall()
        if len(res) > 0:
            ret = []
            for obj in res:
                wrong_rate = obj[0]
                ret.append({'date': obj[1], 'knowledge_rate_percentage': (1-wrong_rate) * 100})
            return ret
        return []

    def search_term(self, search_term, category):
        search_term = str.lower(search_term)
        category = str.lower(category)
        return self.conn.cursor().execute(
            """
            SELECT term FROM Terms WHERE term LIKE ? AND category = ?
            """,
            ('%' + search_term + '%', category,)).fetchall()

    @staticmethod
    def new_tick(conn, appeared_sum, wrong_sum, terms_count):
        with conn:
            c = conn.cursor()
            c.execute("""
            INSERT INTO Statistics (sum_of_appeared, sum_of_wrongs, num_of_terms, for_date) VALUES 
            (?, ?, ?, datetime('now', 'localtime'))
            """, (appeared_sum, wrong_sum, terms_count))

    def statistic_tick(self):
        # First fetch data
        data = self.conn.cursor().execute(
            """
            SELECT SUM(appeared) AS apsum, SUM(wrong) AS wsum, COUNT(rowid) AS tc FROM Terms
            """).fetchone()
        if data is not None:
            appeared_sum, wrong_sum, terms_count = data[0], data[1], data[2]
            if terms_count == 0:
                return

            last_date = self.conn.cursor().execute("""
            SELECT rowid, strftime('%d/%m/%Y', for_date) as date FROM Statistics ORDER BY for_date DESC LIMIT 1
            """).fetchone()
            if last_date is None:
                DbManager.new_tick(self.conn, appeared_sum, wrong_sum, terms_count)
                return

            rowid, date = last_date[0], last_date[1]
            today = time.strftime("%d/%m/%Y")
            # Tick was already taken place
            if date == today:
                with self.conn:
                    c = self.conn.cursor()
                    c.execute("""
                    UPDATE Statistics SET sum_of_appeared = ?, sum_of_wrongs = ?, num_of_terms = ?, for_date = datetime('now', 'localtime') WHERE rowid = ? 
                    """, (appeared_sum, wrong_sum, terms_count, rowid))
            else:
                DbManager.new_tick(self.conn, appeared_sum, wrong_sum, terms_count)

    def terms_list(self, search_term, category):
        search_term = str.lower(search_term)
        category = str.lower(category)
        return self.conn.cursor().execute(
            """
            SELECT term FROM Terms WHERE term IS NOT ? AND term LIKE ? AND category = ?
            """,
            (search_term, '%' + search_term + '%', category,)).fetchall()

    def update_term(self, rowid, category, term, answer, reset_stats=False):
        category = str.lower(category)
        term = str.lower(term)
        with self.conn:
            c = self.conn.cursor()
            if reset_stats:
                c.execute("""
                UPDATE Terms SET term = ?, category = ?, answer = ?, appeared = 2, wrong = 1 WHERE rowid = ?""",
                          (term, category, answer, rowid,))
            else:
                c.execute("""
                UPDATE Terms SET term = ?, category = ?, answer = ? WHERE rowid = ?""",
                          (term, category, answer, rowid,))
        return True

    def get_term(self, category, term):
        category = str.lower(category)
        term = str.lower(term)
        c = self.conn.cursor()
        c.execute("SELECT rowid, category, term, answer FROM Terms WHERE term = ? AND category = ?", (term, category,))
        res = c.fetchone()
        if res is not None:
            res = {
                'rowid': res[0],
                'category': res[1],
                'term': res[2],
                'answer': res[3]
            }
        return res

    # Assumption is that validation done somewhere else.
    def insert(self, category, term, answer):
        category = str.lower(category)
        term = str.lower(term)

        term_object = self.get_term(category, term)
        if term_object is not None:
            return self.update_term(term_object.get('rowid'), category, term, answer)

        with self.conn:
            c = self.conn.cursor()
            c.execute("""
            INSERT INTO Terms (category, term, answer, appeared, wrong, insert_time) VALUES 
            (?, ?, ?, ?, ?, datetime('now', 'localtime'))
            """, (category, term, answer, 2, 1))
        return True

    def update_wrong_and_appeared(self, category, term):
        category = str.lower(category)
        term = str.lower(term)
        with self.conn:
            c = self.conn.cursor()
            c.execute("""
            UPDATE Terms SET wrong =  wrong + 1, appeared = appeared + 1 WHERE term = ? AND category = ?""",
                      (term, category,))
        return True

    def get_categories_list(self):
        return self.conn.cursor().execute(
            """
            SELECT DISTINCT category FROM Terms
            """).fetchall()

    def delete_term(self, term, category):
        category = str.lower(category)
        term = str.lower(term)
        with self.conn:
            c = self.conn.cursor()
            c.execute("""
            DELETE FROM Terms WHERE term = ? AND category = ?
            """, (term, category,))
        return True

    def search_category(self, category):
        category = str.lower(category)
        if len(category) == 0:
            return self.get_categories_list()
        return self.conn.cursor().execute(
            """
            SELECT DISTINCT category FROM Terms WHERE category LIKE ?
            """, ('%' + category + '%',)).fetchall()

    def get_most_common_category(self):
        return self.conn.cursor().execute(
            """
            SELECT DISTINCT category, COUNT(rowid) AS c FROM Terms GROUP BY category ORDER BY c DESC LIMIT 1
            """).fetchone()

    def get_terms(self, category, how_many=1):
        res = self.conn.cursor().execute(
            """
            SELECT term, category, answer, appeared, wrong, CAST(wrong AS FLOAT) / appeared AS ratio FROM Terms WHERE category = ? ORDER BY ratio DESC LIMIT ?
            """,
            (category, how_many,)).fetchall()
        if len(res) > 0:
            return [{'term': obj[0], 'category': obj[1], 'answer': obj[2], 'appeared': obj[3], 'wrong': obj[4],
                     'ratio': obj[5]} for obj in res]
        return []

    def update_appeared(self, category, term):
        category = str.lower(category)
        term = str.lower(term)
        with self.conn:
            c = self.conn.cursor()
            c.execute("""
            UPDATE Terms SET appeared = appeared + 1 WHERE term = ? AND category = ?""",
                      (term, category,))
        return True

    def update_wrong_or_appearance(self, category, count, data, wrong=False):
        query = ' OR '.join(['term = ?' for _ in range(len(data))])
        prop = 'wrong' if wrong else 'appeared'
        with self.conn:
            c = self.conn.cursor()
            c.execute("""
            UPDATE Terms SET {} = {} + ? WHERE {} AND category = ?""".format(prop, prop, query),
                      (count, *data, category))

    def prep_data_for_update(self, data):
        # They must be sorted in order to be used by groupby
        key_count_pairs = [(key, len(list(group))) for key, group in groupby(sorted(data))]
        groups = defaultdict(list)

        for obj in key_count_pairs:
            groups[obj[1]].append(obj[0])

        return groups  # for example: defaultdict(<class 'list'>, {2: ['aviel', 'eti'], 3: ['eli'], 1: ['mordi']})

    def update_many_wrong_appeared(self, category, appeared_terms, wrong_terms):
        category = str.lower(category)

        if len(appeared_terms) > 0:
            groups = self.prep_data_for_update(appeared_terms)
            for count in groups:
                self.update_wrong_or_appearance(category, count, groups.get(count))

        if len(wrong_terms) > 0:
            groups = self.prep_data_for_update(wrong_terms)
            for count in groups:
                self.update_wrong_or_appearance(category, count, groups.get(count), wrong=True)
