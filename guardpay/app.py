import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from modelo import treinar_modelo, aplicar_modelo, carregar_modelo_salvo
from db import carregar_transacoes, conectar_db, historico_por_cliente, inserir_transacoes_analise
from utils import gerar_transacao_baixoValor_analise, gerar_transacao_altoValor_analise

st.set_page_config(page_title="GuardPay - Análise de Fraudes", layout="wide")
st.title("🔐 GuardPay - Análise de Transações Fraudulentas")

# Explicação da lógica
st.markdown("""
### ℹ️ Como funciona o GuardPay?
1. O sistema **carrega as transações** do banco de dados.
2. Se existir um modelo de IA treinado, ele será usado. Caso contrário, um novo será treinado com base nas transações rotuladas.
3. O modelo classifica cada transação como **fraude** ou **não fraude**.
4. Abaixo você pode visualizar as fraudes detectadas e investigar o histórico por cliente.
""")

# Carregar dados do banco
df = carregar_transacoes()

#Carregar modelo salvo
modelo = carregar_modelo_salvo()

#Verifica se há modelo salvo
if modelo is None:
    modelo, status = treinar_modelo(df)
    st.info("ℹ️ Novo modelo treinado, pois nenhum modelo salvo foi encontrado.")
else:
    st.success("✅ Modelo carregado com sucesso.")

# Botão para gerar transações de baixo valor para analise do modelo
if st.button("Gerar Transação baixo valor para analise"):
    transacoes = gerar_transacao_baixoValor_analise()
    conexao = conectar_db()
    inserir_transacoes_analise(conexao,transacoes)
    st.success("Transação geradas com sucesso!")
    df = carregar_transacoes()

# Botão para gerar transaçõe de alto valor para analise do modelo
if st.button("Gerar Transação alto  valor para analise"):
    transacoes = gerar_transacao_altoValor_analise()
    conexao = conectar_db()
    inserir_transacoes_analise(conexao,transacoes)
    st.success("Transação geradas com sucesso!")
    df = carregar_transacoes()

# Treinar o modelo
modelo, status, metricas = treinar_modelo(df)

if modelo is None:
    st.warning(status)
    st.stop()

# Aplicar modelo treinado
df = aplicar_modelo(modelo, df)

# Exibir total de transações e fraudes
col1, col2 = st.columns(2)
col1.metric("🔢 Total de Transações", len(df))
col2.metric("🚨 Total de Fraudes Detectadas", df['Fraude'].sum())

# Mapear rótulos
df['Fraude_Label'] = df['Fraude'].map({0: 'Não Fraude', 1: 'Fraude'})

# Gráfico de barras
df['Fraude_Label'] = df['Fraude'].map({0: 'Não Fraude', 1: 'Fraude'})
st.subheader("📊 Distribuição de Transações Fraudulentas")
fig, ax = plt.subplots(figsize=(4, 3))
sns.countplot(data=df, x='Fraude_Label', palette='pastel', ax=ax)

# Rótulos nas barras
for p in ax.patches:
    ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width()/2, p.get_height()),
                ha='center', va='bottom', fontsize=9, color='black')

ax.set_xlabel("Tipo de Transação", fontsize=10)
ax.set_ylabel("Quantidade", fontsize=10)
ax.set_title("Classificação das Transações pela IA", fontsize=11)
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
st.pyplot(fig)

# Tabela geral de transaçoes
st.subheader("🔍 Lista de Transações completa")
st.dataframe(df[['Transacao_ID', 'Cliente_ID', 'Valor_Transacao', 'Frequencia', 'fraude_real']])

# Tabela geral de fraudes detectadas
st.subheader("🔍 Lista de Transações com Fraude Detectada")
df_fraudes = df[df['Fraude'] == 1]
st.dataframe(df_fraudes[['Transacao_ID', 'Cliente_ID', 'Valor_Transacao', 'Frequencia','fraude_real']])

# Histórico por cliente
st.subheader("📁 Histórico de Transações por Cliente com Fraude")
clientes_fraudados = df[df['Fraude'] == 1]['Cliente_ID'].unique()
cliente_escolhido = st.selectbox("Selecione um Cliente", clientes_fraudados)

if cliente_escolhido:
    historico = historico_por_cliente(cliente_escolhido)
    st.write(f"Transações do Cliente **{cliente_escolhido}**:")
    st.dataframe(historico[['Transacao_ID', 'Valor_Transacao', 'Frequencia', 'fraude_real']])

st.markdown("---")
st.subheader("📊 Desempenho do Modelo")

if metricas:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Acurácia", f"{metricas['Acurácia']:.2%}")
    col2.metric("Precisão", f"{metricas['Precisão']:.2%}")
    col3.metric("Recall", f"{metricas['Recall']:.2%}")
    col4.metric("F1-score", f"{metricas['F1-score']:.2%}")
else:
    st.info("O modelo ainda não foi treinado com dados rotulados.")

with st.expander("Clique aqui para entender cada métrica"):
    st.markdown("""
    **🔍 Acurácia**  
    Proporção de todas as previsões corretas (fraudes e não fraudes).

    **🎯 Precisão**  
    Das transações que o modelo previu como fraude, quantas realmente eram fraude?  
    Alta precisão = poucos falsos alarmes.

    **📡 Recall (Sensibilidade)**  
    Das fraudes reais, quantas o modelo conseguiu identificar?  
    Alto recall = menos fraudes escapando.

    **⚖️ F1-score**  
    Equilíbrio entre Precisão e Recall. Útil quando o conjunto de dados está desbalanceado.
    
    ---
    **Exemplo de Erros/Acertos:**

    | Previsão | Realidade | Interpretação         |
    |----------|-----------|------------------------|
    | 1        | 1         | ✅ Verdadeiro Positivo |
    | 1        | 0         | ❌ Falso Positivo      |
    | 0        | 0         | ✅ Verdadeiro Negativo |
    | 0        | 1         | ❌ Falso Negativo      |
    """)