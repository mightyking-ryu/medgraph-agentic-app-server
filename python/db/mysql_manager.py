import mysql.connector

class MysqlManager:
    def __init__(self, config):
        self.config = config
        self.connection = None

    # 데이터베이스 연결
    def connect(self):
        if not self.connection or not self.connection.is_connected():
            self.connection = mysql.connector.connect(**self.config)
    
    # 일반적인 쿼리 실행 (select가 아닐 경우)
    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                self.connection.commit()
        except Exception as e:
            print(f"Database Error: {e}")
            self.connection.rollback()

    # fetchone 쿼리 실행
    def fetch_one(self, query, params=None):
        try:
            self.connect()
            self.connection.commit()
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchone()
                return result
        except Exception as e:
            print(f"Database Error: {e}")

    # fetchall 쿼리 실행
    def fetch_all(self, query, params=None):
        try:
            self.connect()
            self.connection.commit()
            with self.connection.cursor(dictionary=True) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"Database Error: {e}")

    # 연결 닫기
    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None