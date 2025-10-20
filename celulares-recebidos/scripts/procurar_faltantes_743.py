import pandas as pd

# Lê a aba 743
df = pd.read_excel('analise_detalhada.xlsx', sheet_name='743')

print("="*80)
print("PROCURANDO OS 23 APARELHOS FALTANTES NO PDF 0743")
print("="*80)

# Total esperado: 912
# Total encontrado: 889
# Diferença: 23

coluna_a = df.iloc[:, 0]
coluna_b = df.iloc[:, 1]

# Analisa todas as linhas com quantidade
valores = pd.to_numeric(coluna_a, errors='coerce')
linhas_com_qtd = df[valores.notna()]

print(f"\nTotal de linhas com quantidade na coluna A: {len(linhas_com_qtd)}")
print(f"Soma total da coluna A: {valores.sum()}")

# Procura por diferentes padrões
padroes_a_verificar = [
    (r'\bkg\b', 'linhas com "kg"'),
    (r'^\d+,\d+ kg', 'linhas que começam com quantidade kg'),
    (r'AWB:', 'linhas com AWB'),
    (r'^\s*$', 'linhas vazias na coluna B'),
]

print("\n" + "="*80)
print("ANÁLISE DE PADRÕES:")
print("="*80)

for padrao, descricao in padroes_a_verificar:
    import re
    mask = coluna_b.astype(str).str.contains(padrao, na=False, regex=True)
    count = mask.sum()
    
    if count > 0:
        print(f"\n{descricao}: {count} linhas")
        
        # Mostra exemplos
        exemplos = df[mask].head(10)
        for idx, row in exemplos.iterrows():
            qtd = row.iloc[0]
            desc = str(row.iloc[1])[:100]
            print(f"   Linha {idx+2}: Qtd={qtd} | {desc}")

# Procura especificamente linhas com "kg"
print("\n" + "="*80)
print("LINHAS COM 'kg' (podem ser aparelhos em peso):")
print("="*80)

mask_kg = coluna_b.astype(str).str.contains(r'\bkg\b', na=False, regex=True)
linhas_kg = df[mask_kg]

qtds_kg = pd.to_numeric(linhas_kg.iloc[:, 0], errors='coerce')
total_kg = qtds_kg.dropna().sum()

print(f"Total de linhas: {len(linhas_kg)}")
print(f"Soma de quantidades: {total_kg}")

for idx, row in linhas_kg.iterrows():
    qtd = row.iloc[0]
    desc = str(row.iloc[1])
    print(f"\nLinha {idx+2}:")
    print(f"   Qtd: {qtd}")
    print(f"   Descrição: {desc}")

# Verifica se 912 é um subtotal específico
print("\n" + "="*80)
print("PROCURANDO VALOR '912' NO EXCEL:")
print("="*80)

# Procura por 912 em qualquer coluna
for col_idx in range(len(df.columns)):
    col = df.iloc[:, col_idx]
    for idx, val in col.items():
        if pd.notna(val):
            val_str = str(val)
            if '912' in val_str:
                print(f"\nEncontrado '912' na linha {idx+2}, coluna {chr(65+col_idx)}:")
                print(f"   Valor: {val}")
                # Mostra contexto (linhas ao redor)
                start = max(0, idx-2)
                end = min(len(df), idx+3)
                print(f"\n   Contexto (linhas {start+2} a {end+1}):")
                for i in range(start, end):
                    print(f"      Linha {i+2}: {df.iloc[i, 0]} | {df.iloc[i, 1] if len(df.iloc[i]) > 1 else ''}")
