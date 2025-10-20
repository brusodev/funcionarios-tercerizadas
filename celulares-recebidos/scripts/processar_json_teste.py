import json
import re

# Ler o arquivo JSON (que na verdade é texto extraído do PDF)
with open('teste.json', 'r', encoding='utf-8') as f:
    conteudo = f.read()

# Separar em linhas
linhas = conteudo.split('\n')

# Padrão para identificar linhas de itens (quantidade + unidade + descrição)
pattern_item = re.compile(
    r'^(\d+,\d+)\s+un\s+(SMARTPHONE.*?)(?://|$)',
    re.IGNORECASE
)

# Padrão para valores em reais
pattern_valor = re.compile(r'R\$\s*([\d.]+,\d{2})')

resultados = []
total_aparelhos = 0
total_valor = 0

i = 0
while i < len(linhas):
    linha = linhas[i].strip()
    
    # Verificar se é uma linha de item
    match = pattern_item.match(linha)
    if match:
        qtd_str = match.group(1).replace(',', '.')
        quantidade = float(qtd_str)
        descricao = match.group(2).strip()
        
        # Buscar valor nas próximas linhas (normalmente está 1-2 linhas depois)
        valor = None
        for j in range(i, min(i + 5, len(linhas))):
            linha_busca = linhas[j]
            
            # Ignorar linhas com "Subtotal:" ou "Total do ADM:"
            if 'Subtotal:' in linha_busca or 'Total do ADM:' in linha_busca:
                continue
            
            match_valor = pattern_valor.search(linha_busca)
            if match_valor:
                valor_str = match_valor.group(1).replace('.', '').replace(',', '.')
                valor = float(valor_str)
                break
        
        if valor:
            # Limpar descrição (remover detalhes técnicos extras)
            desc_limpa = descricao.split('//')[0].strip()
            
            resultados.append({
                'quantidade': quantidade,
                'descricao': desc_limpa,
                'valor': valor
            })
            
            total_aparelhos += quantidade
            total_valor += valor
    
    i += 1

# Buscar "Total do ADM" no JSON (valor oficial do PDF)
pattern_total_adm = re.compile(r'Total do ADM:\s*R\$\s*([\d.]+,\d{2})')
match_total_adm = pattern_total_adm.search(conteudo)
total_oficial = None
if match_total_adm:
    total_str = match_total_adm.group(1).replace('.', '').replace(',', '.')
    total_oficial = float(total_str)

# Exibir resultados
print("="*80)
print("ANÁLISE DO JSON EXTRAÍDO DO PDF 0745")
print("="*80)

print(f"\nTOTAL DE APARELHOS: {int(total_aparelhos):,}".replace(',', '.'))

if total_oficial:
    print(f"VALOR TOTAL (oficial do PDF): R$ {total_oficial:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"  ✓ Usando 'Total do ADM' encontrado no final do documento")
else:
    print(f"VALOR TOTAL (soma dos itens): R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"  ⚠️ 'Total do ADM' não encontrado - usando soma manual")

print(f"\n{'='*80}")
print(f"DETALHAMENTO POR ITEM ({len(resultados)} itens encontrados):")
print(f"{'='*80}")

# Agrupar por modelo
agrupado = {}
for item in resultados:
    desc = item['descricao']
    if desc not in agrupado:
        agrupado[desc] = {
            'quantidade': 0,
            'valor_total': 0,
            'itens': []
        }
    agrupado[desc]['quantidade'] += item['quantidade']
    agrupado[desc]['valor_total'] += item['valor']
    agrupado[desc]['itens'].append(item)

# Ordenar por quantidade (maior para menor)
for desc in sorted(agrupado.keys(), key=lambda x: agrupado[x]['quantidade'], reverse=True):
    dados = agrupado[desc]
    qtd = int(dados['quantidade'])
    valor = dados['valor_total']
    valor_medio = valor / dados['quantidade'] if dados['quantidade'] > 0 else 0
    
    print(f"\n{desc}")
    print(f"  Quantidade: {qtd:,}".replace(',', '.'))
    print(f"  Valor Total: R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"  Valor Médio: R$ {valor_medio:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Salvar resultado em JSON estruturado
resultado_final = {
    'total_aparelhos': int(total_aparelhos),
    'total_valor_oficial': round(total_oficial, 2) if total_oficial else round(total_valor, 2),
    'total_valor_soma_itens': round(total_valor, 2),
    'fonte_valor': 'Total do ADM (oficial)' if total_oficial else 'Soma manual dos itens',
    'total_modelos': len(agrupado),
    'resumo_por_modelo': [
        {
            'modelo': desc,
            'quantidade': int(dados['quantidade']),
            'valor_total': round(dados['valor_total'], 2),
            'valor_medio': round(dados['valor_total'] / dados['quantidade'], 2)
        }
        for desc, dados in sorted(agrupado.items(), key=lambda x: x[1]['quantidade'], reverse=True)
    ],
    'itens_detalhados': resultados
}

with open('resultado_teste_0745.json', 'w', encoding='utf-8') as f:
    json.dump(resultado_final, f, ensure_ascii=False, indent=2)

print(f"\n{'='*80}")
print(f"✓ Arquivo 'resultado_teste_0745.json' criado com dados estruturados")
print(f"{'='*80}")
