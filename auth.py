import sqlite3
import os

class AuthSystem:
    def __init__(self, db_name="usuarios.db"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.base_dir, db_name)
        self.create_users_table()

    def create_users_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    senha TEXT NOT NULL,
                    nivel TEXT DEFAULT 'Operador'
                )
            ''')
            try:
                cursor.execute('INSERT INTO usuarios (usuario, senha, nivel) VALUES (?, ?, ?)', 
                               ('admin', 'admin123', 'Administrador'))
                conn.commit()
            except sqlite3.IntegrityError:
                pass

    def validar_login(self, usuario, senha):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT nivel FROM usuarios WHERE usuario = ? AND senha = ?', (usuario, senha))
            resultado = cursor.fetchone()
            return (True, resultado[0]) if resultado else (False, None)

    def adicionar_usuario(self, usuario, senha, nivel):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO usuarios (usuario, senha, nivel) VALUES (?, ?, ?)', 
                               (usuario, senha, nivel))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
