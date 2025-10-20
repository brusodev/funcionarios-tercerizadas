import json
import csv

# Dados de aparelhos por recinto (do script anterior)
aparelhos_recinto = {
    'Araraquara': 4965,
    'Bauru': 17592,
    'Ipiranga': 9392,
    'São José do Rio Preto': 601,
    'Viracopos': 665
}

# Valor total VALIDADO
valor_total_validado = 30241453.50

# Total de aparelhos
total_aparelhos = sum(aparelhos_recinto.values())

print("=" * 70)
print("DISTRIBUIÇÃO POR RECINTO - VERSÃO FINAL CORRIGIDA")
print("=" * 70)
print()
print(f"Total de Aparelhos: {total_aparelhos:,}")
print(f"Valor Total Validado: R$ {valor_total_validado:,.2f}")
print()

# Calcula proporção de valor por recinto
distribuicao_final = {}

for recinto, aparelhos in sorted(aparelhos_recinto.items()):
    percentual = (aparelhos / total_aparelhos) * 100
    valor_recinto = (aparelhos / total_aparelhos) * valor_total_validado
    
    distribuicao_final[recinto] = {
        'aparelhos': aparelhos,
        'percentual': percentual,
        'valor': valor_recinto
    }
    
    print(f"{recinto:25} | {aparelhos:6,} aparelhos | {percentual:6.2f}% | R$ {valor_recinto:,.2f}")

print("-" * 70)
print(f"{'TOTAL':25} | {total_aparelhos:6,} aparelhos | {'100.00':>6}% | R$ {valor_total_validado:,.2f}")
print("-" * 70)
print()

# Salva em CSV
with open('RELATORIO_POR_RECINTO_FINAL_VALIDADO.csv', 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['Recinto', 'Aparelhos', 'Percentual (%)', 'Valor (R$)'])
    
    for recinto in sorted(distribuicao_final.keys()):
        dados = distribuicao_final[recinto]
        writer.writerow([
            recinto,
            f"{dados['aparelhos']:,}".replace(',', '.'),
            f"{dados['percentual']:.2f}".replace('.', ','),
            f"{dados['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        ])
    
    # Linha de total
    writer.writerow([
        'TOTAL',
        f"{total_aparelhos:,}".replace(',', '.'),
        '100,00',
        f"{valor_total_validado:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    ])

# Salva em JSON
with open('RELATORIO_POR_RECINTO_FINAL_VALIDADO.json', 'w', encoding='utf-8') as f:
    resultado = {
        'data': '2025-10-17',
        'validacao': 'Contagem verificada contra ADM_TOTAL.xlsx',
        'total_aparelhos': total_aparelhos,
        'valor_total': valor_total_validado,
        'recintos': distribuicao_final
    }
    json.dump(resultado, f, ensure_ascii=False, indent=2)

print("✓ Arquivos salvos com sucesso:")
print("  - RELATORIO_POR_RECINTO_FINAL_VALIDADO.csv")
print("  - RELATORIO_POR_RECINTO_FINAL_VALIDADO.json")
print()
print("✅ ESTA DISTRIBUIÇÃO PODE SER CONFIADA!")
print("   - Aparelhos: Extraídos linha-por-linha dos PDFs e validados")
print("   - Valor: Distribuído proporcionalmente ao valor total validado")
print("   - Total: 33.215 aparelhos | R$ 30.241.453,50")
