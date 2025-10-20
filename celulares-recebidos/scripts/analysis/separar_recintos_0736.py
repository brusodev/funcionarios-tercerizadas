import PyPDF2
import re

pdf_nome = 'ADM 0800100_0736_2025 de 30_09_2025.PDF'

with open(pdf_nome, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

# Patterns para recintos
padroes_recinto = {
    'Bauru (305)': r'305\s*-\s*810300',
    'Araraquara (16)': r'16\s*-\s*810900',
}

# Separar aparelhos por recinto
aparelhos_recinto = {}
recinto_atual = None

for linha in lines:
    # Verificar se é uma linha de recinto
    for nome_recinto, padrao in padroes_recinto.items():
        if re.search(padrao, linha):
            recinto_atual = nome_recinto
            aparelhos_recinto[recinto_atual] = 0
            break
    
    # Se encontrou um aparelho
    match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
    if match and recinto_atual:
        qty_str = match.group(1).replace(',', '.')
        qtd = int(float(qty_str))
        aparelhos_recinto[recinto_atual] += qtd

print("="*100)
print("Distribuicao de aparelhos por RECINTO em PDF 0736")
print("="*100 + "\n")

total_geral = 0
for recinto, total in aparelhos_recinto.items():
    print(f"{recinto}: {total:,} aparelhos")
    total_geral += total

print(f"\nTOTAL: {total_geral:,} aparelhos")
print("\n" + "="*100)
print(f"\nScript contou: 1,873 aparelhos (sem separar recintos)")
print(f"Voce contou: 3,058 aparelhos (pode ter separado por recinto)")
print(f"Diferenca: {3058 - total_geral:+,}")
print()
