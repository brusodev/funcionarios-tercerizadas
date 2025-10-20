import PyPDF2
import re
import json
from collections import defaultdict

# Padrões dos recintos
padroes_recinto = {
    'Bauru': r'305\s*-\s*810300.*Bauru',
    'Araraquara': r'16\s*-\s*810900.*Araraquara',
    'São José': r'2\s*-\s*DEPÓSITO SAPOL.*SJR',
    'Viracopos': r'1\s*-\s*AEROPORTOS BRASIL VIRACOPOS',
    'Ipiranga': r'309\s*-\s*817900.*IPIRANGA'
}

# As 4 linhas EXATAS a remover - pelo PROCESSO (PROC.10835.726566/2024-81)
# Essas 4 linhas vão ser identificadas por conteúdo específico
aparelhos_remover = [
    ('XIAOMI REDMI NOTE 13 256GB CHINA', 692, 'PROC.10835.726566/2024-81'),
    ('XIAOMI REDMI NOTE 13 5G 256GB CHINA', 161, 'PROC.10835.726566/2024-81'),
    ('XIAOMI POCO C65 128GB INDIA', 119, 'PROC.10835.726566/2024-81'),
    ('XIAOMI REDMI NOTE 14 256GB CHINA', 206, 'PROC.10835.720548/2025-77'),
]

padrao_total = r'Total\s+do\s+ADM\s*:\s*R\$\s*([\d.]+,\d+)'

pdf_file = 'ADM 0800100_0735_2025 de 30_09_2025.PDF'

with open(pdf_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

print("=== ANÁLISE DETALHADA PDF 0735 ===\n")

# Contar com e sem as 4 duplicatas
aparelhos_com_duplicatas = defaultdict(int)
aparelhos_sem_duplicatas = defaultdict(int)
aparelhos_removidos = 0

recinto_atual = None

for i, linha in enumerate(lines):
    # Detectar mudança de recinto
    for nome_recinto, padrao in padroes_recinto.items():
        if re.search(padrao, linha):
            recinto_atual = nome_recinto
            break
    
    # Procurar linhas de aparelhos
    match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
    if match and recinto_atual:
        qty_str = match.group(1).replace(',', '.')
        qtd = int(float(qty_str))
        description = match.group(2)
        
        # COM DUPLICATAS
        aparelhos_com_duplicatas[recinto_atual] += qtd
        
        # Verificar se é uma das 4 duplicatas
        eh_duplicata = False
        for modelo, qty_esperada, processo in aparelhos_remover:
            if modelo in description and qtd == qty_esperada and processo in description:
                eh_duplicata = True
                print(f"❌ REMOVENDO: {qtd} un de {modelo}")
                print(f"   Linha: {description[:80]}")
                aparelhos_removidos += qtd
                break
        
        # SEM DUPLICATAS
        if not eh_duplicata:
            aparelhos_sem_duplicatas[recinto_atual] += qtd

print(f"\n{'='*60}")
print(f"RESUMO DO PDF 0735:")
print(f"{'='*60}")

print(f"\n📊 COM AS 4 DUPLICATAS:")
for recinto in sorted(aparelhos_com_duplicatas.keys()):
    print(f"   {recinto}: {aparelhos_com_duplicatas[recinto]:,} aparelhos")
total_com = sum(aparelhos_com_duplicatas.values())
print(f"   TOTAL: {total_com:,} aparelhos")

print(f"\n📊 SEM AS 4 DUPLICATAS:")
for recinto in sorted(aparelhos_sem_duplicatas.keys()):
    print(f"   {recinto}: {aparelhos_sem_duplicatas[recinto]:,} aparelhos")
total_sem = sum(aparelhos_sem_duplicatas.values())
print(f"   TOTAL: {total_sem:,} aparelhos")

print(f"\n🔍 DIFERENÇA:")
print(f"   Total com duplicatas: {total_com:,}")
print(f"   Total sem duplicatas: {total_sem:,}")
print(f"   Diferença: {total_com - total_sem:,}")
print(f"   Sua contagem: 3,804")
print(f"   Script com: 3,816 (Sua + {total_com - 3804})")
print(f"   Script sem: {total_sem} (Sua - {3804 - total_sem})")
