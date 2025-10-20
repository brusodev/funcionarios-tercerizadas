import PyPDF2
import re

pdf_nome = 'ADM 0800100_0733_2025 de 30_09_2025.PDF'

with open(pdf_nome, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')
total = 0
encontrados = 0

for linha in lines:
    # Testar cada padrão
    m1 = re.match(r'^(\d+,\d+)\s+un\s+', linha)
    m2 = re.match(r'^(\d+\.\d+,\d+)\s+un\s+', linha)
    m3 = re.match(r'^(\d+,\d+)\s+kg\s+', linha)
    m4 = re.match(r'^(\d+\.\d+,\d+)\s+kg\s+', linha)
    
    if m1:
        qty_str = m1.group(1).replace(',', '.')
        qtd = int(float(qty_str))
        total += qtd
        encontrados += 1
        print(f'Pattern 1: {linha[:80]} = {qtd}')
    elif m2:
        qty_str = m2.group(1).replace('.', '').replace(',', '.')
        qtd = int(float(qty_str))
        total += qtd
        encontrados += 1
        print(f'Pattern 2: {linha[:80]} = {qtd}')
    elif m3:
        qty_str = m3.group(1).replace(',', '.')
        qtd_kg = float(qty_str)
        qtd = int(qtd_kg / 0.5)
        total += qtd
        encontrados += 1
        print(f'Pattern 3: {linha[:80]} = {qtd}')
    elif m4:
        qty_str = m4.group(1).replace('.', '').replace(',', '.')
        qtd_kg = float(qty_str)
        qtd = int(qtd_kg / 0.5)
        total += qtd
        encontrados += 1
        print(f'Pattern 4: {linha[:80]} = {qtd}')

print(f'\nTotal encontrado: {total:,}')
print(f'Linhas encontradas: {encontrados}')
