# PostgreSQL
import psycopg2
from psycopg2 import extras

def connection():
    conn = psycopg2.connect(host="meridia.crooktec.com",database="intelliherd",user="tannercrook",password="Kinger413!")
    c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return c, conn