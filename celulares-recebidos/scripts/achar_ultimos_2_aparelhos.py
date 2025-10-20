import pandas as pd
import PyPDF2
import re

def normalizar_quantidade(qtd_str):
    try:
        return int(float(str(qtd_str).replace(',', '.')))
    except:
        return 0

# Lê o Excel
df_excel = pd.read_excel('analise_detalhada.xlsx', sheet_name='743')
coluna_a = df_excel.iloc[:, 0]
coluna_b = df_excel.iloc[:, 1]

valores_excel = pd.to_numeric(coluna_a, errors='coerce')
excel_marcadas = df_excel[valores_excel.notna()].copy()
excel_marcadas['qtd'] = valores_excel[valores_excel.notna()]

print("="*80)
print("PROCURANDO OS 2 APARELHOS FINAIS (PDF 0743)")
print("="*80)

# Padrão V5
padrao_v5 = r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|APARELHO\s+CELULAR|IPHONE|(?<!TELEFONE\s)(?<!APARELHO\s)CELULAR|(?:REDMI|NOTE|POCO|POCOPHONE|MI)\s+\d+).*)'

nao_capturados = []
capturados_total = 0

for idx, row in excel_marcadas.iterrows():
    desc = str(row.iloc[1])
    qtd = row['qtd']
    
    # Testa se o padrão V5 captura
    match = re.match(padrao_v5, desc, re.IGNORECASE)
    if match:
        capturados_total += qtd
    else:
        nao_capturados.append({
            'linha_excel': idx + 2,
            'qtd': qtd,
            'desc': desc
        })

print(f"Total capturado pelo V5: {capturados_total}")
print(f"Total NÃO capturado: {912 - capturados_total}")
print(f"Número de linhas NÃO capturadas: {len(nao_capturados)}")

if nao_capturados:
    print(f"\n{'='*80}")
    print(f"TODAS AS LINHAS QUE O PADRÃO V5 NÃO CAPTURA:")
    print(f"{'='*80}")
    
    for i, item in enumerate(nao_capturados):
        print(f"\n{i+1}. Linha Excel {item['linha_excel']}: Qtd={item['qtd']}")
        print(f"   {item['desc']}")
        
        # Analisa o que está faltando
        desc_upper = item['desc'].upper()
        
        if 'NOTE' in desc_upper and not re.search(r'\bNOTE\s+\d+', desc_upper):
            print(f"   ⚠️ Tem 'NOTE' mas não está no padrão 'NOTE <número>'")
        
        if 'REDMI' in desc_upper and not re.search(r'\bREDMI\s+\d+', desc_upper):
            print(f"   ⚠️ Tem 'REDMI' mas não está no padrão 'REDMI <número>'")
        
        # Testa diferentes variações
        if item['desc'].strip().startswith(('1,00', '2,00', '3,00', '4,00', '5,00')):
            # Extrai a parte após "un"
            match_un = re.match(r'(\d+,\d+)\s+(un|kg)\s+(.*)', item['desc'])
            if match_un:
                resto = match_un.group(3)
                print(f"   📝 Depois do 'un': {resto}")
                
                # Verifica se é um padrão conhecido
                if not any(palavra in resto.upper() for palavra in 
                          ['SMARTPHONE', 'TELEFONE', 'CELULAR', 'IPHONE', 'APARELHO', 'NOTE', 'REDMI', 'POCO', 'MI']):
                    print(f"   ❌ Nenhum padrão conhecido encontrado!")
                    
                    # Tenta identificar o que é
                    palavras = resto.split()
                    if palavras:
                        primeira_palavra = palavras[0].upper()
                        print(f"   🔍 Primeira palavra: '{primeira_palavra}'")

print(f"\n{'='*80}")
print(f"RESUMO:")
print(f"   Excel: 912 aparelhos")
print(f"   V5 captura: {capturados_total} aparelhos")
print(f"   Diferença: {912 - capturados_total} aparelhos")
print(f"{'='*80}")
