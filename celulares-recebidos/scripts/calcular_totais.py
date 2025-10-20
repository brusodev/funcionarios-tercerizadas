import json

# Ler o arquivo JSON estruturado
with open('celulares_estruturado.json', 'r', encoding='utf-8') as f:
    celulares = json.load(f)

# Calcular totais
total_aparelhos = 0
total_valor = 0

for item in celulares:
    unidade = item['unidade']
    valor_str = item['valor'].replace('R$ ', '').replace('.', '').replace(',', '.')
    valor = float(valor_str)
    
    total_aparelhos += unidade
    total_valor += valor

# Exibir resultados
print("="*80)
print("TOTAIS DO JSON ESTRUTURADO")
print("="*80)

print(f"\nTotal de aparelhos: {int(total_aparelhos):,}".replace(',', '.'))
print(f"Valor total: R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

print(f"\n{'='*80}")
print("DETALHAMENTO:")
print("="*80)
print(f"Total de linhas no JSON: {len(celulares):,}".replace(',', '.'))
print(f"Total de unidades (soma): {int(total_aparelhos):,}".replace(',', '.'))
print(f"Valor total (soma): R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Estatísticas adicionais
print(f"\n{'='*80}")
print("ESTATÍSTICAS:")
print("="*80)
valor_medio_por_aparelho = total_valor / total_aparelhos if total_aparelhos > 0 else 0
print(f"Valor médio por aparelho: R$ {valor_medio_por_aparelho:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Valor mínimo e máximo
valores = []
for item in celulares:
    valor_str = item['valor'].replace('R$ ', '').replace('.', '').replace(',', '.')
    valores.append(float(valor_str))

print(f"Valor unitário mínimo: R$ {min(valores):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
print(f"Valor unitário máximo: R$ {max(valores):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Top 5 modelos por quantidade
print(f"\n{'='*80}")
print("TOP 5 MODELOS POR QUANTIDADE:")
print("="*80)

# Agrupar por modelo
modelos = {}
for item in celulares:
    modelo_base = item['modelo'].split('//')[0].strip()  # Pegar só a parte antes de //
    if modelo_base not in modelos:
        modelos[modelo_base] = {
            'quantidade': 0,
            'valor_total': 0
        }
    
    unidade = item['unidade']
    valor_str = item['valor'].replace('R$ ', '').replace('.', '').replace(',', '.')
    valor = float(valor_str)
    
    modelos[modelo_base]['quantidade'] += unidade
    modelos[modelo_base]['valor_total'] += valor

# Ordenar por quantidade
top_modelos = sorted(modelos.items(), key=lambda x: x[1]['quantidade'], reverse=True)[:5]

for i, (modelo, dados) in enumerate(top_modelos, 1):
    qtd = int(dados['quantidade'])
    valor = dados['valor_total']
    print(f"\n{i}. {modelo}")
    print(f"   Quantidade: {qtd:,}".replace(',', '.'))
    print(f"   Valor total: R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Salvar resumo em JSON
resumo = {
    "total_aparelhos": int(total_aparelhos),
    "total_valor": f"R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'),
    "total_valor_numerico": round(total_valor, 2),
    "total_linhas": len(celulares),
    "valor_medio_por_aparelho": round(valor_medio_por_aparelho, 2),
    "valor_unitario_minimo": round(min(valores), 2),
    "valor_unitario_maximo": round(max(valores), 2),
    "top_5_modelos": [
        {
            "modelo": modelo,
            "quantidade": int(dados['quantidade']),
            "valor_total": round(dados['valor_total'], 2)
        }
        for modelo, dados in top_modelos
    ]
}

with open('resumo_totais.json', 'w', encoding='utf-8') as f:
    json.dump(resumo, f, ensure_ascii=False, indent=2)

print(f"\n{'='*80}")
print("✓ Arquivo 'resumo_totais.json' criado com estatísticas completas!")
print("="*80)
