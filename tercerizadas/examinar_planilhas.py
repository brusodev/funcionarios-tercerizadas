import pandas as pd
import os

def examinar_planilha(arquivo):
    """Examina uma planilha Excel e mostra sua estrutura"""
    try:
        # Lê a planilha
        df = pd.read_excel(arquivo)
        
        print(f"\n=== ANÁLISE DA PLANILHA: {arquivo} ===")
        print(f"Dimensões: {df.shape[0]} linhas x {df.shape[1]} colunas")
        print(f"Colunas: {list(df.columns)}")
        
        print("\nPrimeiras 5 linhas:")
        print(df.head())
        
        print("\nInformações das colunas:")
        print(df.info())
        
        # Se existem as colunas esperadas, mostra valores únicos
        colunas_esperadas = ['nomes', 'tipo_manutencao', 'locais']
        for col in colunas_esperadas:
            if col in df.columns:
                print(f"\nValores únicos em '{col}':")
                valores_unicos = df[col].dropna().unique()
                print(f"Total: {len(valores_unicos)}")
                for i, valor in enumerate(valores_unicos[:10]):  # Primeiros 10
                    print(f"  - {valor}")
                if len(valores_unicos) > 10:
                    print(f"  ... e mais {len(valores_unicos) - 10} valores")
        
        return df
        
    except Exception as e:
        print(f"Erro ao ler {arquivo}: {e}")
        return None

# Examinar as planilhas
planilhas = ['manutencao_predios.xlsx', 'servicos_copas.xlsx']

dados = {}
for planilha in planilhas:
    if os.path.exists(planilha):
        dados[planilha] = examinar_planilha(planilha)
    else:
        print(f"Arquivo {planilha} não encontrado!")

print("\n" + "="*60)
print("RESUMO GERAL:")
print("="*60)

for arquivo, df in dados.items():
    if df is not None:
        print(f"\n{arquivo}:")
        print(f"  - {df.shape[0]} registros")
        print(f"  - Colunas: {list(df.columns)}")