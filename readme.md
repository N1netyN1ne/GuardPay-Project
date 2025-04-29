# 🔍 Sistema de Detecção de Fraudes em Transações

Este projeto simula um sistema de detecção de fraudes em transações financeiras. Utilizando aprendizado de máquina supervisionado, 
o sistema analisa dados de clientes e suas transações para identificar comportamentos suspeitos.

---

## ✨ Descrição do Projeto

O projeto gera dados simulados de transações de clientes, aplica pré-processamentos (como normalização e classificação de frequência),
treina um modelo de **Random Forest** para detectar fraudes e gera relatórios com os resultados.

Também são gerados gráficos para análise visual das fraudes por localização.

---

## ✅ Principais Funcionalidades

- Geração de dados fictícios de transações financeiras
- Normalização por cliente e análise de comportamento
- Classificação de frequência de transações (Baixa, Média, Alta)
- Treinamento de modelo Random Forest para predição de fraudes
- Geração de relatório `.txt` com o resultado das transações
- Visualização gráfica das fraudes por localização
- Exportação de fraudes detectadas para arquivo `.xlsx`

---

## ⚙️ Instruções de Instalação e Configuração

1. **Clone o repositório:**
   git clone https://github.com/N1netyN1ne/GuardPay-Project
   
2. **Acesse a pasta do projeto:**
    cd GuardPay-Project

3. **(Opcional) Crie e ative um ambiente virtual:**
    python -m venv venv
    # No Windows
    venv\Scripts\activate

    # No Linux/Mac
    source venv/bin/activate

4. **Instale as dependências:**
    pip install -r requirements.txt

5. **Execute o projeto:**
    python main.py
