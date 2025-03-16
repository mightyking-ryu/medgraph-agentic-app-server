import os
import time
import signal
import sys

from config.settings import OPENAI_API_KEY, MYSQL_CONFIG
from db.mysql_manager import MysqlManager
from models.question_model import QuestionModel

import engine.langchain_agent as agent

# 종료 플래그
stop_flag = False

# 종료 신호 감지 핸들러
def signal_handler(signum, frame):
    global stop_flag
    print(f"\nReceived signal {signum}, shutting down gracefully...")
    stop_flag = True

# 종료 신호 등록
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# 질문 처리 함수
def process_question(question_model: QuestionModel):

    # 가장 오래된 질문 가져오기
    data = question_model.get_top_question()

    if not data:
        return

    user_id = data["user_id"]
    question_id = data["question_id"]
    user_query = data["question"]

    # 사용자 개인정보 가져오기
    survey_row = question_model.get_survey_by_userid(user_id)
    user_info = survey_row["result"]

    # 응답 생성 (LLM 대체 가능)
    user_query = f"response for question '{user_query}' with user info {user_info}"
    try:
        response = agent.query_graph(user_query)
    except Exception as e:
        print(f"query_graph runtime error: {e}")
        return

    # response_queue에 응답 추가
    question_model.create_response(user_id, question_id, response)

    # backup 테이블에 질문과 응답 백업
    question_model.create_backup(user_id, question_id, user_query, response)

    # question_queue에서 해당 질문 삭제
    question_model.delete_question_by_id(question_id)

# 메인 함수
def main():

    global stop_flag

    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    mysql_manager = MysqlManager(MYSQL_CONFIG)
    question_model = QuestionModel(mysql_manager)

    while not stop_flag:
        process_question(question_model)
        time.sleep(0.5)

    mysql_manager.close()

    # 정상 종료
    print("\nProgram has been terminated successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()