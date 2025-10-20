import PyPDF2
import re

pdf_nome = 'ADM 0800100_0736_2025 de 30_09_2025.PDF'

with open(pdf_nome, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

contador = 0
total = 0
linhas_grandes = []
linhas_kg = []

print('='*130)
print('INSPECAO PDF 0736 - PROCURANDO TODAS AS LINHAS')
print('='*130 + '\n')

print(f"{'Nº':<5} {'Qtd':<10} {'Descrição':<100}\n")

for linha in lines:
    # Padrão com 'un'
    match_un = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
    # Padrão com 'kg'
    match_kg = re.match(r'^(\d+,\d+)\s+kg\s+(.+)$', linha)
    
    if match_un:
        qty_str = match_un.group(1).replace(',', '.')
        qtd = int(float(qty_str))
        description = match_un.group(2)
        
        contador += 1
        total += qtd
        
        if qtd >= 100:
            linhas_grandes.append((qtd, description[:70]))
            print(f"{contador:<5} {qtd:>8,d} {description[:100]} [GRANDE]")
        else:
            print(f"{contador:<5} {qtd:>8,d} {description[:100]}")
    
    elif match_kg:
        qty_str = match_kg.group(1).replace(',', '.')
        qtd = float(qty_str)
        description = match_kg.group(2)
        
        linhas_kg.append((qtd, description[:70]))
        print(f"{'KG':<5} {qtd:>8.2f}kg {description[:100]} [KG]")

print(f"\n{'-'*130}")
print(f"OK Total de linhas (un): {contador}")
print(f"OK Total de aparelhos (un): {total:,}")

if linhas_kg:
    print(f"\nAVISO Linhas em KG encontradas: {len(linhas_kg)}")
    total_kg = sum(q for q, _ in linhas_kg)
    print(f"    Total em KG: {total_kg:.2f}")
    for qtd, desc in linhas_kg:
        print(f"      * {qtd:.2f} kg - {desc}")

print(f"\nLinhas GRANDES (>= 100):")
if linhas_grandes:
    for qtd, desc in linhas_grandes:
        print(f"   * {qtd:,} un - {desc}")
    print(f"\n   SUBTOTAL das linhas grandes: {sum(q for q, _ in linhas_grandes):,} un")
else:
    print("   Nenhuma linha >= 100 encontrada")

print(f"\n{'='*130}\n")
