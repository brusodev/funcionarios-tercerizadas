import pandas as pd
import re

# Lê a aba 743
df = pd.read_excel('analise_detalhada.xlsx', sheet_name='743')

print("="*80)
print("CONTANDO LINHAS COM VALOR R$ NA DESCRIÇÃO (PDF 0743)")
print("="*80)

coluna_a = df.iloc[:, 0]  # Quantidades
coluna_b = df.iloc[:, 1]  # Descrições

# Identifica linhas com quantidade
valores_a = pd.to_numeric(coluna_a, errors='coerce')
linhas_com_qtd = valores_a.notna()

# Identifica linhas que têm "R$" na descrição
linhas_com_valor_desc = coluna_b.astype(str).str.contains(r'R\$', na=False, regex=True)

# Combina: linhas com quantidade E com R$ na descrição
df_com_valor = df[linhas_com_qtd & linhas_com_valor_desc].copy()
df_com_valor['qtd_num'] = pd.to_numeric(df_com_valor.iloc[:, 0], errors='coerce')

total_aparelhos = df_com_valor['qtd_num'].sum()
total_linhas = len(df_com_valor)

print(f"\nLinhas com quantidade E valor R$ na descrição: {total_linhas}")
print(f"Soma das quantidades: {total_aparelhos}")

print(f"\n{'='*80}")
print("PRIMEIROS 50 EXEMPLOS:")
print(f"{'='*80}")

for i, (idx, row) in enumerate(df_com_valor.head(50).iterrows()):
    qtd = row.iloc[0]
    desc = str(row.iloc[1])
    
    # Extrai o valor R$
    match = re.search(r'R\$\s*([\d.,]+)', desc)
    valor_str = match.group(1) if match else "???"
    
    print(f"{i+1}. Linha {idx+2}: Qtd={qtd} | R$ {valor_str}")
    if i < 10:  # Mostra descrição completa dos primeiros 10
        print(f"   {desc[:120]}")

# Padrões nas linhas COM valor
print(f"\n{'='*80}")
print("PADRÕES nas linhas COM VALOR R$:")
print(f"{'='*80}")

padroes = {
    'IPHONE': 0,
    'SMARTPHONE': 0,
    'TELEFONE CELULAR': 0,
    'APARELHO CELULAR': 0,
    'CELULAR (sem prefixo)': 0
}

for idx, row in df_com_valor.iterrows():
    desc = str(row.iloc[1]).upper()
    
    if 'IPHONE' in desc:
        padroes['IPHONE'] += row['qtd_num']
    elif 'SMARTPHONE' in desc:
        padroes['SMARTPHONE'] += row['qtd_num']
    elif 'TELEFONE CELULAR' in desc or 'TELEFONE  CELULAR' in desc:
        padroes['TELEFONE CELULAR'] += row['qtd_num']
    elif 'APARELHO CELULAR' in desc or 'APARELHO  CELULAR' in desc:
        padroes['APARELHO CELULAR'] += row['qtd_num']
    elif 'CELULAR' in desc:
        padroes['CELULAR (sem prefixo)'] += row['qtd_num']

for padrao, count in padroes.items():
    if count > 0:
        print(f"   {padrao}: {count} aparelhos")

# Linhas SEM valor na descrição
df_sem_valor = df[linhas_com_qtd & ~linhas_com_valor_desc].copy()
df_sem_valor['qtd_num'] = pd.to_numeric(df_sem_valor.iloc[:, 0], errors='coerce')

total_sem_valor = df_sem_valor['qtd_num'].sum()

print(f"\n{'='*80}")
print("LINHAS COM QUANTIDADE mas SEM valor R$ na descrição:")
print(f"{'='*80}")
print(f"Total de linhas: {len(df_sem_valor)}")
print(f"Soma das quantidades: {total_sem_valor}")

print(f"\n⚠️ DIFERENÇA:")
print(f"   Esperado: 912 aparelhos")
print(f"   Encontrado (com R$ no Excel): {total_aparelhos}")
print(f"   Diferença: {912 - total_aparelhos}")
