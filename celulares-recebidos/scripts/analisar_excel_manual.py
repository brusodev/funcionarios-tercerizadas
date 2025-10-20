import pandas as pd
from pathlib import Path

def analisar_contagem_manual():
    """Analisa o arquivo de contagem manual do usuário"""
    
    arquivo = Path('analise_detalhada.xlsx')
    
    if not arquivo.exists():
        print(f"❌ Arquivo não encontrado: {arquivo}")
        return
    
    print("="*80)
    print("ANÁLISE DA CONTAGEM MANUAL (analise_detalhada.xlsx)")
    print("="*80)
    
    # Tenta ler o Excel
    try:
        # Lê todas as abas
        xls = pd.ExcelFile(arquivo)
        
        print(f"\n📊 Abas encontradas no arquivo:")
        for i, sheet in enumerate(xls.sheet_names, 1):
            print(f"   {i}. {sheet}")
        
        # Analisa cada aba
        for sheet_name in xls.sheet_names:
            print(f"\n{'='*80}")
            print(f"ABA: {sheet_name}")
            print(f"{'='*80}")
            
            df = pd.read_excel(arquivo, sheet_name=sheet_name)
            
            print(f"\n📋 Informações gerais:")
            print(f"   Total de linhas: {len(df)}")
            print(f"   Total de colunas: {len(df.columns)}")
            print(f"   Colunas: {list(df.columns)}")
            
            # Mostra primeiras linhas
            print(f"\n🔍 Primeiras 20 linhas:")
            print(df.head(20).to_string())
            
            # Analisa coluna A
            if len(df.columns) > 0:
                coluna_a = df.iloc[:, 0]  # Primeira coluna (índice 0 = coluna A)
                
                print(f"\n📊 ANÁLISE DA COLUNA A ({df.columns[0]}):")
                
                # Tenta identificar se são quantidades
                valores_numericos = pd.to_numeric(coluna_a, errors='coerce')
                valores_validos = valores_numericos.dropna()
                
                if len(valores_validos) > 0:
                    print(f"   Valores numéricos encontrados: {len(valores_validos)}")
                    print(f"   Soma total: {valores_validos.sum()}")
                    print(f"   Média: {valores_validos.mean():.2f}")
                    print(f"   Mínimo: {valores_validos.min()}")
                    print(f"   Máximo: {valores_validos.max()}")
                    
                    # Mostra alguns exemplos
                    print(f"\n   Exemplos de valores:")
                    for idx, val in valores_validos.head(10).items():
                        # Pega o conteúdo das outras colunas da mesma linha
                        linha_completa = df.iloc[idx]
                        print(f"      Linha {idx+2}: {val} | {linha_completa.to_dict()}")
                else:
                    print(f"   Tipo de dados: {coluna_a.dtype}")
                    print(f"   Valores únicos: {coluna_a.nunique()}")
                    print(f"\n   Primeiros valores:")
                    for idx, val in coluna_a.head(20).items():
                        print(f"      Linha {idx+2}: {val}")
            
            # Se tiver mais colunas, mostra também
            if len(df.columns) > 1:
                print(f"\n📋 Outras colunas:")
                for i, col in enumerate(df.columns[1:], 1):
                    print(f"   Coluna {chr(65+i)} ({col}):")
                    print(f"      Tipo: {df[col].dtype}")
                    print(f"      Valores não-nulos: {df[col].notna().sum()}")
                    if df[col].dtype in ['int64', 'float64']:
                        print(f"      Soma: {df[col].sum()}")
        
        # Procura especificamente pelo PDF 0746
        print(f"\n{'='*80}")
        print("PROCURANDO DADOS DO PDF 0746")
        print(f"{'='*80}")
        
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(arquivo, sheet_name=sheet_name)
            
            # Procura por "0746" em qualquer coluna
            for col in df.columns:
                if df[col].astype(str).str.contains('0746', na=False).any():
                    print(f"\n✓ Encontrado '0746' na aba '{sheet_name}', coluna '{col}'")
                    
                    # Mostra as linhas que contêm 0746
                    linhas_0746 = df[df[col].astype(str).str.contains('0746', na=False)]
                    print(f"   Total de linhas com '0746': {len(linhas_0746)}")
                    
                    if len(linhas_0746) > 0:
                        print(f"\n   Primeiras linhas:")
                        print(linhas_0746.head(10).to_string())
                        
                        # Se tiver coluna A com números, soma
                        if len(linhas_0746.columns) > 0:
                            primeira_col = linhas_0746.iloc[:, 0]
                            nums = pd.to_numeric(primeira_col, errors='coerce')
                            total = nums.sum()
                            if total > 0:
                                print(f"\n   ✅ TOTAL DA COLUNA A (para linhas com 0746): {total}")
    
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analisar_contagem_manual()
