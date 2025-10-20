import json

# Carregar resultados
with open('resumo_por_pdf.json', 'r', encoding='utf-8') as f:
    resumo = json.load(f)

print("="*80)
print("VALIDAÇÃO DOS VALORES CONHECIDOS")
print("="*80)

# Valores que você informou
validacoes = {
    'ADM 0800100_0735_2025 de 30_09_2025.PDF': {
        'aparelhos': 3804,
        'valor': 2845357.66
    },
    'ADM 0800100_0746_2025 de 30_09_2025.PDF': {
        'aparelhos': 2544,
        'valor': 3050180.53
    },
    'ADM 0800100_0743_2025 de 30_09_2025.PDF': {
        'aparelhos': 912,
        'valor': 1555781.16
    }
}

for item in resumo:
    if item['pdf'] in validacoes:
        esperado = validacoes[item['pdf']]
        encontrado_aparelhos = item['aparelhos']
        encontrado_valor = item['valor_total']
        
        diff_aparelhos = encontrado_aparelhos - esperado['aparelhos']
        diff_valor = encontrado_valor - esperado['valor']
        perc_valor = (diff_valor / esperado['valor']) * 100 if esperado['valor'] > 0 else 0
        
        print(f"\n{item['pdf']}")
        print("-" * 80)
        print(f"APARELHOS:")
        print(f"  Esperado: {esperado['aparelhos']:,}".replace(',', '.'))
        print(f"  Encontrado: {encontrado_aparelhos:,}".replace(',', '.'))
        print(f"  Diferença: {diff_aparelhos:+d}")
        
        print(f"\nVALOR:")
        print(f"  Esperado: R$ {esperado['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"  Encontrado: R$ {encontrado_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"  Diferença: R$ {diff_valor:+,.2f} ({perc_valor:+.2f}%)".replace(',', 'X').replace('.', ',').replace('X', '.'))
        
        if abs(diff_aparelhos) <= 5 and abs(perc_valor) <= 1:
            print(f"  ✅ VALIDADO (diferença aceitável)")
        else:
            print(f"  ⚠️ Verificar diferença")

print("\n" + "="*80)
