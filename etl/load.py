import sqlite3
import os

def carregar_dados_sqlite(df, db_path="data/covid_brasil.db"):
    print(f"Iniciando o carregamento dos dados no banco: {db_path}...")
    
    # Cria a pasta 'data' automaticamente caso ela ainda não exista no projeto
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql('dados_covid', conn, if_exists='replace', index=False)
        print("Dados salvos com sucesso na base de dados!")
    except Exception as e:
        print(f"Erro ao salvar no banco de dados: {e}")
    finally:
        if 'conn' in locals():
            conn.close()