import pandas as pd

def transformar_dados(df):
    print("Iniciando a transformação dos dados...")
    
    # Remove a totalização nacional para manter apenas a granularidade estadual
    df = df[df['state'] != 'TOTAL'].copy()
    
    # Tratamento de datas
    df['date'] = pd.to_datetime(df['date'])
    df['ano'] = df['date'].dt.year
    df['mes'] = df['date'].dt.month
    
    # Seleção de colunas e tratamento de nulos
    colunas_uteis = ['date', 'ano', 'mes', 'state', 'newCases', 'newDeaths', 'totalCases', 'deaths']
    df_limpo = df[colunas_uteis].copy()
    df_limpo = df_limpo.fillna(0)
    
    print("Transformação concluída!")
    return df_limpo