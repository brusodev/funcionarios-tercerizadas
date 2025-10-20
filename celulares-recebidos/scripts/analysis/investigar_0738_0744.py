import PyPDF2
import re

# Analisar PDF 0738 (diferença de +2)
print("="*80)
print("🔍 ANÁLISE PDF 0738 (Script: 444, Você: 442, Diferença: +2)")
print("="*80 + "\n")

pdf_file = 'ADM 0800100_0738_2025 de 30_09_2025.PDF'

with open(pdf_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

# Procurar TODAS as linhas de quantidade (não só "un")
print("LINHAS COM QUANTIDADES (TODOS OS TIPOS):\n")

count_un = 0
count_outros = 0
linhas_especiais = []

for i, linha in enumerate(lines):
    # Padrão normal: N,NN un DESCRIÇÃO
    match_un = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
    if match_un:
        qty_str = match_un.group(1).replace(',', '.')
        qtd = int(float(qty_str))
        count_un += qtd
    
    # Procurar outros padrões
    match_outro = re.search(r'^(\d+,\d+)\s+(kg|lote|LOTE|caixa|CAIXA|pç|Pç|lata|LATA|PACOTE|pacote|FARDO|fardo)\s+', linha)
    if match_outro:
        qty_str = match_outro.group(1).replace(',', '.')
        qtd = float(qty_str)
        unidade = match_outro.group(2)
        linhas_especiais.append({
            'linha': i,
            'qtd': qtd,
            'unidade': unidade,
            'descricao': linha[:80]
        })
        count_outros += int(qtd)

print(f"Total em 'un': {count_un}")
print(f"Total em outras unidades: {count_outros}")
print(f"TOTAL GERAL: {count_un + count_outros}\n")

if linhas_especiais:
    print(f"LINHAS COM UNIDADES ESPECIAIS ({len(linhas_especiais)}):\n")
    for item in linhas_especiais:
        print(f"  Linha {item['linha']}: {item['qtd']:.2f} {item['unidade']}")
        print(f"  └─ {item['descricao']}\n")
else:
    print("Nenhuma linha com unidades especiais encontrada\n")

# Procurar linhas que começam com número mas não têm "un"
print("\nPROCURANDO LINHAS ANÔMALAS (começam com número mas sem padrão un):\n")

anomalas = []
for i, linha in enumerate(lines):
    match = re.match(r'^(\d+,\d+)\s+(.+)$', linha)
    if match:
        depois = match.group(2)
        # Se NÃO contém "un" nos primeiros 30 caracteres
        if 'un ' not in depois[:30]:
            anomalas.append({
                'linha': i,
                'qtd': match.group(1),
                'descricao': depois[:80]
            })

if anomalas:
    print(f"Encontradas {len(anomalas)} linhas anômalas:\n")
    for item in anomalas[:5]:
        print(f"  Linha {item['linha']}: {item['qtd']} {item['descricao']}")
else:
    print("Nenhuma linha anômala encontrada")

print("\n" + "="*80)
print("🔍 ANÁLISE PDF 0744 (Script: 3,458, Você: 3,457, Diferença: +1)")
print("="*80 + "\n")

pdf_file = 'ADM 0800100_0744_2025 de 30_09_2025.PDF'

with open(pdf_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

print("LINHAS COM QUANTIDADES:\n")

count_un = 0
count_outros = 0
linhas_especiais = []
anomalas = []

for i, linha in enumerate(lines):
    # Padrão normal: N,NN un DESCRIÇÃO
    match_un = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
    if match_un:
        qty_str = match_un.group(1).replace(',', '.')
        qtd = int(float(qty_str))
        count_un += qtd
    
    # Procurar outros padrões
    match_outro = re.search(r'^(\d+,\d+)\s+(kg|lote|LOTE|caixa|CAIXA|pç|Pç|lata|LATA|PACOTE|pacote|FARDO|fardo)\s+', linha)
    if match_outro:
        qty_str = match_outro.group(1).replace(',', '.')
        qtd = float(qty_str)
        unidade = match_outro.group(2)
        linhas_especiais.append({
            'qtd': qtd,
            'unidade': unidade,
            'descricao': linha[:80]
        })
    
    # Procurar anômalas
    match = re.match(r'^(\d+,\d+)\s+(.+)$', linha)
    if match:
        depois = match.group(2)
        if 'un ' not in depois[:30]:
            anomalas.append({
                'linha': i,
                'qtd': match.group(1),
                'descricao': depois[:80]
            })

print(f"Total em 'un': {count_un}")
print(f"Total em outras unidades: {len(linhas_especiais)}")
print(f"TOTAL GERAL: {count_un}\n")

if anomalas:
    print(f"LINHAS ANÔMALAS ({len(anomalas)}):\n")
    for item in anomalas[:10]:
        print(f"  Linha {item['linha']}: {item['qtd']} {item['descricao']}")
else:
    print("Nenhuma linha anômala encontrada")
