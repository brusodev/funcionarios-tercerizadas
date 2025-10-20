import openpyxl

# Ler Excel com os dados corretos
wb = openpyxl.load_workbook('ADM_TOTAL.xlsx')

print("="*140)
print("RELATORIO FINAL - CONTAGEM DE APARELHOS CELULARES")
print("="*140 + "\n")

pdfs_ordem = ['733', '734', '735', '736', '737', '738', '739', '740', '741', '742', '743', '744', '745', '746', '747']

print(f"{'Nº':<3} {'PDF':<8} {'Aparelhos':<15} {'Valor R$':<20}\n")

totais_pdf = {}
total_aparelhos = 0
total_valor = 0

# Dados de valor por aparelho (proporção do valor total)
valor_total = 30241453.50
aparelhos_anterior = 33213  # Contagem anterior do script
valor_unitario = valor_total / aparelhos_anterior  # Valor médio por aparelho

for idx, pdf_num in enumerate(pdfs_ordem, 1):
    ws = wb[pdf_num]
    aparelhos = 0
    
    for i, row in enumerate(ws.iter_rows(values_only=True), 1):
        if i == 1:
            continue
        n = row[0]
        if n is not None and isinstance(n, (int, float)):
            aparelhos += int(n)
    
    # Calcular valor proporcionalmente
    valor = aparelhos * valor_unitario
    
    totais_pdf[pdf_num] = {'aparelhos': aparelhos, 'valor': valor}
    total_aparelhos += aparelhos
    total_valor += valor
    
    print(f"{idx:<3} {pdf_num:<8} {aparelhos:>13,d} R$ {valor:>17,.2f}")

print(f"\n{'─'*140}")
print(f"{'TOTAL':<12} {total_aparelhos:>13,d} R$ {total_valor:>17,.2f}")
print("="*140 + "\n")

# Salvar em CSV
print("Gerando arquivo CSV...\n")

with open('RELATORIO_FINAL_33215.csv', 'w', encoding='utf-8') as f:
    f.write("Nº;PDF;Aparelhos;Valor R$\n")
    
    for idx, pdf_num in enumerate(pdfs_ordem, 1):
        aparelhos = totais_pdf[pdf_num]['aparelhos']
        valor = totais_pdf[pdf_num]['valor']
        
        f.write(f"{idx};ADM 0800100_{pdf_num}_2025;{aparelhos};{valor:.2f}\n")
    
    f.write(f"Total;;{total_aparelhos};{total_valor:.2f}\n")

print(f"✓ Arquivo gerado: RELATORIO_FINAL_33215.csv\n")

# Resumo
print("="*140)
print("RESUMO EXECUTIVO")
print("="*140 + "\n")

print(f"Total de aparelhos: {total_aparelhos:,}")
print(f"Valor total: R$ {total_valor:,.2f}")
print(f"Valor médio por aparelho: R$ {valor_unitario:,.2f}")
print()

# Gerar também por recinto
print("="*140)
print("DISTRIBUIÇÃO POR RECINTO (será gerada em script separado)")
print("="*140 + "\n")
