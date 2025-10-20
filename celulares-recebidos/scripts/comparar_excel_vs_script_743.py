import pandas as pd
import PyPDF2
import re

def normalizar_quantidade(qtd_str):
    """Converte quantidade com vírgula para inteiro"""
    try:
        return int(float(str(qtd_str).replace(',', '.')))
    except:
        return 0

# Lê o Excel (413 linhas com soma = 912)
df_excel = pd.read_excel('analise_detalhada.xlsx', sheet_name='743')
coluna_a = df_excel.iloc[:, 0]
coluna_b = df_excel.iloc[:, 1]

# Linhas do Excel com quantidade
valores_excel = pd.to_numeric(coluna_a, errors='coerce')
excel_marcadas = df_excel[valores_excel.notna()].copy()
excel_marcadas['qtd'] = valores_excel[valores_excel.notna()]

print("="*80)
print("COMPARAÇÃO: EXCEL (912) vs SCRIPT (889)")
print("="*80)

print(f"\nEXCEL:")
print(f"   Linhas com quantidade: {len(excel_marcadas)}")
print(f"   Soma das quantidades: {excel_marcadas['qtd'].sum()}")

# Extrai do PDF usando o padrão V4
def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto_completo = []
        for pagina in leitor_pdf.pages:
            texto_completo.append(pagina.extract_text())
        return '\n'.join(texto_completo)

pdf_path = 'ADM 0800100_0743_2025 de 30_09_2025.PDF'
texto_pdf = extrair_texto_pdf(pdf_path)
linhas_pdf = texto_pdf.split('\n')

# Padrão V4
padrao_item = r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|APARELHO\s+CELULAR|IPHONE|(?<!TELEFONE\s)(?<!APARELHO\s)CELULAR).*)'
padrao_codigo = r'^\d+\s*-\s*\d+'

itens_pdf = []
for linha in linhas_pdf:
    linha = linha.strip()
    if not linha or re.match(padrao_codigo, linha):
        continue
    
    match = re.match(padrao_item, linha, re.IGNORECASE)
    if match:
        qtd_str = match.group(1)
        desc = match.group(2)
        qtd = normalizar_quantidade(qtd_str)
        itens_pdf.append({
            'qtd': qtd,
            'desc': desc[:100],
            'linha_pdf': linha[:150]
        })

total_pdf = sum(item['qtd'] for item in itens_pdf)

print(f"\nPDF (padrão V4):")
print(f"   Linhas encontradas: {len(itens_pdf)}")
print(f"   Soma das quantidades: {total_pdf}")

print(f"\nDIFERENÇA:")
print(f"   Linhas: {len(excel_marcadas)} (Excel) - {len(itens_pdf)} (PDF) = {len(excel_marcadas) - len(itens_pdf)}")
print(f"   Aparelhos: 912 (Excel) - {total_pdf} (PDF) = {912 - total_pdf}")

# Procura padrões que aparecem no Excel mas não no PDF
print(f"\n{'='*80}")
print("PROCURANDO PADRÕES QUE FALTAM NO SCRIPT:")
print(f"{'='*80}")

# Pega descrições do Excel
descricoes_excel = []
for idx, row in excel_marcadas.head(50).iterrows():
    desc = str(row.iloc[1])
    descricoes_excel.append(desc)

# Mostra exemplos do Excel
print(f"\nPRIMEIRAS 30 LINHAS DO EXCEL (que você marcou):")
for i, desc in enumerate(descricoes_excel[:30]):
    print(f"{i+1}. {desc[:120]}")

# Verifica quais padrões o script V4 captura
print(f"\n{'='*80}")
print("TESTANDO PADRÃO V4 NAS LINHAS DO EXCEL:")
print(f"{'='*80}")

capturados = 0
nao_capturados = []

for idx, row in excel_marcadas.iterrows():
    desc = str(row.iloc[1])
    qtd = row['qtd']
    
    # Testa se o padrão V4 captura
    match = re.match(padrao_item, desc, re.IGNORECASE)
    if match:
        capturados += qtd
    else:
        nao_capturados.append({
            'qtd': qtd,
            'desc': desc
        })

print(f"Capturados pelo padrão V4: {capturados} aparelhos")
print(f"NÃO capturados: {912 - capturados} aparelhos")

if nao_capturados:
    print(f"\n{'='*80}")
    print(f"EXEMPLOS DE LINHAS QUE O PADRÃO V4 NÃO CAPTURA:")
    print(f"{'='*80}")
    
    for i, item in enumerate(nao_capturados[:20]):
        print(f"\n{i+1}. Qtd={item['qtd']} | {item['desc'][:120]}")
