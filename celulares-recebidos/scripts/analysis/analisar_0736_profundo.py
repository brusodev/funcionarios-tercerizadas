import PyPDF2
import re

pdf_nome = 'ADM 0800100_0736_2025 de 30_09_2025.PDF'

with open(pdf_nome, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    print(f"Total de pages no PDF: {len(reader.pages)}")
    
    text = ''
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        text += page_text
        print(f"Page {i+1}: {len(page_text)} caracteres")

print(f"\nTotal de caracteres: {len(text)}")

# Procurar por padrões de recinto
recintos = ['305 - 810300', '16 - 810900', '2 - DEPÓSITO', '1 - AEROPORTOS', '309 - 817900', 'Recinto', 'SAPOL']
for recinto in recintos:
    if recinto.lower() in text.lower():
        print(f"Encontrado: {recinto}")

# Contar linhas com "un"
matches = re.findall(r'^(\d+,\d+)\s+un\s+', text, re.MULTILINE)
print(f"\nTotal de linhas com 'un': {len(matches)}")

# Contar linhas com "kg"
kg_matches = re.findall(r'^(\d+,\d+)\s+kg\s+', text, re.MULTILINE)
print(f"Total de linhas com 'kg': {len(kg_matches)}")

# Procurar por outras unidades
outras_linhas = re.findall(r'^(\d+,\d+)\s+(\w+)\s+', text, re.MULTILINE)
unidades = set([u[1] for u in outras_linhas])
print(f"\nUnidades encontradas: {unidades}")

# Contar totais
total_un = sum(int(float(m.replace(',', '.'))) for m in matches)
total_kg = sum(float(m.replace(',', '.')) for m in kg_matches)

print(f"\nTotal em 'un': {total_un:,}")
print(f"Total em 'kg': {total_kg:.2f}")
if total_kg > 0:
    aparelhos_de_kg = int(total_kg / 0.5)
    print(f"Aparelhos de KG (convertidos): {aparelhos_de_kg:,}")
