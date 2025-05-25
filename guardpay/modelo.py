import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

MODEL_DIR = "modelo"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..",MODEL_DIR,"modelo_treinado.pkl")

def treinar_modelo(df):
    if 'fraude_real' not in df.columns:
        return None, "⚠️ Coluna 'fraude_real' não encontrada.", {}
    
    # Usar apenas transações rotuladas manualmente
    df_treino = df[df['fraude_real'].notnull()].copy()
    if df_treino.empty:
        return None, "⚠️ Nenhuma transação rotulada disponível para treinar o modelo."
    
    # Pré-processamento
    scaler = StandardScaler()
    df_treino['Valor_Transacao_Normalizado'] = df_treino.groupby('Cliente_ID')['Valor_Transacao'].transform(
        lambda x: scaler.fit_transform(x.values.reshape(-1, 1)).flatten())
    df_treino['Media_Valor_Cliente'] = df_treino.groupby('Cliente_ID')['Valor_Transacao'].transform('mean')
    df_treino['Media_Frequencia_Cliente'] = df_treino.groupby('Cliente_ID')['Frequencia'].transform('mean')
    df_treino['Diferenca_Valor'] = df_treino['Valor_Transacao'] - df_treino['Media_Valor_Cliente']
    df_treino['Diferenca_Frequencia'] = df_treino['Frequencia'] - df_treino['Media_Frequencia_Cliente']

    # Features e target
    X = df_treino[['Valor_Transacao_Normalizado', 'Frequencia', 'Diferenca_Valor', 'Diferenca_Frequencia']]
    y = df_treino['fraude_real']

    # Dividir treino e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Treinar modelo
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # Avaliação
    y_pred = modelo.predict(X_test)
    metricas = {
        "Acurácia": accuracy_score(y_test, y_pred),
        "Precisão": precision_score(y_test, y_pred, zero_division=0),
        "Recall": recall_score(y_test, y_pred, zero_division=0),
        "F1-score": f1_score(y_test, y_pred, zero_division=0)
    }

    joblib.dump(modelo,MODEL_PATH)
    return modelo, "✅ Modelo treinado com sucesso com dados reais.", metricas


def carregar_modelo_salvo():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    else:
        return None
    
def aplicar_modelo(modelo, df):
    # Pré-processamento
    scaler = StandardScaler()
    df['Valor_Transacao_Normalizado'] = df.groupby('Cliente_ID')['Valor_Transacao'].transform(
        lambda x: scaler.fit_transform(x.values.reshape(-1, 1)).flatten())
    
    df['Media_Valor_Cliente'] = df.groupby('Cliente_ID')['Valor_Transacao'].transform('mean')
    df['Media_Frequencia_Cliente'] = df.groupby('Cliente_ID')['Frequencia'].transform('mean')
    df['Diferenca_Valor'] = df['Valor_Transacao'] - df['Media_Valor_Cliente']
    df['Diferenca_Frequencia'] = df['Frequencia'] - df['Media_Frequencia_Cliente']

    X = df[['Valor_Transacao_Normalizado', 'Frequencia', 'Diferenca_Valor', 'Diferenca_Frequencia']]
    df['Fraude'] = modelo.predict(X)
    return df