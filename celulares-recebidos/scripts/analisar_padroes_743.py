import pandas as pd

# Lê a aba 743
df = pd.read_excel('analise_detalhada.xlsx', sheet_name='743')

print("="*80)
print("ANÁLISE DAS PRIMEIRAS 50 LINHAS - ABA 743")
print("="*80)

# Mostra as primeiras 50 linhas
for idx in range(min(50, len(df))):
    row = df.iloc[idx]
    col_a = row.iloc[0]
    col_b = row.iloc[1] if len(row) > 1 else ""
    
    print(f"\nLinha {idx+2}:")
    print(f"   Coluna A: {col_a}")
    print(f"   Coluna B: {col_b}")

# Procura por padrões específicos
print("\n" + "="*80)
print("PADRÕES ENCONTRADOS:")
print("="*80)

coluna_b = df.iloc[:, 1]

# Conta diferentes padrões
padroes = {
    'APARELHO CELULAR': 0,
    'IPHONE': 0,
    'SMARTPHONE': 0,
    'TELEFONE CELULAR': 0,
    'CELULAR': 0
}

linhas_por_padrao = {k: [] for k in padroes.keys()}

for idx, texto in coluna_b.items():
    if pd.notna(texto):
        texto_str = str(texto).upper()
        
        if 'APARELHO CELULAR' in texto_str:
            padroes['APARELHO CELULAR'] += 1
            if padroes['APARELHO CELULAR'] <= 10:
                qtd = df.iloc[idx, 0]
                linhas_por_padrao['APARELHO CELULAR'].append(f"Linha {idx+2}: Qtd={qtd} | {str(texto)[:80]}")
        elif 'IPHONE' in texto_str:
            padroes['IPHONE'] += 1
            if padroes['IPHONE'] <= 10:
                qtd = df.iloc[idx, 0]
                linhas_por_padrao['IPHONE'].append(f"Linha {idx+2}: Qtd={qtd} | {str(texto)[:80]}")
        elif 'SMARTPHONE' in texto_str:
            padroes['SMARTPHONE'] += 1
            if padroes['SMARTPHONE'] <= 10:
                qtd = df.iloc[idx, 0]
                linhas_por_padrao['SMARTPHONE'].append(f"Linha {idx+2}: Qtd={qtd} | {str(texto)[:80]}")
        elif 'TELEFONE CELULAR' in texto_str:
            padroes['TELEFONE CELULAR'] += 1
            if padroes['TELEFONE CELULAR'] <= 10:
                qtd = df.iloc[idx, 0]
                linhas_por_padrao['TELEFONE CELULAR'].append(f"Linha {idx+2}: Qtd={qtd} | {str(texto)[:80]}")
        elif 'CELULAR' in texto_str:
            padroes['CELULAR'] += 1
            if padroes['CELULAR'] <= 10:
                qtd = df.iloc[idx, 0]
                linhas_por_padrao['CELULAR'].append(f"Linha {idx+2}: Qtd={qtd} | {str(texto)[:80]}")

print("\nContagem por tipo:")
for padrao, count in padroes.items():
    print(f"   {padrao}: {count} linhas")

print("\nExemplos de cada tipo:")
for padrao, linhas in linhas_por_padrao.items():
    if linhas:
        print(f"\n{padrao}:")
        for linha in linhas:
            print(f"   {linha}")

# Procura especificamente por linhas sem "un"
print("\n" + "="*80)
print("LINHAS SEM 'un' mas com quantidade na coluna A:")
print("="*80)

coluna_a = df.iloc[:, 0]
sem_un = []

for idx, row in df.iterrows():
    qtd = row.iloc[0]
    texto = row.iloc[1] if len(row) > 1 else ""
    
    if pd.notna(qtd) and pd.notna(texto):
        texto_str = str(texto).lower()
        # Tem quantidade mas não tem "un"
        if ' un ' not in texto_str and not texto_str.startswith('un '):
            if any(palavra in texto_str for palavra in ['iphone', 'celular', 'smartphone']):
                sem_un.append(f"Linha {idx+2}: Qtd={qtd} | {str(texto)[:80]}")

if sem_un:
    print(f"\nTotal de linhas sem 'un': {len(sem_un)}")
    print("\nPrimeiras 20:")
    for linha in sem_un[:20]:
        print(f"   {linha}")
