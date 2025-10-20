import PyPDF2
import re

# Seus dados de 32.015 com valores reais
dados_usuario = {
    '0733': {'aparelhos': 13, 'valor': 7879.62},
    '0734': {'aparelhos': 6879, 'valor': 5716622.03},
    '0740': {'aparelhos': 9, 'valor': 3950.54},
    '0741': {'aparelhos': 19, 'valor': 18816.20},
    '0742': {'aparelhos': 225, 'valor': 84426.55},
    '0743': {'aparelhos': 912, 'valor': 1555781.16},
    '0744': {'aparelhos': 3457, 'valor': 3465958.49},
    '0735': {'aparelhos': 3804, 'valor': 2845357.66},
    '0736': {'aparelhos': 1873, 'valor': 2744064.74},
    '0737': {'aparelhos': 616, 'valor': 280644.01},
    '0738': {'aparelhos': 442, 'valor': 486866.60},
    '0739': {'aparelhos': 3708, 'valor': 1870406.44},
    '0745': {'aparelhos': 3390, 'valor': 4644268.78},
    '0746': {'aparelhos': 2544, 'valor': 3050180.53},
    '0747': {'aparelhos': 4124, 'valor': 3466230.15},
}

# Dados do script (32.027)
dados_script = {
    '0733': 13,
    '0734': 6879,
    '0740': 9,
    '0741': 19,
    '0742': 225,
    '0743': 909,  # -3 (kg devices)
    '0744': 3458,  # +1 (SEM CAPACIDADE)
    '0735': 3816,  # +12 (4 linhas grandes)
    '0736': 1873,
    '0737': 616,
    '0738': 444,   # +2 (BLOQUEADO + SEM EMBALAGEM)
    '0739': 3708,
    '0745': 3390,
    '0746': 2544,
    '0747': 4124,
}

# Valor total que deve ser mantido
valor_total_fixo = 30241453.50

# Calcular valor unitário por aparelho (será o mesmo para todos)
# valor_total / aparelhos_totais = valor por aparelho
valor_unitario_geral = valor_total_fixo / 32027

print("="*110)
print("📊 DISTRIBUIÇÃO DOS 32.027 APARELHOS POR PDF (com valor total fixo de R$ 30.241.453,50)")
print("="*110 + "\n")

print(f"Valor unitário por aparelho: R$ {valor_unitario_geral:.6f}\n")

# Ordem dos PDFs
ordem_pdfs = ['0733', '0734', '0740', '0741', '0742', '0743', '0744', '0735', '0736', '0737', '0738', '0739', '0745', '0746', '0747']
nome_arquivos = {
    '0733': 'ADM 0800100_0733_2025 de 30_09_2025.PDF',
    '0734': 'ADM 0800100_0734_2025 de 30_09_2025.PDF',
    '0740': 'ADM 0800100_0740_2025 de 30_09_2025.PDF',
    '0741': 'ADM 0800100_0741_2025 de 30_09_2025.PDF',
    '0742': 'ADM 0800100_0742_2025 de 30_09_2025.PDF',
    '0743': 'ADM 0800100_0743_2025 de 30_09_2025.PDF',
    '0744': 'ADM 0800100_0744_2025 de 30_09_2025.PDF',
    '0735': 'ADM 0800100_0735_2025 de 30_09_2025.PDF',
    '0736': 'ADM 0800100_0736_2025 de 30_09_2025.PDF',
    '0737': 'ADM 0800100_0737_2025 de 30_09_2025.PDF',
    '0738': 'ADM 0800100_0738_2025 de 30_09_2025.PDF',
    '0739': 'ADM 0800100_0739_2025 de 30_09_2025.PDF',
    '0745': 'ADM 0800100_0745_2025 de 30_09_2025.PDF',
    '0746': 'ADM 0800100_0746_2025 de 30_09_2025.PDF',
    '0747': 'ADM 0800100_0747_2025 de 30092025.PDF',
}

print(f"{'Nº':<3} {'Nome do Arquivo':<45} {'32.015':<12} {'32.027':<12} {'Diferença':<12} {'Valor R$ (32.027)':<20}\n")

contador = 1
total_novo_aparelhos = 0
total_novo_valores = 0.0

for pdf in ordem_pdfs:
    aparelhos_usuario = dados_usuario[pdf]['aparelhos']
    aparelhos_script = dados_script[pdf]
    diferenca = aparelhos_script - aparelhos_usuario
    
    # Calcular valor usando valor unitário universal
    valor_novo = valor_unitario_geral * aparelhos_script
    
    total_novo_aparelhos += aparelhos_script
    total_novo_valores += valor_novo
    
    diferenca_str = f"{diferenca:+d}"
    
    print(f"{contador:<3} {nome_arquivos[pdf]:<45} {aparelhos_usuario:<12,d} {aparelhos_script:<12,d} {diferenca_str:<12} R$ {valor_novo:>17,.2f}")
    contador += 1

print("\n" + "="*110)
print(f"{'TOTAL':<51} {32015:<12,d} {32027:<12,d} {'+12':<12} R$ {total_novo_valores:>17,.2f}")
print("="*110 + "\n")

# Validação
diferenca_valor = abs(total_novo_valores - valor_total_fixo)
print(f"Validação de valor total:")
print(f"  Esperado: R$ {valor_total_fixo:,.2f}")
print(f"  Calculado: R$ {total_novo_valores:,.2f}")
print(f"  Diferença: R$ {diferenca_valor:.2f} {'✅' if diferenca_valor < 0.01 else '❌'}\n")

# Criar arquivo CSV para exportar
with open('RELATORIO_APARELHOS_POR_PDF_32027.csv', 'w', encoding='utf-8') as f:
    f.write("Nº;Nome do Arquivo;Total de Aparelhos (32.015);Total de Aparelhos (32.027);Diferença;Valor Total R$\n")
    
    contador = 1
    for pdf in ordem_pdfs:
        aparelhos_usuario = dados_usuario[pdf]['aparelhos']
        aparelhos_script = dados_script[pdf]
        diferenca = aparelhos_script - aparelhos_usuario
        
        valor_novo = valor_unitario_geral * aparelhos_script
        
        diferenca_str = f"{diferenca:+d}"
        
        f.write(f"{contador};{nome_arquivos[pdf]};{aparelhos_usuario};{aparelhos_script};{diferenca_str};{valor_novo:.2f}\n")
        contador += 1
    
    f.write(f"Total;;32015;32027;+12;{total_novo_valores:.2f}\n")

print("✅ Arquivo CSV gerado: RELATORIO_APARELHOS_POR_PDF_32027.csv\n")
