from sqlalchemy import create_engine, text

engine = create_engine("postgresql+psycopg2://admin:admin@localhost:5432/berka")

with engine.connect() as conn:
    result = conn.execute(text("SELECT version()"))
    print(result.scalar())