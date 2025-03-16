import os

# MySQL 연결 정보
MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
}

# ArangoDB 연결 정보
ARANGODB_CONFIG = {
    "host": os.getenv("ARANGODB_HOST"),
    "user": os.getenv("ARANGODB_USER", "root"),
    "password": os.getenv("ARANGODB_PASSWORD"),
    "database": os.getenv("ARANGODB_DATABASE"),
}

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")