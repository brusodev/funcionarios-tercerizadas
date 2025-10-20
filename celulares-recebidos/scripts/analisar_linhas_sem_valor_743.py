import pandas as pd

# Lê a aba 743
df = pd.read_excel('analise_detalhada.xlsx', sheet_name='743')

print("="*80)
print("ANÁLISE: LINHAS COM VS SEM VALOR NO EXCEL (PDF 0743)")
print("="*80)

coluna_a = df.iloc[:, 0]  # Quantidades
coluna_b = df.iloc[:, 1]  # Descrições
coluna_c = df.iloc[:, 2] if len(df.columns) > 2 else None  # Valores (R$)

# Identifica linhas com quantidade NA coluna A
valores_a = pd.to_numeric(coluna_a, errors='coerce')
linhas_com_qtd = valores_a.notna()

print(f"\nTotal de linhas com quantidade na coluna A: {linhas_com_qtd.sum()}")

if coluna_c is not None:
    # Identifica quais têm valor na coluna C (você marcou como válido)
    valores_c = pd.to_numeric(coluna_c, errors='coerce')
    linhas_com_valor = valores_c.notna()
    
    print(f"Linhas com VALOR na coluna C (você marcou): {linhas_com_valor.sum()}")
    print(f"Linhas SEM valor na coluna C (você NÃO marcou): {(linhas_com_qtd & ~linhas_com_valor).sum()}")
    
    # Soma das quantidades marcadas
    soma_marcadas = valores_a[linhas_com_valor].sum()
    print(f"\nSoma das QUANTIDADES marcadas com valor: {soma_marcadas}")
    
    # Linhas que VOCÊ marcou (com quantidade E com valor)
    df_marcadas = df[linhas_com_qtd & linhas_com_valor].copy()
    df_marcadas['qtd_num'] = pd.to_numeric(df_marcadas.iloc[:, 0], errors='coerce')
    
    print(f"\n{'='*80}")
    print("LINHAS QUE VOCÊ MARCOU COMO VÁLIDAS:")
    print(f"{'='*80}")
    print(f"Total de linhas: {len(df_marcadas)}")
    print(f"Soma das quantidades: {df_marcadas['qtd_num'].sum()}")
    
    # Analisa padrões nas linhas marcadas
    print(f"\nPADRÕES nas linhas MARCADAS:")
    padroes = {
        'IPHONE': 0,
        'SMARTPHONE': 0,
        'TELEFONE CELULAR': 0,
        'APARELHO CELULAR': 0,
        'CELULAR (sem prefixo)': 0,
        'Outros': 0
    }
    
    for idx, row in df_marcadas.iterrows():
        desc = str(row.iloc[1]).upper()
        
        if 'IPHONE' in desc:
            padroes['IPHONE'] += 1
        elif 'SMARTPHONE' in desc:
            padroes['SMARTPHONE'] += 1
        elif 'TELEFONE CELULAR' in desc or 'TELEFONE  CELULAR' in desc:
            padroes['TELEFONE CELULAR'] += 1
        elif 'APARELHO CELULAR' in desc or 'APARELHO  CELULAR' in desc:
            padroes['APARELHO CELULAR'] += 1
        elif 'CELULAR' in desc:
            padroes['CELULAR (sem prefixo)'] += 1
        else:
            padroes['Outros'] += 1
    
    for padrao, count in padroes.items():
        if count > 0:
            print(f"   {padrao}: {count} linhas")
    
    # Linhas que VOCÊ NÃO marcou (têm quantidade mas não têm valor)
    df_nao_marcadas = df[linhas_com_qtd & ~linhas_com_valor].copy()
    df_nao_marcadas['qtd_num'] = pd.to_numeric(df_nao_marcadas.iloc[:, 0], errors='coerce')
    
    print(f"\n{'='*80}")
    print("LINHAS QUE VOCÊ NÃO MARCOU (têm qtd mas não têm valor):")
    print(f"{'='*80}")
    print(f"Total de linhas: {len(df_nao_marcadas)}")
    print(f"Soma das quantidades: {df_nao_marcadas['qtd_num'].sum()}")
    
    # Mostra exemplos das não marcadas
    print(f"\nPrimeiros 30 exemplos de linhas NÃO MARCADAS:")
    for i, (idx, row) in enumerate(df_nao_marcadas.head(30).iterrows()):
        qtd = row.iloc[0]
        desc = str(row.iloc[1])[:120]
        print(f"{i+1}. Linha {idx+2}: Qtd={qtd} | {desc}")
    
    # Procura padrões nas não marcadas
    print(f"\n{'='*80}")
    print("PADRÕES nas linhas NÃO MARCADAS:")
    print(f"{'='*80}")
    
    padroes_nao_marcadas = {
        'IPHONE': 0,
        'SMARTPHONE': 0,
        'TELEFONE CELULAR': 0,
        'APARELHO CELULAR': 0,
        'CELULAR (sem prefixo)': 0,
        'TABLET': 0,
        'BATERIA': 0,
        'CARREGADOR': 0,
        'FONE': 0,
        'CAPA': 0,
        'CABO': 0,
        'Outros': 0
    }
    
    for idx, row in df_nao_marcadas.iterrows():
        desc = str(row.iloc[1]).upper()
        
        if 'IPHONE' in desc:
            padroes_nao_marcadas['IPHONE'] += 1
        elif 'SMARTPHONE' in desc:
            padroes_nao_marcadas['SMARTPHONE'] += 1
        elif 'TELEFONE CELULAR' in desc or 'TELEFONE  CELULAR' in desc:
            padroes_nao_marcadas['TELEFONE CELULAR'] += 1
        elif 'APARELHO CELULAR' in desc or 'APARELHO  CELULAR' in desc:
            padroes_nao_marcadas['APARELHO CELULAR'] += 1
        elif 'CELULAR' in desc:
            padroes_nao_marcadas['CELULAR (sem prefixo)'] += 1
        elif 'TABLET' in desc:
            padroes_nao_marcadas['TABLET'] += 1
        elif 'BATERIA' in desc:
            padroes_nao_marcadas['BATERIA'] += 1
        elif 'CARREGADOR' in desc:
            padroes_nao_marcadas['CARREGADOR'] += 1
        elif 'FONE' in desc or 'HEADPHONE' in desc:
            padroes_nao_marcadas['FONE'] += 1
        elif 'CAPA' in desc or 'CASE' in desc:
            padroes_nao_marcadas['CAPA'] += 1
        elif 'CABO' in desc:
            padroes_nao_marcadas['CABO'] += 1
        else:
            padroes_nao_marcadas['Outros'] += 1
    
    for padrao, count in padroes_nao_marcadas.items():
        if count > 0:
            print(f"   {padrao}: {count} linhas")
    
    # Se há celulares não marcados, mostra exemplos
    if padroes_nao_marcadas['IPHONE'] + padroes_nao_marcadas['SMARTPHONE'] + padroes_nao_marcadas['TELEFONE CELULAR'] + padroes_nao_marcadas['APARELHO CELULAR'] + padroes_nao_marcadas['CELULAR (sem prefixo)'] > 0:
        print(f"\n{'='*80}")
        print("⚠️ ATENÇÃO: Há aparelhos CELULARES que você NÃO marcou!")
        print(f"{'='*80}")
        
        for idx, row in df_nao_marcadas.iterrows():
            desc = str(row.iloc[1]).upper()
            if any(palavra in desc for palavra in ['IPHONE', 'SMARTPHONE', 'TELEFONE CELULAR', 'APARELHO CELULAR', 'CELULAR']):
                qtd = row.iloc[0]
                desc_original = str(row.iloc[1])[:120]
                print(f"Linha {idx+2}: Qtd={qtd} | {desc_original}")

else:
    print("\n⚠️ Não há coluna C (valores) no Excel, impossível determinar quais você marcou")
