import os

DB_CONFIG = {
    "DB_NAME": os.getenv("DB_NAME", "phonebook_db"),
    "DB_USER": os.getenv("DB_USER", "postgres"),
    "DB_PASSWORD": os.getenv("DB_PASSWORD", "12345678"),
    "DB_HOST": os.getenv("DB_HOST", "localhost"),
    "DB_PORT": os.getenv("DB_PORT", "5432")
}