import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Definir semente aleatória
np.random.seed()

# Criar dados simulados
data = {
    'Transacao_ID': np.arange(1, 11),
    'Cliente_ID': np.tile(np.arange(101, 106), 2),
    'Valor_Transacao': np.random.randint(100, 5000, size=10),
    'Frequencia': np.random.randint(1, 20, size=10)
}

df = pd.DataFrame(data)

# Normalização por cliente
scaler = StandardScaler()
df['Valor_Transacao_Normalizado'] = df.groupby('Cliente_ID')['Valor_Transacao'].transform(
    lambda x: scaler.fit_transform(x.values.reshape(-1, 1)).flatten())

# Classificação da frequência
def classificar_frequencia(grupo):
    q1 = grupo.quantile(0.33)
    q2 = grupo.quantile(0.66)
    def categorizar(f):
        if f <= q1:
            return 'Baixa'
        elif f <= q2:
            return 'Média'
        else:
            return 'Alta'
    return grupo.apply(categorizar)

df['Frequencia_Classificada'] = df.groupby('Cliente_ID', group_keys=False)['Frequencia'].apply(classificar_frequencia)

# Comparação com média por cliente
df['Media_Valor_Cliente'] = df.groupby('Cliente_ID')['Valor_Transacao'].transform('mean')
df['Media_Frequencia_Cliente'] = df.groupby('Cliente_ID')['Frequencia'].transform('mean')
df['Diferenca_Valor'] = df['Valor_Transacao'] - df['Media_Valor_Cliente']
df['Diferenca_Frequencia'] = df['Frequencia'] - df['Media_Frequencia_Cliente']

# Features e target
X = df[['Valor_Transacao_Normalizado', 'Frequencia', 'Diferenca_Valor', 'Diferenca_Frequencia']]
y = np.random.choice([0, 1], size=10)

# Treinamento do modelo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Previsões
df['Fraude'] = rf_model.predict(X)

# Criar diretório e salvar relatório
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
report_file = os.path.join(log_dir, "relatorio_fraudes.txt")

with open(report_file, "w") as f:
    f.write("Relatório de Transações Suspeitas\n")
    f.write("====================================\n\n")
    for _, row in df.iterrows():
        f.write(f"Transação ID: {row['Transacao_ID']}\n")
        f.write(f"Cliente ID: {row['Cliente_ID']}\n")
        f.write(f"Valor da Transação: R${row['Valor_Transacao']:.2f}\n")
        f.write(f"Frequência: {row['Frequencia_Classificada']}\n")
        f.write(f"Fraude Detectada: {'Sim' if row['Fraude'] == 1 else 'Não'}\n")
        f.write("------------------------------------\n\n")

print(f"Relatório de transações salvo em {report_file}\n")

# Gráfico de barras: fraudes vs. não fraudes
sns.set(style="whitegrid")
plt.figure(figsize=(6, 4))
ax = sns.countplot(x=df['Fraude'], palette='pastel')

# Rótulos
for p in ax.patches:
    height = p.get_height()
    ax.annotate(f'{int(height)}', (p.get_x() + p.get_width() / 2., height), 
                ha='center', va='center', fontsize=12, color='black', 
                xytext=(0, 5), textcoords='offset points')

plt.xticks(ticks=[0, 1], labels=['Não Fraude', 'Fraude'])
plt.xlabel("Tipo de Transação")
plt.ylabel("Número de Transações")
plt.title("Distribuição de Transações Fraudulentas")
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))
plt.tight_layout()
plt.show()

# Gerar Excel com fraudes
with open(report_file, "r") as file:
    relatorio = file.read()

pattern = r"Transação ID: (\d+)\nCliente ID: (\d+)\nValor da Transação: R\$(\d+\.\d{2})\nFrequência: (\w+)\nFraude Detectada: (\w+)"
matches = re.findall(pattern, relatorio)
df_fraudes = pd.DataFrame(matches, columns=['Transacao_ID', 'Cliente_ID', 'Valor_Transacao', 'Frequencia', 'Fraude_Detectada'])
df_fraudes['Valor_Transacao'] = df_fraudes['Valor_Transacao'].astype(float)
df_fraudes['Transacao_ID'] = df_fraudes['Transacao_ID'].astype(int)
df_fraudes['Cliente_ID'] = df_fraudes['Cliente_ID'].astype(int)
df_fraudes_com_fraude = df_fraudes[df_fraudes['Fraude_Detectada'] == 'Sim']

excel_path = "logs/relatorio_fraudes.xlsx"
df_fraudes_com_fraude.to_excel(excel_path, index=False)
print(f"Relatório de fraudes salvo em {excel_path}")
