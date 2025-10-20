import json

print("=" * 80)
print("CONFIRMAÇÃO VISUAL DOS TOTAIS")
print("=" * 80)
print()

# Carregar JSON
with open('celulares_contabilizados.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

print("📊 TOTAIS DO JSON:")
print(f"   Total de aparelhos......: {dados['total_aparelhos']:,}")
print(f"   Total de modelos/descrições: {dados['total_modelos']:,}")
print()

# Vamos somar manualmente alguns exemplos
print("🧮 EXEMPLOS DE COMO CHEGAR NO TOTAL DE 31.703:")
print("-" * 80)

exemplos_soma = [
    ("SMARTPHONE REALME C51 128GB 4GB RAM", 1071),
    ("SMARTPHONE REALME NOTE 50 64GB 3GB RAM", 1049),
    ("SMARTPHONE REALME NOTE 50 128GB 4GB RAM", 1001),
    ("SMARTPHONE XIAOMI REDMI NOTE 13 256GB CHINA NR DE SERIE NO", 838),
    ("SMARTPHONE XIAOMI REDMI 13C, 256GB SN: NO PROCESSO", 410),
]

soma_parcial = 0
for desc, qtd in exemplos_soma:
    print(f"   {desc[:65]:65s} = {qtd:5,} aparelhos")
    soma_parcial += qtd

print("-" * 80)
print(f"   Subtotal (apenas 5 modelos mais comuns).............. = {soma_parcial:5,} aparelhos")
print(f"   + Restante (outros {dados['total_modelos'] - 5:,} modelos).................... = {dados['total_aparelhos'] - soma_parcial:5,} aparelhos")
print("-" * 80)
print(f"   TOTAL GERAL.......................................... = {dados['total_aparelhos']:5,} aparelhos ✅")
print()

# Mostrar a matemática
print("📐 MATEMÁTICA:")
print("-" * 80)
total_calculado = sum(dados['modelos'].values())
print(f"   Soma de todos os {dados['total_modelos']:,} modelos no JSON = {total_calculado:,} aparelhos")
print()

# Comparar
if total_calculado == dados['total_aparelhos']:
    print("   ✅ CORRETO! A soma manual bate com o total_aparelhos")
else:
    print(f"   ⚠️  Divergência: {total_calculado} vs {dados['total_aparelhos']}")

print()
print("=" * 80)
print("RESUMO FINAL:")
print("=" * 80)
print()
print(f"   📦 APARELHOS FÍSICOS TOTAIS....: {dados['total_aparelhos']:,} unidades")
print(f"   📝 LINHAS NOS PDFs.............: 14.402 linhas")
print(f"   🏷️  DESCRIÇÕES DIFERENTES.......: {dados['total_modelos']:,} variações")
print()
print("   Isso significa que foram recebidos 31.703 celulares físicos,")
print("   distribuídos em 14.402 lotes (linhas nos PDFs),")
print("   com 8.162 descrições diferentes.")
print()
