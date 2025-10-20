import json
import csv

print("=" * 70)
print("VERIFICAÇÃO CRUZADA DOS TOTAIS")
print("=" * 70)
print()

# 1. Verificar JSON
print("1. Verificando arquivo JSON...")
with open('celulares_contabilizados.json', 'r', encoding='utf-8') as f:
    dados_json = json.load(f)

total_json = dados_json['total_aparelhos']
total_modelos_json = dados_json['total_modelos']
print(f"   Total de aparelhos no JSON: {total_json:,}")
print(f"   Total de modelos no JSON: {total_modelos_json:,}")
print()

# 2. Verificar CSV
print("2. Verificando arquivo CSV...")
total_csv = 0
linhas_csv = 0
with open('celulares_detalhado.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        total_csv += int(row['Quantidade'])
        linhas_csv += 1

print(f"   Total de aparelhos no CSV: {total_csv:,}")
print(f"   Total de linhas no CSV: {linhas_csv:,}")
print()

# 3. Somar manualmente os modelos do JSON
print("3. Somando manualmente os valores do JSON...")
soma_manual = sum(dados_json['modelos'].values())
print(f"   Soma manual dos modelos: {soma_manual:,}")
print()

# 4. Verificar consistência
print("=" * 70)
print("RESULTADO DA VERIFICAÇÃO")
print("=" * 70)
print()

if total_json == total_csv == soma_manual:
    print(f"✅ VERIFICAÇÃO OK! Todos os valores conferem: {total_json:,} aparelhos")
    print()
    print(f"   📊 Total de aparelhos: {total_json:,}")
    print(f"   📝 Total de linhas processadas: {linhas_csv:,}")
    print(f"   🏷️  Total de descrições únicas: {total_modelos_json:,}")
    print()
    print("   Os números são 100% confiáveis! ✓")
else:
    print("⚠️  ATENÇÃO: Inconsistência detectada!")
    print(f"   JSON total_aparelhos: {total_json:,}")
    print(f"   CSV soma quantidades: {total_csv:,}")
    print(f"   Soma manual modelos: {soma_manual:,}")

print()
print("=" * 70)

# 5. Mostrar distribuição por PDF
print()
print("DISTRIBUIÇÃO POR PDF:")
print("-" * 70)

pdfs_contagem = {}
with open('celulares_detalhado.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        pdf = row['PDF']
        qtd = int(row['Quantidade'])
        pdfs_contagem[pdf] = pdfs_contagem.get(pdf, 0) + qtd

for pdf, total in sorted(pdfs_contagem.items()):
    print(f"   {pdf:50s} {total:6,} aparelhos")

print("-" * 70)
print(f"   TOTAL GERAL: {sum(pdfs_contagem.values()):6,} aparelhos")
print()
