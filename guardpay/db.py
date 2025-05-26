import mysql.connector
import pandas as pd

def conectar_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="guardpay"
    )

def carregar_transacoes():
    conexao = conectar_db()
    query = """
    SELECT *
    FROM transacoes 
    ORDER BY Transacao_ID DESC
    """
    df = pd.read_sql(query, conexao)
    conexao.close()
    return df

def historico_por_cliente(cliente_id):
    conexao = conectar_db()
    query = f"""
        SELECT *
        FROM transacoes
        WHERE Cliente_ID = {cliente_id}
        ORDER BY Transacao_ID DESC
    """
    df = pd.read_sql(query, conexao)
    conexao.close()
    return df

def inserir_transacoes_aleatorias(conexao, transacoes):
    sql = """
        INSERT INTO transacoes (Cliente_ID, Valor_Transacao, Frequencia, fraude_real)
        VALUES (%s, %s, %s, %s)
    """
    cursor = conexao.cursor()
    cursor.executemany(sql, transacoes)
    conexao.commit()
    cursor.close()

def inserir_transacoes_analise(conexao, transacoes):
    sql = """
        INSERT INTO transacoes (Cliente_ID, Valor_Transacao, Frequencia)
        VALUES (%s, %s, %s)
    """
    cursor = conexao.cursor()
    cursor.executemany(sql, transacoes)
    conexao.commit()
    cursor.close()

