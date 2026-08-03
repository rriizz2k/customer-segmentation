import pandas as pd
from sqlalchemy import create_engine


def load_data():
    engine = create_engine("postgresql+psycopg2://admin:admin@localhost:5432/berka")

    tables = ["account", "card", "client", "disp", "district", "loan", "order", "trans"]

    for name in tables:
        df = pd.read_csv(f"data/{name}.csv", sep=";")
        df.to_sql(name, engine, if_exists="replace", index=False)
        print(f"таблица {name} готова")

load_data()
    