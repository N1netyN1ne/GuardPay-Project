#Classe utilitária  
import numpy as np

def gerar_transacao_baixoValor_analise(n=1):
    transacoes = []
    for _ in range(n):
        cliente_id = np.random.randint(100, 111)
        valor = float(np.random.randint(100, 1000))
        freq = int(np.random.randint(1, 10))
        transacoes.append((cliente_id, valor, freq))
    return transacoes

def gerar_transacao_altoValor_analise(n=1):
    transacoes = []
    for _ in range(n):
        cliente_id = np.random.randint(100, 111)
        valor = float(np.random.randint(1000, 100000))
        freq = int(np.random.randint(1, 30))
        transacoes.append((cliente_id, valor, freq))
    return transacoes