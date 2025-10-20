import json
import re

# Ler o arquivo JSON
with open('teste.json', 'r', encoding='utf-8') as f:
    conteudo = f.read()

print("="*80)
print("INVESTIGAÇÃO - Por que o JSON está dando valor menor?")
print("="*80)

# Contar linhas totais
linhas = conteudo.split('\n')
print(f"\nTotal de linhas no JSON: {len(linhas):,}".replace(',', '.'))

# Buscar TODOS os valores R$ no arquivo (incluindo Subtotais)
pattern_valor = re.compile(r'R\$\s*([\d.]+,\d{2})')
todos_valores = pattern_valor.findall(conteudo)

print(f"Total de valores R$ encontrados: {len(todos_valores):,}".replace(',', '.'))

# Converter e somar TODOS os valores (incluindo subtotais)
valores_float = []
for valor_str in todos_valores:
    valor_float = float(valor_str.replace('.', '').replace(',', '.'))
    valores_float.append(valor_float)

total_bruto = sum(valores_float)
print(f"\nSoma de TODOS os valores R$ no JSON: R$ {total_bruto:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Buscar valores "Subtotal:"
pattern_subtotal = re.compile(r'Subtotal:\s*R\$\s*([\d.]+,\d{2})')
subtotais = pattern_subtotal.findall(conteudo)
print(f"\nSubtotais encontrados: {len(subtotais)}")

if subtotais:
    soma_subtotais = sum(float(s.replace('.', '').replace(',', '.')) for s in subtotais)
    print(f"Soma dos Subtotais: R$ {soma_subtotais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Buscar "Total do ADM:"
pattern_total_adm = re.compile(r'Total do ADM:\s*R\$\s*([\d.]+,\d{2})')
total_adm = pattern_total_adm.findall(conteudo)
print(f"\nTotal do ADM encontrados: {len(total_adm)}")

if total_adm:
    for i, total in enumerate(total_adm, 1):
        total_float = float(total.replace('.', '').replace(',', '.'))
        print(f"  Total do ADM #{i}: R$ {total_float:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Agora vamos contar APENAS itens de smartphone (sem subtotais)
pattern_item = re.compile(
    r'^(\d+,\d+)\s+un\s+(SMARTPHONE.*?)(?://|$)',
    re.IGNORECASE
)

itens_smartphone = []
valores_por_item = []

i = 0
while i < len(linhas):
    linha = linhas[i].strip()
    
    match = pattern_item.match(linha)
    if match:
        qtd_str = match.group(1).replace(',', '.')
        quantidade = float(qtd_str)
        
        # Buscar valor nas próximas linhas
        valor = None
        for j in range(i, min(i + 5, len(linhas))):
            linha_busca = linhas[j]
            
            # Ignorar Subtotal e Total do ADM
            if 'Subtotal:' in linha_busca or 'Total do ADM:' in linha_busca:
                continue
            
            match_valor = pattern_valor.search(linha_busca)
            if match_valor:
                valor_str = match_valor.group(1).replace('.', '').replace(',', '.')
                valor = float(valor_str)
                break
        
        if valor:
            itens_smartphone.append({
                'quantidade': quantidade,
                'valor': valor
            })
            valores_por_item.append(valor)
    
    i += 1

total_itens = sum(item['quantidade'] for item in itens_smartphone)
total_valores_itens = sum(valores_por_item)

print("\n" + "="*80)
print("COMPARAÇÃO:")
print("="*80)

print(f"\nMÉTODO 1 - Soma de TODOS os R$ do arquivo:")
print(f"  Total: R$ {total_bruto:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

print(f"\nMÉTODO 2 - Soma apenas valores de itens (ignorando Subtotal/Total):")
print(f"  Aparelhos: {int(total_itens):,}".replace(',', '.'))
print(f"  Total: R$ {total_valores_itens:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

print(f"\nVALOR ESPERADO (do script V7):")
print(f"  Total: R$ 4.644.268,78")

print(f"\nDIFERENÇA:")
diff1 = total_bruto - 4644268.78
diff2 = total_valores_itens - 4644268.78
print(f"  Método 1 vs Esperado: R$ {diff1:+,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
print(f"  Método 2 vs Esperado: R$ {diff2:+,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Verificar se o JSON está completo (deve ter o total no final)
if total_adm:
    print(f"\n{'='*80}")
    print("✓ JSON contém 'Total do ADM' - arquivo parece completo")
    print(f"{'='*80}")
else:
    print(f"\n{'='*80}")
    print("⚠️ JSON NÃO contém 'Total do ADM' - arquivo pode estar incompleto!")
    print(f"{'='*80}")
