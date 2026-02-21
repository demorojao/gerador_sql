import sqlite3
import pandas as pd
from datetime import datetime
import os

DB_PATH = "sales.db"

def init_db():
    # Remover o banco antigo se existir (para resetar os dados durante os testes)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Criação das tabelas
    cursor.execute('''
    CREATE TABLE categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (category_id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        sale_date DATE NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')

    # Inserindo dados de exemplo
    categories_data = [('Eletrônicos',), ('Roupas',), ('Casa',)]
    cursor.executemany("INSERT INTO categories (name) VALUES (?)", categories_data)

    products_data = [
        ('Smartphone X', 2500.00, 1),
        ('Notebook Pro', 5500.00, 1),
        ('Camisa Polo', 89.90, 2),
        ('Calça Jeans', 120.00, 2),
        ('Liquidificador', 150.00, 3),
        ('Cafeteira', 200.00, 3)
    ]
    cursor.executemany("INSERT INTO products (name, price, category_id) VALUES (?, ?, ?)", products_data)

    # Vendas de Janeiro
    january_sales = [
        (1, 10, '2026-01-05'),
        (2, 5, '2026-01-10'),
        (3, 50, '2026-01-12'),
        (4, 30, '2026-01-15'),
        (5, 15, '2026-01-20'),
        (6, 25, '2026-01-22'),
        (1, 8, '2026-01-25'),
        (3, 20, '2026-01-30')
    ]
    
    # Algumas vendas de Fevereiro (para testar os filtros de data)
    february_sales = [
        (1, 5, '2026-02-02'),
        (2, 2, '2026-02-05'),
        (4, 10, '2026-02-10')
    ]

    cursor.executemany("INSERT INTO sales (product_id, quantity, sale_date) VALUES (?, ?, ?)", january_sales + february_sales)

    conn.commit()
    conn.close()
    print("Database 'sales.db' initialized with sample data.")

if __name__ == "__main__":
    init_db()
