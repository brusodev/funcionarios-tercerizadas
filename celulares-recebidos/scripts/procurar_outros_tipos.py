import PyPDF2
import re

# Ler o PDF
pdf_path = "ADM 0800100_0745_2025 de 30_09_2025.PDF"

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    texto_completo = []
    for page in reader.pages:
        texto_completo.append(page.extract_text())

texto = '\n'.join(texto_completo)
linhas = texto.split('\n')

print("="*80)
print("PROCURANDO OUTROS TIPOS DE APARELHOS")
print("="*80)

# Padrões alternativos
patterns = [
    (r'^\d+,\d+\s+un\s+SMARTPHONE', 'SMARTPHONE'),
    (r'^\d+,\d+\s+un\s+TELEFONE\s+CELULAR', 'TELEFONE CELULAR'),
    (r'^\d+,\d+\s+un\s+APARELHO', 'APARELHO'),
    (r'^\d+,\d+\s+un\s+IPHONE', 'IPHONE'),
    (r'^\d+,\d+\s+un\s+CELULAR', 'CELULAR (standalone)'),
]

resultados = {}

for pattern_str, tipo in patterns:
    pattern = re.compile(pattern_str, re.IGNORECASE)
    count = 0
    for linha in linhas:
        if pattern.match(linha.strip()):
            count += 1
    resultados[tipo] = count

print("\nTipos de aparelhos encontrados:")
for tipo, count in sorted(resultados.items(), key=lambda x: x[1], reverse=True):
    print(f"  {tipo}: {count:,}".replace(',', '.'))

# Buscar TODOS os padrões que começam com quantidade
print(f"\n{'='*80}")
print("PRIMEIRAS 50 LINHAS COM PADRÃO: 'X,XX un ...'")
print("="*80)

pattern_generico = re.compile(r'^(\d+,\d+)\s+un\s+(.+)', re.IGNORECASE)

exemplos = []
for i, linha in enumerate(linhas):
    match = pattern_generico.match(linha.strip())
    if match:
        exemplos.append((i+1, linha.strip()))
        if len(exemplos) >= 50:
            break

for linha_num, texto in exemplos:
    # Marcar os que não começam com SMARTPHONE
    marcador = "   " if texto.upper().startswith(tuple([f"{p[0].split('un')[1].strip()[:10]}" for p in patterns])) else ">>>"
    print(f"{marcador} Linha {linha_num}: {texto[:100]}")

# Contar quantos NÃO são SMARTPHONE
print(f"\n{'='*80}")
print("ANÁLISE COMPLETA:")
print("="*80)

pattern_smartphone = re.compile(r'^\d+,\d+\s+un\s+SMARTPHONE', re.IGNORECASE)
total_itens = 0
smartphones = 0
outros = []

for linha in linhas:
    match = pattern_generico.match(linha.strip())
    if match:
        total_itens += 1
        if pattern_smartphone.match(linha.strip()):
            smartphones += 1
        else:
            outros.append(linha.strip())

print(f"Total de itens com 'X,XX un ...': {total_itens:,}".replace(',', '.'))
print(f"SMARTPHONEs: {smartphones:,}".replace(',', '.'))
print(f"OUTROS: {len(outros):,}".replace(',', '.'))

if outros:
    print(f"\nPrimeiros 30 itens que NÃO são SMARTPHONE:")
    for i, item in enumerate(outros[:30], 1):
        print(f"  {i}. {item[:100]}")
