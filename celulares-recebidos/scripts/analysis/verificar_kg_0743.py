import PyPDF2
import re

pdf_nome = 'ADM 0800100_0743_2025 de 30_09_2025.PDF'

with open(pdf_nome, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

print("="*120)
print("PROCURANDO POR LINHAS EM KG NO PDF 0743")
print("="*120 + "\n")

linhas_kg = []
total_kg = 0
total_aparelhos_kg = 0

for i, linha in enumerate(lines):
    # Procurar por linhas com kg
    match_kg = re.match(r'^(\d+,\d+)\s+kg\s+(.+)$', linha)
    if match_kg:
        qty_kg_str = match_kg.group(1).replace(',', '.')
        qty_kg = float(qty_kg_str)
        description = match_kg.group(2)
        
        linhas_kg.append({
            'kg': qty_kg,
            'desc': description[:80],
            'linha': i
        })
        
        total_kg += qty_kg

print(f"Linhas em KG encontradas: {len(linhas_kg)}\n")

# Converter kg para aparelhos usando o critério correto
print("Conversao de KG para APARELHOS:")
print("Criterio: 0,49 kg = 1 aparelho; 1 kg = 2 aparelhos (arredondado)\n")

for i, item in enumerate(linhas_kg, 1):
    kg = item['kg']
    
    # Usar a proporcao: 0.49 kg = 1 aparelho
    # Portanto: 1 kg = 1 / 0.49 = 2.04 aparelhos ≈ 2
    aparelhos = round(kg / 0.49)
    
    print(f"{i}. {kg:.2f} kg = {aparelhos} aparelhos")
    print(f"   {item['desc']}")
    print()
    
    total_aparelhos_kg += aparelhos

print("="*120)
print(f"Total em KG: {total_kg:.2f} kg")
print(f"Total em APARELHOS (convertidos): {total_aparelhos_kg} aparelhos")
print()

# Agora contar linhas com "un"
print("="*120)
print("CONTANDO LINHAS COM 'UN':\n")

total_un = 0
linhas_un = 0

for linha in lines:
    # Padrão com "un" (simple e com ponto de milhar)
    match_un = re.match(r'^(\d+[\.,]?\d*,\d+)\s+un\s+', linha)
    if match_un:
        qty_str = match_un.group(1).replace('.', '').replace(',', '.')
        qtd = int(float(qty_str))
        total_un += qtd
        linhas_un += 1

print(f"Linhas com 'un': {linhas_un}")
print(f"Total em 'un': {total_un:,} aparelhos\n")

print("="*120)
print("TOTAL FINAL PDF 0743:\n")
print(f"Aparelhos em 'un':  {total_un:,}")
print(f"Aparelhos em 'kg':  {total_aparelhos_kg}")
print(f"TOTAL:              {total_un + total_aparelhos_kg:,} aparelhos")
print()
print(f"Sua contagem:       911 aparelhos")
print(f"Diferenca:          {911 - (total_un + total_aparelhos_kg):+d}")
print()
print("="*120 + "\n")
