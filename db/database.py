from sqlalchemy import (
    create_engine, 
    MetaData, 
    Table, 
    Column,
    String,
    Text,
    Integer,
    select,
    DateTime,
    func,
    delete,

)

from config import MYSQL_URL

engine = create_engine(MYSQL_URL)
meta = MetaData()

class CarManager():

    def __init__(self, engine) -> None:
        self.engine = engine
        self.car = self.get_table_schema()

    def get_table_schema(self):
        car = Table(
            "cars", meta,
            Column("id",Integer, primary_key=True),
            Column("title", String(200)),
            Column("som", Integer),
            Column("dollar", Integer),
            Column("mobile", String(50)),
            Column("description", Text), 
            Column("link",String(255), nullable=False, unique=True),
            Column("created", DateTime(timezone=True), server_default=func.now())
        )
        return car
    
    def create_table(self):
        meta.create_all(self.engine, checkfirst=True)
        print("Таблица успешно создано")


    def insert_car(self, data):
        print(data)
        ins = self.car.insert().values(
           **data
        )
        connect = self.engine.connect()
        result = connect.execute(ins)
        connect.commit()
        connect.close()

    def check_car_in_db(self, url):
        query = select(self.car).where(self.car.c.link==url)
        connect = self.engine.connect()
        result = connect.execute(query)
        connect.close()
        result = result.fetchone()
        return result is not None
    
    def search_by_name(self, name: str, offset: int = 0, limit=5):
        query = select(self.car).where(
            self.car.c.title.like(f"%{name}%")
            ).offset(offset).limit(limit)
        connect = self.engine.connect()
        result = connect.execute(query)
        connect.close()
        cars = result.fetchall()
        return cars
    
    def search_by_price(self, start, end):
        query = select(self.car).where(self.car.c.dollar.between(start, end))
        # SELECT * FROM cars WHERE dollar BETWEEN start and end;
        connect = self.engine.connect()
        result = connect.execute(query)
        connect.close()
        cars = result.fetchall()
        return cars

    def delete_post(self, old_time):
        query = delete(self.car).where(self.car.c.created<=old_time)# Создание запроса
        connect = self.engine.connect()
        result = connect.execute(query) # Выполнение запроса
        connect.commit()
        connect.close()
    
manager = CarManager(engine=engine)