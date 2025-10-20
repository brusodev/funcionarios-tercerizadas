import PyPDF2
import re

pdf_file = 'ADM 0800100_0735_2025 de 30_09_2025.PDF'

with open(pdf_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

# Procurar as 4 linhas específicas com REGEX mais tolerante
print("=== PROCURA PELAS 4 LINHAS DUPLICADAS ===\n")

padroes = [
    (r'692.*XIAOMI REDMI NOTE 13 256GB CHINA.*NR DE SERIE', '692 un'),
    (r'161.*XIAOMI REDMI NOTE 13 5G.*256GB CHINA.*NR DE SERIE', '161 un'),
    (r'119.*XIAOMI POCO C65 128GB INDIA.*NR DE SERIE', '119 un'),
    (r'206.*XIAOMI REDMI NOTE 14 256GB CHINA.*NR DE SERIE', '206 un'),
]

for padrao_str, label in padroes:
    found = False
    for i, linha in enumerate(lines):
        if re.search(padrao_str, linha, re.IGNORECASE):
            print(f"✅ ENCONTRADA: {label}")
            print(f"   Linha {i}: {linha[:100]}")
            found = True
            break
    if not found:
        print(f"❌ NÃO ENCONTRADA: {label}")

print("\n" + "="*60)
print("=== BUSCA ALTERNATIVA: TODAS AS LINHAS COM,00 un ===\n")

for i, linha in enumerate(lines):
    match = re.match(r'^(\d+),00 un\s+(.+)$', linha)
    if match:
        qtd = int(match.group(1))
        desc = match.group(2)[:60]
        if qtd >= 100:  # Apenas as grandes
            print(f"Linha {i}: {qtd:4d} un - {desc}")
