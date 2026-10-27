import pandas as pd

def extrair_dados_covid():
    print("Iniciando a extração dos dados da web...")
    url_fonte = "https://raw.githubusercontent.com/wcota/covid19br/master/cases-brazil-states.csv"
    
    try:
        df = pd.read_csv(url_fonte)
        print("Extração concluída com sucesso!")
        return df
    except Exception as e:
        print(f"Erro na extração dos dados: {e}")
        return None