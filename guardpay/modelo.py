from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os

def treinar_modelo(df):
    # Filtrar dados rotulados para treinamento
    df_treino = df[df['fraude_real'].notnull()].copy() # Use .copy() para evitar SettingWithCopyWarning

    if df_treino.empty:
        return None, "Nenhum dado rotulado disponível para treinamento.", None

    df_nao_fraude = df_treino[df_treino['fraude_real'] == 0]
    
    medias_valor_cliente = df_nao_fraude.groupby('Cliente_ID')['Valor_Transacao'].mean()
    medias_frequencia_cliente = df_nao_fraude.groupby('Cliente_ID')['Frequencia'].mean()

    # Mapear as médias para o DataFrame de treinamento
    df_treino['Media_Valor_Cliente'] = df_treino['Cliente_ID'].map(medias_valor_cliente)
    df_treino['Media_Frequencia_Cliente'] = df_treino['Cliente_ID'].map(medias_frequencia_cliente)
    
    global_mean_valor_nao_fraude = df_nao_fraude['Valor_Transacao'].mean()
    global_mean_frequencia_nao_fraude = df_nao_fraude['Frequencia'].mean()
    
    df_treino['Media_Valor_Cliente'].fillna(global_mean_valor_nao_fraude, inplace=True)
    df_treino['Media_Frequencia_Cliente'].fillna(global_mean_frequencia_nao_fraude, inplace=True)

    df_treino['Diferenca_Valor'] = df_treino['Valor_Transacao'] - df_treino['Media_Valor_Cliente']
    df_treino['Diferenca_Frequencia'] = df_treino['Frequencia'] - df_treino['Media_Frequencia_Cliente']

    # Separar features e target
    X = df_treino[['Valor_Transacao', 'Frequencia', 'Diferenca_Valor', 'Diferenca_Frequencia']]
    y = df_treino['fraude_real'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    y_pred = modelo.predict(X_test)

    metricas = {
        'Acurácia': accuracy_score(y_test, y_pred),
        'Precisão': precision_score(y_test, y_pred, zero_division=0),
        'Recall': recall_score(y_test, y_pred, zero_division=0),
        'F1-score': f1_score(y_test, y_pred, zero_division=0),
    }

    joblib.dump(modelo, 'modelo/modelo_treinado.pkl')

    return modelo, "Modelo treinado com sucesso!", metricas

def aplicar_modelo(modelo, df):
    if modelo is None:
        return df

    # Criar uma cópia para evitar SettingWithCopyWarning
    df_temp = df.copy()

    # Calcular médias APENAS para transações que são explicitamente 'Não Fraude' (0)
    df_nao_fraude_historico = df_temp[df_temp['fraude_real'] != 1] # Inclui 0 e None

    # Calcular as médias com base neste subconjunto
    medias_valor_cliente = df_nao_fraude_historico.groupby('Cliente_ID')['Valor_Transacao'].mean()
    medias_frequencia_cliente = df_nao_fraude_historico.groupby('Cliente_ID')['Frequencia'].mean()

    # Mapear as médias de volta para o DataFrame completo
    df_temp['Media_Valor_Cliente'] = df_temp['Cliente_ID'].map(medias_valor_cliente)
    df_temp['Media_Frequencia_Cliente'] = df_temp['Cliente_ID'].map(medias_frequencia_cliente)

    # Preencher NaNs que podem surgir (ex: cliente sem histórico de não-fraudes)
    global_mean_valor_nao_fraude = df_nao_fraude_historico['Valor_Transacao'].mean()
    global_mean_frequencia_nao_fraude = df_nao_fraude_historico['Frequencia'].mean()
    
    df_temp['Media_Valor_Cliente'].fillna(global_mean_valor_nao_fraude, inplace=True)
    df_temp['Media_Frequencia_Cliente'].fillna(global_mean_frequencia_nao_fraude, inplace=True)

    df_temp['Diferenca_Valor'] = df_temp['Valor_Transacao'] - df_temp['Media_Valor_Cliente']
    df_temp['Diferenca_Frequencia'] = df_temp['Frequencia'] - df_temp['Media_Frequencia_Cliente']

    # Preencher quaisquer NaNs remanescentes nas colunas de diferença (ex: para clientes com apenas 1 transação)
    df_temp['Diferenca_Valor'].fillna(0, inplace=True)
    df_temp['Diferenca_Frequencia'].fillna(0, inplace=True)

    X = df_temp[['Valor_Transacao', 'Frequencia', 'Diferenca_Valor', 'Diferenca_Frequencia']]
    
    # Garantir que não há NaNs em X antes da previsão
    X = X.fillna(X.mean())

    df['Fraude'] = modelo.predict(X)
    return df

def carregar_modelo_salvo():
    caminho_modelo = 'modelo/modelo_treinado.pkl'
    if os.path.exists(caminho_modelo):
        return joblib.load(caminho_modelo)
    return None