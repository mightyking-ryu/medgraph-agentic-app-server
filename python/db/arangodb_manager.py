from arango import ArangoClient

class ArangoDBManager:
    def __init__(self, config):

        self.host = config["host"]
        self.username = config["user"]
        self.password = config["password"]

        self.client = ArangoClient(hosts=self.host)
        self.db = None

        self.connect()

    # 데이터베이스 연결
    def connect(self):
        if not self.db:
            self.db = self.client.db(username=self.username, password=self.password, verify=True)

    # 연결 닫기
    def close(self):
        if self.db:
            self.db = None