import psycopg2
from decouple import config


class Database:
    def __new__(cls,*args,**kwargs) :
        if not hasattr(cls,"instance"):
            cls.instance = super(Database,cls).__new__(cls)
        return cls.instance

    def __init__(
            self,
            host,
            port,
            user,
            password,
            db_name
    ) -> None:
        self.host = host
        self.port =port
        self.user = user
        self.password = password
        self.db_name = db_name
        self.conn = None
        try:
            self.conn = psycopg2.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                database = self.db_name,
            )
            self.conn.autocommit = True
            print("Соединение с БД успешно!")
        except Exception as e:
            print("Ошибка -",e)
    

    def create_table(self) -> None:
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS tasks(
                        id SERIAL PRIMARY KEY,
                        bilet_number INTEGER NOT NULL,
                        answer TEXT NOT NULL
                    );
                """)
                print('Таблица создана')
        except Exception as e:
            print("Ошибка создания таблиц: ",e)