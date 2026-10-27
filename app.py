import os
import sys
import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

# Garante que o diretório raiz está no caminho de módulos do Python
DIRETORIO_RAIZ = os.path.dirname(os.path.abspath(__file__))
if DIRETORIO_RAIZ not in sys.path:
    sys.path.insert(0, DIRETORIO_RAIZ)

st.set_page_config(page_title="Dashboard COVID-19", layout="wide")

@st.cache_data
def carregar_dados():
    caminho_banco = os.path.join(DIRETORIO_RAIZ, "data", "covid_brasil.db")
    
    # Se o banco não existir na nuvem, roda o pipeline ETL completo
    if not os.path.exists(caminho_banco):
        with st.spinner("Base de dados ausente. Baixando e processando dados pela primeira vez..."):
            os.makedirs(os.path.join(DIRETORIO_RAIZ, "data"), exist_ok=True)
            
            import etl.extract as extract
            import etl.transform as transform
            import etl.load as load
            
            # Chamada com o nome exato definido em etl/extract.py
            df_bruto = extract.extrair_dados_covid()
            df_tratado = transform.transformar_dados(df_bruto)
            load.carregar_dados_sqlite(df_tratado)

    conn = sqlite3.connect(caminho_banco)
    df = pd.read_sql("SELECT * FROM dados_covid", conn)
    conn.close()
    df['date'] = pd.to_datetime(df['date'])
    return df

df = carregar_dados()

# 3. Cabeçalho do Dashboard
st.title("🦠 Monitoramento da COVID-19 no Brasil")
st.markdown("Análise histórica interativa com tratamento de sazonalidade via Média Móvel de 7 dias.")

# 4. Barra lateral para Filtros (Sidebar)
st.sidebar.header("Filtros de Pesquisa")

lista_estados = ["Brasil (Geral)"] + sorted(list(df['state'].unique()))
local_selecionado = st.sidebar.selectbox("Selecione o Local / UF:", lista_estados)

# Agrupamento nacional ou filtro por UF específica
if local_selecionado == "Brasil (Geral)":
    df_local = (
        df.groupby(['date', 'ano', 'mes'], as_index=False)[['newCases', 'newDeaths', 'totalCases', 'deaths']]
        .sum()
    )
    df_local['state'] = "BR"
else:
    df_local = df[df['state'] == local_selecionado].copy()

# Ordenação cronológica obrigatória para o cálculo da média móvel
df_local = df_local.sort_values(by='date', ascending=True).reset_index(drop=True)

# Cálculo da Média Móvel de 7 dias
df_local['mm_casos'] = df_local['newCases'].rolling(window=7, min_periods=1).mean()
df_local['mm_obitos'] = df_local['newDeaths'].rolling(window=7, min_periods=1).mean()

# Filtro de Ano
lista_anos = sorted(list(df_local['ano'].unique()))
ano_selecionado = st.sidebar.selectbox("Selecione o Ano:", ["Todos"] + lista_anos)

if ano_selecionado != "Todos":
    df_filtrado = df_local[df_local['ano'] == ano_selecionado].copy()
else:
    df_filtrado = df_local.copy()

# 5. Apresentação de Métricas (Cartões de Resumo)
st.subheader(f"Resumo Geral - {local_selecionado} ({ano_selecionado})")

if not df_filtrado.empty:
    dados_recentes = df_filtrado.sort_values(by='date', ascending=False).iloc[0]
    casos_acumulados = int(dados_recentes['totalCases'])
    obitos_acumulados = int(dados_recentes['deaths'])
    
    if ano_selecionado == "Todos":
        col1, col2 = st.columns(2)
        col1.metric("Casos Acumulados (Total Histórico)", f"{casos_acumulados:,}".replace(",", "."))
        col2.metric("Óbitos Acumulados (Total Histórico)", f"{obitos_acumulados:,}".replace(",", "."))
    else:
        casos_ano = int(df_filtrado['newCases'].sum())
        obitos_ano = int(df_filtrado['newDeaths'].sum())
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(f"Casos em {ano_selecionado}", f"{casos_ano:,}".replace(",", "."))
        col2.metric(f"Óbitos em {ano_selecionado}", f"{obitos_ano:,}".replace(",", "."))
        col3.metric(f"Casos Acumulados (até {ano_selecionado})", f"{casos_acumulados:,}".replace(",", "."))
        col4.metric(f"Óbitos Acumulados (até {ano_selecionado})", f"{obitos_acumulados:,}".replace(",", "."))
else:
    st.warning("Não existem dados para os filtros selecionados.")

# 6. Gráficos Interativos
st.markdown("---")
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.subheader("Novos Casos e Média Móvel (7 dias)")
    fig_casos = go.Figure()
    fig_casos.add_trace(go.Bar(
        x=df_filtrado['date'], y=df_filtrado['newCases'],
        name='Registros Diários', marker_color='rgba(31, 119, 180, 0.3)'
    ))
    fig_casos.add_trace(go.Scatter(
        x=df_filtrado['date'], y=df_filtrado['mm_casos'],
        name='Média Móvel (7d)', line=dict(color='#1f77b4', width=2.5)
    ))
    fig_casos.update_layout(
        xaxis_title="Data", yaxis_title="Casos", hovermode="x unified",
        legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig_casos, use_container_width=True)

with col_grafico2:
    st.subheader("Novos Óbitos e Média Móvel (7 dias)")
    fig_obitos = go.Figure()
    fig_obitos.add_trace(go.Bar(
        x=df_filtrado['date'], y=df_filtrado['newDeaths'],
        name='Registros Diários', marker_color='rgba(214, 39, 40, 0.3)'
    ))
    fig_obitos.add_trace(go.Scatter(
        x=df_filtrado['date'], y=df_filtrado['mm_obitos'],
        name='Média Móvel (7d)', line=dict(color='#d62728', width=2.5)
    ))
    fig_obitos.update_layout(
        xaxis_title="Data", yaxis_title="Óbitos", hovermode="x unified",
        legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig_obitos, use_container_width=True)

# 7. Tabela Detalhada com Arredondamento Inteiro
st.markdown("---")
st.subheader("Tabela de Dados Diários (Mês a Mês)")

df_tabela = df_filtrado.sort_values(by='date', ascending=False).copy()
df_tabela = df_tabela[['date', 'mes', 'newCases', 'mm_casos', 'newDeaths', 'mm_obitos', 'totalCases', 'deaths']]
df_tabela.columns = [
    'Data', 'Mês', 'Novos Casos', 'Média Móvel Casos', 
    'Novos Óbitos', 'Média Móvel Óbitos', 'Casos Acumulados', 'Óbitos Acumulados'
]

# Formatação de datas
df_tabela['Data'] = df_tabela['Data'].dt.strftime('%d/%m/%Y')

# Arredondamento com proteção para nulos
df_tabela['Média Móvel Casos'] = df_tabela['Média Móvel Casos'].fillna(0).apply(lambda x: f"{int(round(x)):,}".replace(",", "."))
df_tabela['Média Móvel Óbitos'] = df_tabela['Média Móvel Óbitos'].fillna(0).apply(lambda x: f"{int(round(x)):,}".replace(",", "."))

for col in ['Novos Casos', 'Novos Óbitos', 'Casos Acumulados', 'Óbitos Acumulados']:
    df_tabela[col] = df_tabela[col].fillna(0).apply(lambda x: f"{int(x):,}".replace(",", "."))

st.dataframe(df_tabela, use_container_width=True, hide_index=True)