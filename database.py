import sqlite3



class Database:
    def __init__(self, database_name):
        self.database_name = database_name
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.create_database()


    def create_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                bot_id INTEGER,
                captcha_type TEXT
            )
        ''')
        self.conn.commit()


    def close(self):
        self.conn.close()


    def insert_bot(self, bot_id, captcha_type):
        self.cursor.execute('INSERT INTO bots (bot_id, captcha_type) VALUES (?, ?)', (bot_id, captcha_type))
        self.conn.commit()


    def get_all_bots(self):
        self.cursor.execute('SELECT * FROM bots')
        result = self.cursor.fetchall()
        return result


