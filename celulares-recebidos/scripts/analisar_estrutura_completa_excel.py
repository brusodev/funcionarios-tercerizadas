import pandas as pd

# Abre o Excel e lista TODAS as abas com detalhes
excel_file = pd.ExcelFile('analise_detalhada.xlsx')

print("="*80)
print("ESTRUTURA COMPLETA DO EXCEL")
print("="*80)

print(f"\nTotal de abas: {len(excel_file.sheet_names)}")

for i, aba in enumerate(excel_file.sheet_names):
    print(f"\n{'='*80}")
    print(f"ABA {i+1}: '{aba}'")
    print(f"{'='*80}")
    
    # Lê a aba
    df = pd.read_excel('analise_detalhada.xlsx', sheet_name=aba)
    
    print(f"Dimensões: {len(df)} linhas x {len(df.columns)} colunas")
    
    # Analisa coluna A
    coluna_a = df.iloc[:, 0]
    valores_a = pd.to_numeric(coluna_a, errors='coerce')
    
    linhas_com_qtd = valores_a.notna().sum()
    soma_qtd = valores_a.sum()
    
    print(f"\nColuna A:")
    print(f"   Linhas com quantidade: {linhas_com_qtd}")
    print(f"   Soma das quantidades: {int(soma_qtd) if pd.notna(soma_qtd) else 0}")
    
    # Mostra header da coluna B (se tiver info útil)
    if len(df.columns) > 1:
        header_b = df.columns[1]
        print(f"\nHeader coluna B: {header_b}")
        
        # Tenta extrair número do PDF do header
        import re
        match = re.search(r'(\d{7})', str(header_b))
        if match:
            numero_encontrado = match.group(1)
            print(f"   Número encontrado no header: {numero_encontrado}")
    
    # Mostra primeiras 3 linhas
    print(f"\nPrimeiras 3 linhas:")
    for idx in range(min(3, len(df))):
        row = df.iloc[idx]
        qtd = row.iloc[0] if pd.notna(row.iloc[0]) else "nan"
        desc = str(row.iloc[1])[:80] if len(row) > 1 and pd.notna(row.iloc[1]) else "nan"
        print(f"   Linha {idx+2}: {qtd} | {desc}")

print(f"\n{'='*80}")
print("RESUMO:")
print(f"{'='*80}")

for aba in excel_file.sheet_names:
    df = pd.read_excel('analise_detalhada.xlsx', sheet_name=aba)
    coluna_a = df.iloc[:, 0]
    valores_a = pd.to_numeric(coluna_a, errors='coerce')
    soma = valores_a.sum()
    
    print(f"Aba '{aba}': {int(soma) if pd.notna(soma) else 0} aparelhos")
