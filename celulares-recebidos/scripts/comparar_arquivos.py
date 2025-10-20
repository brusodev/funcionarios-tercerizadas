import re

# Ler arquivo original
with open('teste_original.json', 'r', encoding='utf-8') as f:
    original = f.read()

# Ler arquivo convertido
with open('teste.json', 'r', encoding='utf-8') as f:
    convertido = f.read()

linhas_original = original.split('\n')
linhas_convertido = convertido.split('\n')

print("="*80)
print("COMPARAÇÃO DE LINHAS")
print("="*80)
print(f"\nArquivo ORIGINAL: {len(linhas_original):,} linhas".replace(',', '.'))
print(f"Arquivo CONVERTIDO: {len(linhas_convertido):,} linhas".replace(',', '.'))
print(f"DIFERENÇA: {len(linhas_original) - len(linhas_convertido):,} linhas perdidas".replace(',', '.'))

# Contar quantos SMARTPHONEs existem no original
pattern_smartphone = re.compile(r'^\d+,\d+\s+un\s+SMARTPHONE', re.IGNORECASE)

smartphones_original = 0
for linha in linhas_original:
    if pattern_smartphone.match(linha.strip()):
        smartphones_original += 1

smartphones_convertido = len(linhas_convertido)

print(f"\n{'='*80}")
print("ITENS SMARTPHONE")
print("="*80)
print(f"No ORIGINAL: {smartphones_original:,} itens começando com 'X,XX un SMARTPHONE'".replace(',', '.'))
print(f"No CONVERTIDO: {smartphones_convertido:,} linhas".replace(',', '.'))
print(f"DIFERENÇA: {smartphones_original - smartphones_convertido:,} itens perdidos".replace(',', '.'))

# Verificar se há itens sem valor no original
print(f"\n{'='*80}")
print("ANÁLISE DO ORIGINAL - Primeiras 50 linhas com SMARTPHONE")
print("="*80)

count = 0
for i, linha in enumerate(linhas_original):
    if pattern_smartphone.match(linha.strip()):
        # Mostrar a linha e as próximas 3
        print(f"\nLinha {i+1}: {linha.strip()}")
        for j in range(1, 4):
            if i+j < len(linhas_original):
                print(f"  +{j}: {linhas_original[i+j].strip()}")
        
        count += 1
        if count >= 10:
            break

print(f"\n{'='*80}")
print("Vou verificar se há itens que não foram capturados...")
print("="*80)
