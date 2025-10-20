import csv
import json

# Exemplos que você mencionou
exemplos = [
    "TELEFONE CELULAR XIAOMI REDMI 9 ACTIVE, 128GB, INDIA,",
    "TELEFONE CELULAR XIAOMI REDMI 9A, 64GB, SEM ORIGEM IMEI1:",
    "SMARTPHONE XIAOMI POCO X5 PRO, 256GB, CHINA SN:",
    "SMARTPHONE MOTOROLA MOTO G52, CHINA, 128GB, IMEI:",
    "SMARTPHONE MOTOROLA MOTO G 42, 128GB, CHINA, IMEI:"
]

print("=" * 100)
print("MOSTRANDO DE ONDE VÊM OS NÚMEROS - EXEMPLOS DO JSON")
print("=" * 100)
print()

# Verificar no JSON
with open('celulares_contabilizados.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

print("1. VALORES NO JSON:")
print("-" * 100)
total_exemplos = 0
for desc in exemplos:
    qtd = dados['modelos'].get(desc, 0)
    total_exemplos += qtd
    print(f"   {desc[:80]:80s} = {qtd} aparelho(s)")

print("-" * 100)
print(f"   TOTAL dos 5 exemplos: {total_exemplos} aparelhos")
print()

# Verificar no CSV
print("2. LINHAS CORRESPONDENTES NO CSV:")
print("-" * 100)
print(f"   {'PDF':<35s} | {'Qtd':>3s} | {'Descrição Completa'}")
print("-" * 100)

with open('celulares_detalhado.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    encontradas = 0
    for row in reader:
        if row['Descrição Completa'] in exemplos:
            pdf = row['PDF'].replace('ADM 0800100_', '').replace('_2025 de 30_09_2025.PDF', '')
            print(f"   {pdf:<35s} | {row['Quantidade']:>3s} | {row['Descrição Completa'][:60]}")
            encontradas += 1

print("-" * 100)
print(f"   Total de linhas encontradas: {encontradas}")
print()

# Mostrar um exemplo com quantidade maior
print("3. EXEMPLO COM QUANTIDADE MAIOR (para comparação):")
print("-" * 100)
print(f"   {'Descrição':<80s} | {'Qtd':>5s}")
print("-" * 100)

# Pega as top 5 do JSON
for desc, qtd in list(dados['modelos_ordenados'].items())[:5]:
    print(f"   {desc[:80]:80s} | {qtd:5d}")

print()
print("=" * 100)
print("CONCLUSÃO:")
print("=" * 100)
print("✅ Cada número no JSON representa a SOMA das quantidades de todas as vezes")
print("   que aquela descrição exata apareceu nos PDFs.")
print()
print("   Por exemplo:")
print("   - Se 'SMARTPHONE REALME C51 128GB 4GB RAM' aparece 50 vezes com qtd 10,")
print("     e 20 vezes com qtd 15, o total será: (50×10) + (20×15) = 800 aparelhos")
print()
