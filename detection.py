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

# Definição de aleatoriedade
np.random.seed()

# Criando dados simulados com múltiplas transações por cliente
data = {
    'Transacao_ID': np.arange(1, 11),
    'Cliente_ID': np.tile(np.arange(101, 106), 2),
    'Valor_Transacao': np.random.randint(100, 5000, size=10),  # Valores entre 100 e 5000
    'Frequencia': np.random.randint(1, 20, size=10),  # Frequência entre 1 e 20
    'Localizacao': np.random.choice(['Online', 'Presencial'], size=10)  # Escolha aleatória entre Online e Presencial
}

df = pd.DataFrame(data)
df['Localizacao'] = df['Localizacao'].map({'Online': 1, 'Presencial': 0})

# Normalização do valor da transação por cliente
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

# Calcular a média do valor da transação e da frequência para cada Cliente_ID
df['Media_Valor_Cliente'] = df.groupby('Cliente_ID')['Valor_Transacao'].transform('mean')
df['Media_Frequencia_Cliente'] = df.groupby('Cliente_ID')['Frequencia'].transform('mean')

# Criar novas variáveis comparando a transação atual com a média do cliente
df['Diferenca_Valor'] = df['Valor_Transacao'] - df['Media_Valor_Cliente']
df['Diferenca_Frequencia'] = df['Frequencia'] - df['Media_Frequencia_Cliente']

# Atualizar as variáveis de entrada do modelo (features)
X = df[['Valor_Transacao_Normalizado', 'Frequencia', 'Localizacao', 'Diferenca_Valor', 'Diferenca_Frequencia']]

#Valor_Transacao_Normalizado → Normalização do valor da transação dentro de cada cliente.

#Frequencia → Quantidade de vezes que o cliente realizou transações.

#Localizacao → Se a transação ocorreu Online (1) ou Presencial (0).

#Diferenca_Valor → Diferença entre o valor da transação e a média de transações do cliente.

#Diferenca_Frequencia → Diferença entre a frequência atual e a média de frequência do cliente.
# Definição da variável dependente (target)
y = np.random.choice([0, 1], size=10)  # Geração aleatória de rótulos de fraude

# Divisão dos dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Machine Learning Supervisionado: Treinamento do modelo com dados rotulados
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

df['Fraude'] = rf_model.predict(X)

# Criação do diretório para armazenar os logs dos resultados
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
report_file = os.path.join(log_dir, "relatorio_fraudes.txt")

# Geração do relatório com os resultados
with open(report_file, "w") as f:
    f.write("Relatório de Transações Suspeitas\n")
    f.write("====================================\n\n")
    for _, row in df.iterrows():
        f.write(f"Transação ID: {row['Transacao_ID']}\n")
        f.write(f"Cliente ID: {row['Cliente_ID']}\n")
        f.write(f"Valor da Transação: R${row['Valor_Transacao']:.2f}\n")
        f.write(f"Frequência: {row['Frequencia_Classificada']}\n")
        f.write(f"Localização: {'Online' if row['Localizacao'] == 1 else 'Presencial'}\n")
        f.write(f"Fraude Detectada: {'Sim' if row['Fraude'] == 1 else 'Não'}\n")
        f.write("------------------------------------\n\n")

print(f"Relatório de transações salvo em {report_file}\n")

with open(report_file, "r") as f:
    print(f.read())

# Configurando o estilo dos gráficos
sns.set(style="whitegrid")

# Gráfico de barras para mostrar fraudes por localização
plt.figure(figsize=(6, 4))
ax = sns.countplot(x=df['Localizacao'], hue=df['Fraude'], palette='coolwarm')

# Adicionar os valores sobre as barras, mas somente para barras com valor > 0
for p in ax.patches:
    height = p.get_height()
    if height > 0:  # Exibir o valor apenas se a altura for maior que 0
        ax.annotate(f'{int(height)}',  # Convertendo o valor para inteiro
                    (p.get_x() + p.get_width() / 2., height), 
                    ha='center', va='center', 
                    fontsize=12, color='black', 
                    xytext=(0, 5), textcoords='offset points')

plt.xticks(ticks=[0, 1], labels=['Presencial', 'Online'])
plt.xlabel("Localização da Transação")
plt.ylabel("Número de Transações")
plt.title("Fraudes por Localização")
plt.legend(title="Fraude", labels=["Não", "Sim"])

# Garantir que o eixo Y mostre apenas números inteiros
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=True))

plt.show()

# Caminho para o arquivo de relatório
file_path = "logs/relatorio_fraudes.txt"

# Abrir o arquivo e ler o conteúdo
with open(file_path, "r") as file:
    relatorio = file.read()

# Regex para extrair as informações do relatório
pattern = r"Transação ID: (\d+)\nCliente ID: (\d+)\nValor da Transação: R\$(\d+\.\d{2})\nFrequência: (\w+)\nLocalização: (\w+)\nFraude Detectada: (\w+)"

# Encontrar todas as ocorrências no relatório
matches = re.findall(pattern, relatorio)

# Transformar os resultados encontrados em um DataFrame para uma visualização mais estruturada
df_fraudes = pd.DataFrame(matches, columns=['Transacao_ID', 'Cliente_ID', 'Valor_Transacao', 'Frequencia', 'Localizacao', 'Fraude_Detectada'])

# Converter os tipos de dados adequadamente
df_fraudes['Valor_Transacao'] = df_fraudes['Valor_Transacao'].astype(float)  # Convertendo para float
df_fraudes['Transacao_ID'] = df_fraudes['Transacao_ID'].astype(int)  # Convertendo para int
df_fraudes['Cliente_ID'] = df_fraudes['Cliente_ID'].astype(int)  # Convertendo para int

# Filtrar as transações onde a fraude foi detectada
df_fraudes_com_fraude = df_fraudes[df_fraudes['Fraude_Detectada'] == 'Sim']

# Caminho para o arquivo Excel de saída
excel_path = "logs/relatorio_fraudes.xlsx" 

# Salvar o DataFrame filtrado (somente com fraudes) em um arquivo Excel
df_fraudes_com_fraude.to_excel(excel_path, index=False)

# Confirmar que o arquivo foi gerado
print(f"Relatório de fraudes salvo em {excel_path}")