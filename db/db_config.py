from sqlalchemy import create_engine

DATABASE_URL = "postgresql://username:password@localhost/sql_training"

engine = create_engine(DATABASE_URL)

def test_connection():
    try:
        with engine.connect() as connection:
            print("Connected to PostgreSQL!")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    test_connection()
