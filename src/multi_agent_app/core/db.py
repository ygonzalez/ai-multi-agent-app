"""Loads the Chinook sample DB into an in-memory SQLite engine."""
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
import sqlite3
import requests

CHINOOK_SQL_URL = (
    "https://raw.githubusercontent.com/lerocha/chinook-database/master/"
    "ChinookDatabase/DataSources/Chinook_Sqlite.sql"
)

def init_memory_engine():
    sql = requests.get(CHINOOK_SQL_URL, timeout=30).text
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.executescript(sql)
    return create_engine("sqlite://", creator=lambda: conn, poolclass=StaticPool)
