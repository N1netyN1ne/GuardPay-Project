# 🔍 Sistema de Detecção de Fraudes em Transações

Este projeto simula um sistema de detecção de fraudes em transações financeiras. Utilizando aprendizado de máquina supervisionado, 
o sistema analisa dados de clientes e suas transações para identificar comportamentos suspeitos.

---

## ✨ Descrição do Projeto

O projeto gera dados simulados de transações de clientes, aplica pré-processamentos (como normalização e classificação de frequência),
treina um modelo de **Random Forest** para detectar fraudes

Também são gerados gráficos para análise visual das fraudes.

---

## ✅ Principais Funcionalidades

- Geração de dados fictícios de transações financeiras
- Normalização por cliente e análise de comportamento
- Treinamento de modelo Random Forest para predição de fraudes
- Visualização gráfica das fraudes

---

### 🚀 Instalação do GuardPay

### Pré-requisitos

- Python 3.12 ou superior
- MySQL Server
- Banco de dados `guardpay` criado (veja "Importação do Banco")

1. **Clone o repositório:**
   - git clone https://github.com/N1netyN1ne/GuardPay-Project

2. **Acesse a pasta do projeto:**
    - cd guardpay

3. **(Opcional) Crie e ative um ambiente virtual:**
    - python -m venv venv

4. **Instale as dependências:**
    - pip install -r requirements.txt

5. **Importe o Banco de Dados** 
    - Acesse http://localhost/phpmyadmin
    - Crie o banco chamado guardpay
    - Vá na aba Importar
    - Escolha o arquivo guardpay.sql fornecido em DB/guardpay.sql
    - Clique em Executar
    
6. **Como Executar**
    - No terminal, execute:
    - streamlit run guardpay/app.py
 

