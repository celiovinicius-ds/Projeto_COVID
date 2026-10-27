from etl.extract import extrair_dados_covid
from etl.transform import transformar_dados
from etl.load import carregar_dados_sqlite

def run_pipeline():
    print("=== INICIANDO PIPELINE ETL COVID-19 ===")
    
    # Step 1: Extract
    df_bruto = extrair_dados_covid()
    if df_bruto is None:
        print("Pipeline interrompido na etapa de extração.")
        return
        
    # Step 2: Transform
    df_pronto = transformar_dados(df_bruto)
    
    # Step 3: Load
    carregar_dados_sqlite(df_pronto)
    
    print("=== PIPELINE FINALIZADO COM SUCESSO ===")

if __name__ == "__main__":
    run_pipeline()