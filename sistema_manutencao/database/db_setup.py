import sqlite3
import os


DB_FILENAME = 'manutencao_preditiva.db' 

def get_db_connection():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, DB_FILENAME)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados em {DB_PATH}: {e}")
        return None

def init_db():
    conn = None
    try:
        conn = get_db_connection()
        if not conn: return
        cursor = conn.cursor()

        # Tabela LEITURAS_SENSOR
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leituras_sensor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pressao REAL NOT NULL,
                temperatura REAL NOT NULL,
                vibracao REAL NOT NULL,
                ciclos_ate_falha_real INTEGER,       
                data_registro TEXT NOT NULL
            );
        """)

        # Tabela PREDICOES_ML
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predicoes_ml (
                id_leitura INTEGER PRIMARY KEY,
                rul_predita REAL NOT NULL,           
                nivel_risco TEXT NOT NULL,           
                FOREIGN KEY (id_leitura) REFERENCES leituras_sensor(id)
            );
        """)

        conn.commit()
        print("✅ Tabelas de banco de dados criadas/verificadas com sucesso.")

    except sqlite3.Error as e:
        print(f"Erro CRÍTICO ao inicializar o banco de dados e criar tabelas: {e}")
    finally:
        if conn:
            conn.close()