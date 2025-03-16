from db.mysql_manager import MysqlManager

class QuestionModel:
    def __init__(self, db_manager: MysqlManager):
        self.db_manager = db_manager

    def get_top_question(self):
        query = "SELECT SQL_NO_CACHE * FROM question_queue ORDER BY created_at ASC LIMIT 1"
        return self.db_manager.fetch_one(query)

    def get_survey_by_userid(self, user_id: str):
        query = "SELECT SQL_NO_CACHE result FROM survey WHERE user_id = %s"
        return self.db_manager.fetch_one(query, (user_id,))

    def create_response(self, user_id: str, question_id: str, response: str):
        query = "INSERT INTO response_queue (user_id, question_id, response) VALUES (%s, %s, %s)"
        self.db_manager.execute_query(query, (user_id, question_id, response))
    
    def create_backup(self, user_id: str, question_id: str, question: str, response: str):
        query = "INSERT INTO backup (user_id, question_id, question, response) VALUES (%s, %s, %s, %s)"
        self.db_manager.execute_query(query, (user_id, question_id, question, response))

    def delete_question_by_id(self, question_id: str):
        query = "DELETE FROM question_queue WHERE question_id = %s"
        self.db_manager.execute_query(query, (question_id,))