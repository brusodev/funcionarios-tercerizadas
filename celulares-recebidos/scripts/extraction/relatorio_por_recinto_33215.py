import PyPDF2
import re
from collections import defaultdict

# Padrões dos recintos
recintos_padrao = {
    'Bauru': r'305\s*-\s*810300',
    'Araraquara': r'16\s*-\s*810900',
    'São José do Rio Preto': r'2\s*-\s*DEPÓSITO SAPOL',
    'Viracopos': r'1\s*-\s*AEROPORTOS BRASIL VIRACOPOS',
    'Ipiranga': r'309\s*-\s*817900'
}

pdfs_ordem = ['733', '734', '735', '736', '737', '738', '739', '740', '741', '742', '743', '744', '745', '746', '747']
valor_total_validado = 30241453.50

# Totais por recinto
totais_recinto = defaultdict(lambda: {'aparelhos': 0, 'valor': 0})

# Processar cada PDF
for pdf_num in pdfs_ordem:
    arquivo_pdf = f'ADM 0800100_0{pdf_num}_2025 de 30_09_2025.PDF'
    
    try:
        with open(arquivo_pdf, 'rb') as f:
            leitor = PyPDF2.PdfReader(f)
            texto_completo = ''
            
            for pagina in leitor.pages:
                texto_completo += pagina.extract_text()
        
        # Encontrar recintos e contar aparelhos
        linhas = texto_completo.split('\n')
        recinto_atual = None
        
        for linha in linhas:
            # Verificar se é linha de recinto
            for nome_recinto, padrao in recintos_padrao.items():
                if re.search(padrao, linha, re.IGNORECASE):
                    recinto_atual = nome_recinto
                    break
            
            # Se tem recinto ativo e encontra quantidade
            if recinto_atual:
                match = re.match(r'^\s*(\d+[\.,]?\d*,\d+)\s+(?:un|kg)', linha)
                if match:
                    qtd_str = match.group(1).replace('.', '').replace(',', '.')
                    qtd = float(qtd_str)
                    
                    # Converter kg para aparelhos
                    if 'kg' in linha.lower():
                        # 0.49 kg = 1 aparelho; 1 kg = 2 aparelhos
                        aparelhos = round(qtd / 0.49)
                    else:
                        aparelhos = int(qtd)
                    
                    totais_recinto[recinto_atual]['aparelhos'] += aparelhos
    
    except Exception as e:
        print(f"Erro ao processar {arquivo_pdf}: {e}")

# Calcular proporção e valores
total_aparelhos = sum(v['aparelhos'] for v in totais_recinto.values())
valor_por_aparelho = valor_total_validado / total_aparelhos

for recinto in totais_recinto:
    totais_recinto[recinto]['valor'] = totais_recinto[recinto]['aparelhos'] * valor_por_aparelho

# Exibir resultado
print("="*120)
print("DISTRIBUIÇÃO POR RECINTO - 33.215 APARELHOS")
print("="*120 + "\n")

print(f"{'Recinto':<40} {'Aparelhos':>15} {'%':>8} {'Valor R$':>20}\n")

# Ordenar por quantidade decrescente
recintos_ordenados = sorted(totais_recinto.items(), key=lambda x: x[1]['aparelhos'], reverse=True)

for recinto, dados in recintos_ordenados:
    aparelhos = dados['aparelhos']
    valor = dados['valor']
    percentual = (aparelhos / total_aparelhos) * 100
    
    print(f"{recinto:<40} {aparelhos:>15,d} {percentual:>7.2f}% R$ {valor:>18,.2f}")

print(f"\n{'─'*120}")
print(f"{'TOTAL':<40} {total_aparelhos:>15,d} {100:>7.2f}% R$ {valor_total_validado:>18,.2f}")
print("="*120 + "\n")

# Salvar em CSV
print("Gerando arquivo CSV...\n")

with open('RELATORIO_POR_RECINTO_33215.csv', 'w', encoding='utf-8') as f:
    f.write("Recinto;Aparelhos;Percentual;Valor R$\n")
    
    for recinto, dados in recintos_ordenados:
        aparelhos = dados['aparelhos']
        valor = dados['valor']
        percentual = (aparelhos / total_aparelhos) * 100
        
        f.write(f"{recinto};{aparelhos};{percentual:.2f}%;{valor:.2f}\n")
    
    f.write(f"Total;{total_aparelhos};100.00%;{valor_total_validado:.2f}\n")

print(f"✓ Arquivo gerado: RELATORIO_POR_RECINTO_33215.csv\n")

# Também por PDF e Recinto
print("="*120)
print("RESUMO: DISTRIBUIÇÃO POR RECINTO")
print("="*120 + "\n")

for recinto, dados in recintos_ordenados:
    percentual = (dados['aparelhos'] / total_aparelhos) * 100
    print(f"{recinto:.<40} {dados['aparelhos']:>7,d} aparelhos ({percentual:>5.2f}%) = R$ {dados['valor']:>14,.2f}")

print(f"\n{'TOTAL':.<40} {total_aparelhos:>7,d} aparelhos ({100:>5.2f}%) = R$ {valor_total_validado:>14,.2f}\n")
