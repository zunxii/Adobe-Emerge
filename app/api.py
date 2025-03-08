from sqlalchemy import create_engine

# Database credentials
DB_NAME = "nlp_sql"
DB_USER = "postgres"
DB_PASSWORD = "your_password"  # Replace with actual password
DB_HOST = "localhost"
DB_PORT = "3000"  # Use the correct port

# Create a connection
engine = create_engine(f"postgresql+psycopg2://postgres:RDX_akku07@localhost:3000/nlp_sql")

# Test connection
try:
    with engine.connect() as connection:
        print("Connected to PostgreSQL successfully!")
except Exception as e:
    print("Error:", e)
