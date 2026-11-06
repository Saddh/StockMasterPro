import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

class EstoqueDB:
    def __init__(self, db_name="estoque.db"):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(self.base_dir, db_name)
        self.create_tables()

    @contextmanager
    def transaction(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def create_tables(self):
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sku TEXT UNIQUE NOT NULL,
                    nome TEXT NOT NULL,
                    categoria TEXT,
                    quantidade INTEGER DEFAULT 0,
                    estoque_minimo INTEGER DEFAULT 5,
                    criado_por TEXT
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movimentacoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    produto_id INTEGER,
                    tipo TEXT CHECK(tipo IN ('ENTRADA', 'SAIDA')),
                    quantidade INTEGER,
                    data TEXT,
                    usuario TEXT,
                    FOREIGN KEY (produto_id) REFERENCES produtos (id)
                )
            ''')

    def gerar_proximo_sku(self):
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT sku FROM produtos ORDER BY id DESC LIMIT 1')
            ultimo = cursor.fetchone()
            if not ultimo: return "PROD-001"
            try:
                num = int(ultimo[0].split('-')[1])
                return f"PROD-{(num + 1):03d}"
            except: return "PROD-001"

    def adicionar_produto(self, nome, categoria, estoque_minimo, usuario):
        sku = self.gerar_proximo_sku()
        try:
            with self.transaction() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO produtos (sku, nome, categoria, estoque_minimo, criado_por) VALUES (?, ?, ?, ?, ?)', 
                               (sku, nome, categoria, estoque_minimo, usuario))
                return True, sku
        except: return False, "Erro"

    def registrar_movimentacao(self, sku, tipo, qtd, usuario):
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, quantidade FROM produtos WHERE sku = ?', (sku,))
            p = cursor.fetchone()
            if not p: return False, "Produto não encontrado"
            nova_qtd = p[1] + qtd if tipo == 'ENTRADA' else p[1] - qtd
            if nova_qtd < 0: return False, "Estoque insuficiente"
            cursor.execute('UPDATE produtos SET quantidade = ? WHERE id = ?', (nova_qtd, p[0]))
            cursor.execute('INSERT INTO movimentacoes (produto_id, tipo, quantidade, data, usuario) VALUES (?, ?, ?, ?, ?)',
                           (p[0], tipo, qtd, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), usuario))
            return True, "Sucesso"

    def listar_produtos(self):
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM produtos')
            return cursor.fetchall()

    def buscar_produtos_por_texto(self, texto):
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT sku, nome FROM produtos WHERE nome LIKE ? OR sku LIKE ?', (f"%{texto}%", f"%{texto}%"))
            return cursor.fetchall()

    def deletar_produto(self, sku):
        with self.transaction() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM produtos WHERE sku = ?', (sku,))
            return cursor.rowcount > 0
