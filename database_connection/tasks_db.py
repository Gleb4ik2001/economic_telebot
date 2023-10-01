from .database import Database

class Tasks:
    
    id:int
    bilet_number: int
    answer : str


    @staticmethod
    def insert_bilet(
        conn:Database,
        bilet_number: int,
        answer : str
    ):
        try:
            with conn.cursor() as cur:
                cur.execute(F"""
                    INSERT INTO tasks(
                        bilet_number,
                        answer
                    ) VALUES(
                        {bilet_number},
                        '{answer}'
                    );
                """)
                print(f"Билет #{bilet_number} добавлен!")
        except Exception as e:
            print("Ошибка добавления: ",e)
    
    @staticmethod
    def find_bilet(
        conn:Database,
        bilet_number:int
    ):
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    SELECT answer FROM tasks WHERE bilet_number = {bilet_number};
                    """
                )
                result = cur.fetchall()
                return result
        except Exception as exc:
            print(f'Ошибка поиска билета #{bilet_number}: ',exc)
            raise exc
        