import re
import json

# Ler arquivo original para comparar
with open('teste_original.json', 'r', encoding='utf-8') as f:
    original = f.read()

# Buscar "Total do ADM" no original
pattern_total_adm = re.compile(r'Total do ADM:\s*R\$\s*([\d.]+,\d{2})')
match = pattern_total_adm.search(original)

if match:
    total_adm_str = match.group(1).replace('.', '').replace(',', '.')
    total_adm = float(total_adm_str)
    print(f"Total do ADM no PDF: R$ {total_adm:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
else:
    total_adm = None
    print("Total do ADM NÃO encontrado no original")

# Calcular total do JSON estruturado
with open('celulares_estruturado.json', 'r', encoding='utf-8') as f:
    celulares = json.load(f)

total_json = 0
for item in celulares:
    valor_str = item['valor'].replace('R$ ', '').replace('.', '').replace(',', '.')
    valor = float(valor_str)
    total_json += valor

print(f"Total do JSON estruturado: R$ {total_json:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

if total_adm:
    diferenca = total_adm - total_json
    percentual = (diferenca / total_adm) * 100
    
    print(f"\n{'='*80}")
    print("DIFERENÇA:")
    print("="*80)
    print(f"Esperado (Total do ADM): R$ {total_adm:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"Calculado (JSON): R$ {total_json:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"Diferença: R$ {diferenca:+,.2f} ({percentual:+.2f}%)".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Verificar se há valores que estão no original mas não no JSON
print(f"\n{'='*80}")
print("VERIFICANDO VALORES PERDIDOS...")
print("="*80)

# Buscar TODOS os valores R$ no original
pattern_valor = re.compile(r'R\$\s*([\d.]+,\d{2})')
todos_valores_original = pattern_valor.findall(original)

print(f"\nTotal de valores R$ no original: {len(todos_valores_original):,}".replace(',', '.'))

# Buscar valores de Subtotais
pattern_subtotal = re.compile(r'Subtotal:\s*R\$\s*([\d.]+,\d{2})')
subtotais = pattern_subtotal.findall(original)
print(f"Subtotais encontrados: {len(subtotais)}")

if subtotais:
    soma_subtotais = sum(float(s.replace('.', '').replace(',', '.')) for s in subtotais)
    print(f"Soma dos Subtotais: R$ {soma_subtotais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    if total_adm:
        print(f"\nDiferença (Total do ADM - Soma Subtotais): R$ {(total_adm - soma_subtotais):+,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Verificar se o problema está na formatação do teste.json
print(f"\n{'='*80}")
print("VERIFICANDO ARQUIVO teste.json...")
print("="*80)

with open('teste.json', 'r', encoding='utf-8') as f:
    linhas_teste = f.readlines()

pattern_linha = re.compile(r'^(\d+,\d+)\s+un\s+(.+?)///R\$\s*([\d.]+,\d{2})')

valores_teste_json = []
for linha in linhas_teste:
    match = pattern_linha.match(linha.strip())
    if match:
        valor_str = match.group(3).replace('.', '').replace(',', '.')
        valores_teste_json.append(float(valor_str))

total_teste_json = sum(valores_teste_json)
print(f"Total calculado de teste.json: R$ {total_teste_json:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
print(f"Linhas em teste.json: {len(valores_teste_json):,}".replace(',', '.'))

print(f"\n{'='*80}")
print("CONCLUSÃO:")
print("="*80)
if total_adm and abs(total_teste_json - total_adm) > 1:
    print(f"⚠️ PROBLEMA: Faltam R$ {(total_adm - total_teste_json):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"   Possível causa: Alguns itens não foram capturados na conversão")
else:
    print("✓ Valores estão corretos!")
