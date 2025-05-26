import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os

def treinar_modelo(df):
    # Filtrar dados rotulados
    df_treino = df[df['fraude_real'].notnull()]

    if df_treino.empty:
        return None, "Nenhum dado rotulado disponível para treinamento.", None

    # Calcular médias sem incluir transações fraudulentas
    df_validas = df[(df['fraude_real'].isnull()) | (df['fraude_real'] == 0)]
    medias_valor = df_validas.groupby('Cliente_ID')['Valor_Transacao'].mean()
    medias_freq = df_validas.groupby('Cliente_ID')['Frequencia'].mean()

    df['Media_Valor_Cliente'] = df['Cliente_ID'].map(medias_valor)
    df['Media_Frequencia_Cliente'] = df['Cliente_ID'].map(medias_freq)
    df['Diferenca_Valor'] = df['Valor_Transacao'] - df['Media_Valor_Cliente']
    df['Diferenca_Frequencia'] = df['Frequencia'] - df['Media_Frequencia_Cliente']

    df_treino['Media_Valor_Cliente'] = df_treino.groupby('Cliente_ID')['Valor_Transacao']\
        .transform(lambda x: x[~df_treino.loc[x.index, 'fraude_real'].astype(bool)].mean())

    df_treino['Media_Frequencia_Cliente'] = df_treino.groupby('Cliente_ID')['Frequencia']\
        .transform(lambda x: x[~df_treino.loc[x.index, 'fraude_real'].astype(bool)].mean())

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

    df['Media_Valor_Cliente'] = df.groupby('Cliente_ID')['Valor_Transacao'].transform('mean')
    df['Media_Frequencia_Cliente'] = df.groupby('Cliente_ID')['Frequencia'].transform('mean')
    df['Diferenca_Valor'] = df['Valor_Transacao'] - df['Media_Valor_Cliente']
    df['Diferenca_Frequencia'] = df['Frequencia'] - df['Media_Frequencia_Cliente']

    X = df[['Valor_Transacao', 'Frequencia', 'Diferenca_Valor', 'Diferenca_Frequencia']]
    df['Fraude'] = modelo.predict(X)
    return df

def carregar_modelo_salvo():
    caminho_modelo = 'modelo/modelo_treinado.pkl'
    if os.path.exists(caminho_modelo):
        return joblib.load(caminho_modelo)
    return None
