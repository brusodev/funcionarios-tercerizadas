import pandas as pd

# Lê a aba 746
df = pd.read_excel('analise_detalhada.xlsx', sheet_name='746')

# Pega a coluna A (primeira coluna)
coluna_a = df.iloc[:, 0]

# Converte para numérico
valores = pd.to_numeric(coluna_a, errors='coerce')

# Remove NaN e soma
total = valores.dropna().sum()

print("="*80)
print("CONTAGEM MANUAL - ABA 746")
print("="*80)
print(f"Total de aparelhos (soma da coluna A): {int(total)}")
print()

# Procura especificamente pela linha com "5,00 un SMARTPHONE///"
coluna_b = df.iloc[:, 1]
mask_smartphone = coluna_b.astype(str).str.contains('5,00 un SMARTPHONE///', na=False, regex=False)

if mask_smartphone.any():
    linhas_smartphone = df[mask_smartphone]
    print("✓ Encontrada a linha problemática:")
    for idx, row in linhas_smartphone.iterrows():
        print(f"   Linha {idx+2} do Excel:")
        print(f"   Coluna A: {row.iloc[0]}")
        print(f"   Coluna B: {row.iloc[1]}")
        print()

# Mostra todas as linhas que têm apenas "SMARTPHONE" ou "CELULAR" sem modelo
print("Procurando outras linhas genéricas (sem modelo específico):")
print("-"*80)

# Padrões genéricos
padroes = [
    r'^\d+,\d+ un SMARTPHONE///',
    r'^\d+,\d+ un CELULAR [^/]*///',
    r'^\d+,\d+ un SMARTPHONE$',
    r'^\d+,\d+ un CELULAR$'
]

for padrao in padroes:
    mask = coluna_b.astype(str).str.match(padrao, na=False)
    if mask.any():
        print(f"\nPadrão: {padrao}")
        linhas = df[mask]
        for idx, row in linhas.iterrows():
            qtd = row.iloc[0]
            desc = row.iloc[1]
            print(f"   Linha {idx+2}: Qtd={qtd} | {desc[:80]}")
