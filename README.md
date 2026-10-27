# 🦠 Pipeline ETL & Dashboard Interativo - COVID-19 no Brasil

Projeto desenvolvido para fins acadêmicos e portfólio prático de Ciência e Engenharia de Dados. O projeto contempla um fluxo completo de ponta a ponta: extração de dados públicos, tratamento e modelagem em banco relacional SQLite e visualização analítica via Streamlit.

---

## 📌 Arquitetura da Solução

O projeto segue o padrão modular com separação clara de responsabilidades:

```text
Projeto_COVID/
│
├── etl/
│   ├── __init__.py       # Configuração de módulo do pacote
│   ├── extract.py        # Extração de dados consolidados da web (Extract)
│   ├── transform.py      # Limpeza, tratamento temporal e criação de métricas (Transform)
│   └── load.py           # Carga estruturada em banco SQLite (Load)
│
├── data/
│   └── covid_brasil.db   # Banco de dados relacional gerado localmente
│
├── app.py                # Dashboard analítico em Streamlit
├── main.py               # Orquestrador do pipeline ETL
├── requirements.txt      # Dependências do projeto
└── .gitignore            # Exclusão de arquivos de ambiente e temporários
```

🛠️ Tecnologias Utilizadas
Linguagem: Python

Manipulação de Dados: Pandas

Banco de Dados: SQLite

Visualização: Streamlit & Plotly

Controle de Versão: Git & GitHub

📊 Regras de Negócio & Tratamento Epidemiológico
Média Móvel de 7 Dias: Implementada via .rolling(window=7) sobre dados ordenados cronologicamente, eliminando o ruído e o represamento de notificações causados pelo "efeito fim de semana" das Secretarias Estaduais de Saúde (SES).

Visão Agregada e Estadual: Filtros dinâmicos que permitem alternar entre o panorama geral do Brasil ou selecionar uma Unidade Federativa (UF) específica.

Métricas Temporais: Separação analítica entre o acumulado histórico da pandemia e os casos/óbitos registrados estritamente no ano selecionado.

Ciclo de Notificação: A série temporal com registros diários consolidados pelas secretarias abrange o período da pandemia até o primeiro semestre de 2023, quando a OMS declarou o fim da Emergência de Saúde Pública e o monitoramento migrou para a rede sentinela (SIVEP-Gripe).

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o repositório
```bash
git clone https://github.com/celiovinicius-ds/Projeto_COVID.git
cd Projeto_COVID
```

### 2. Criar e ativar o ambiente virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências
```bash
pip install -r requirements.txt
```

### 4. Executar o Pipeline ETL
Rode o script orquestrador para extrair os dados da fonte pública, transformá-los e criar o banco de dados SQLite local:
```bash
python main.py
```

### 5. Iniciar o Dashboard Streamlit
```bash
streamlit run app.py
```
A aplicação abrirá automaticamente no navegador no endereço `http://localhost:8501`.
