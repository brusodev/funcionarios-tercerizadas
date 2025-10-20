import PyPDF2
import re
import json
from pathlib import Path

# Valores de referência (verificação manual do usuário)
valores_referencia = {
    'ADM 0800100_0733_2025 de 30_09_2025.PDF': {'aparelhos': 13, 'valor': 7879.62},
    'ADM 0800100_0734_2025 de 30_09_2025.PDF': {'aparelhos': 6879, 'valor': 5716622.03},
    'ADM 0800100_0740_2025 de 30_09_2025.PDF': {'aparelhos': 9, 'valor': 3950.54},
    'ADM 0800100_0741_2025 de 30_09_2025.PDF': {'aparelhos': 19, 'valor': 18816.20},
    'ADM 0800100_0742_2025 de 30_09_2025.PDF': {'aparelhos': 225, 'valor': 84426.55},
    'ADM 0800100_0743_2025 de 30_09_2025.PDF': {'aparelhos': 912, 'valor': 974075.30},
    'ADM 0800100_0744_2025 de 30_09_2025.PDF': {'aparelhos': 3457, 'valor': 3461458.49},
    'ADM 0800100_0735_2025 de 30_09_2025.PDF': {'aparelhos': 3804, 'valor': 2839605.26},
    'ADM 0800100_0736_2025 de 30_09_2025.PDF': {'aparelhos': 1873, 'valor': 1960163.54},
    'ADM 0800100_0737_2025 de 30_09_2025.PDF': {'aparelhos': 616, 'valor': 280644.01},
    'ADM 0800100_0738_2025 de 30_09_2025.PDF': {'aparelhos': 442, 'valor': 485270.26},
    'ADM 0800100_0739_2025 de 30_09_2025.PDF': {'aparelhos': 3708, 'valor': 1870406.44},
    'ADM 0800100_0745_2025 de 30_09_2025.PDF': {'aparelhos': 3390, 'valor': 4644268.78},
    'ADM 0800100_0746_2025 de 30_09_2025.PDF': {'aparelhos': 2544, 'valor': 3050180.53},
    'ADM 0800100_0747_2025 de 30092025.PDF': {'aparelhos': 4124, 'valor': 3466230.15}
}

def processar_pdf(pdf_path):
    """Extrai todos os aparelhos (SMARTPHONE + TELEFONE CELULAR + APARELHO) de um PDF"""
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        texto_completo = ""
        
        for page in pdf_reader.pages:
            texto_completo += page.extract_text() + "\n"
    
    linhas = texto_completo.split('\n')
    
    # PADRÃO EXPANDIDO: SMARTPHONE, TELEFONE CELULAR, APARELHO
    pattern = r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO)\s+(.+)'
    
    items = []
    
    for i, linha in enumerate(linhas):
        match = re.match(pattern, linha.strip(), re.IGNORECASE)
        
        if match:
            quantidade_str = match.group(1)
            tipo = match.group(2)
            descricao = match.group(3).strip()
            
            # Acumular descrição de linhas seguintes
            partes_descricao = [descricao]
            
            for j in range(i+1, min(i+10, len(linhas))):
                proxima_linha = linhas[j].strip()
                
                if re.match(r'^\d+,\d+\s+un\s+', proxima_linha, re.IGNORECASE):
                    break
                if 'Subtotal:' in proxima_linha or 'Total' in proxima_linha:
                    break
                    
                if proxima_linha:
                    partes_descricao.append(proxima_linha)
                    
                    if 'R$' in proxima_linha:
                        break
            
            descricao_completa = ' '.join(partes_descricao)
            
            # Extrair valor
            valor_match = re.search(r'R\$\s*([\d.]+,\d{2})', descricao_completa)
            
            if valor_match:
                quantidade = float(quantidade_str.replace(',', '.'))
                valor_str = valor_match.group(1)
                
                descricao_limpa = re.sub(r'///.*$', '', descricao_completa).strip()
                descricao_formatada = f"{tipo} {descricao_limpa}"
                
                items.append({
                    'unidade': quantidade,
                    'modelo': descricao_formatada,
                    'valor': f'R$ {valor_str}'
                })
    
    return items

# Processar todos os PDFs
resultados = []
total_geral_aparelhos = 0
total_geral_valor = 0.0

print("=" * 100)
print("PROCESSAMENTO COMPLETO - TODOS OS 15 PDFs")
print("PADRÃO EXPANDIDO: SMARTPHONE + TELEFONE CELULAR + APARELHO")
print("=" * 100)
print()

for pdf_nome, ref in valores_referencia.items():
    pdf_path = Path(pdf_nome)
    
    if not pdf_path.exists():
        print(f"❌ ERRO: {pdf_nome} não encontrado")
        continue
    
    print(f"Processando: {pdf_nome}...")
    
    items = processar_pdf(pdf_path)
    
    # Calcular totais
    total_unidades = sum(item['unidade'] for item in items)
    
    total_valor = 0
    for item in items:
        valor_str = item['valor'].replace('R$', '').strip()
        valor_str = valor_str.replace('.', '').replace(',', '.')
        total_valor += float(valor_str)
    
    # Comparar com referência
    dif_aparelhos = int(total_unidades) - ref['aparelhos']
    dif_valor = total_valor - ref['valor']
    
    # Calcular percentual de diferença
    perc_aparelhos = (abs(dif_aparelhos) / ref['aparelhos'] * 100) if ref['aparelhos'] > 0 else 0
    perc_valor = (abs(dif_valor) / ref['valor'] * 100) if ref['valor'] > 0 else 0
    
    # Status
    status_aparelhos = "✓" if abs(dif_aparelhos) <= 1 else "⚠" if perc_aparelhos < 1 else "❌"
    status_valor = "✓" if abs(dif_valor) < 1 else "⚠" if perc_valor < 0.1 else "❌"
    
    resultado = {
        'pdf': pdf_nome,
        'itens_extraidos': len(items),
        'aparelhos_calculados': int(total_unidades),
        'aparelhos_esperados': ref['aparelhos'],
        'diferenca_aparelhos': dif_aparelhos,
        'valor_calculado': total_valor,
        'valor_esperado': ref['valor'],
        'diferenca_valor': dif_valor,
        'percentual_erro_aparelhos': perc_aparelhos,
        'percentual_erro_valor': perc_valor,
        'status_aparelhos': status_aparelhos,
        'status_valor': status_valor
    }
    
    resultados.append(resultado)
    total_geral_aparelhos += int(total_unidades)
    total_geral_valor += total_valor
    
    # Mostrar resultado
    print(f"  Aparelhos: {int(total_unidades):,} (esperado: {ref['aparelhos']:,}) {status_aparelhos}")
    print(f"  Valor: R$ {total_valor:,.2f} (esperado: R$ {ref['valor']:,.2f}) {status_valor}".replace(',', '_').replace('.', ',').replace('_', '.'))
    if abs(dif_aparelhos) > 0 or abs(dif_valor) >= 1:
        print(f"  ⚠ Dif. Aparelhos: {dif_aparelhos:+} ({perc_aparelhos:.2f}%)")
        print(f"  ⚠ Dif. Valor: R$ {dif_valor:+,.2f} ({perc_valor:.3f}%)".replace(',', '_').replace('.', ',').replace('_', '.'))
    print()

# Resumo final
print("=" * 100)
print("RESUMO FINAL")
print("=" * 100)
print()
print(f"Total Geral Calculado:")
print(f"  Aparelhos: {total_geral_aparelhos:,}")
print(f"  Valor: R$ {total_geral_valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
print()
print(f"Total Geral Esperado:")
print(f"  Aparelhos: 32.015")
print(f"  Valor: R$ 28.863.997,70")
print()

dif_final_aparelhos = total_geral_aparelhos - 32015
dif_final_valor = total_geral_valor - 28863997.70

print(f"Diferença:")
print(f"  Aparelhos: {dif_final_aparelhos:+,}")
print(f"  Valor: R$ {dif_final_valor:+,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
print()

# Análise de acurácia
pdfs_perfeitos_aparelhos = sum(1 for r in resultados if r['status_aparelhos'] == '✓')
pdfs_perfeitos_valor = sum(1 for r in resultados if r['status_valor'] == '✓')

print(f"Acurácia:")
print(f"  PDFs com aparelhos corretos: {pdfs_perfeitos_aparelhos}/15 ({pdfs_perfeitos_aparelhos/15*100:.1f}%)")
print(f"  PDFs com valores corretos: {pdfs_perfeitos_valor}/15 ({pdfs_perfeitos_valor/15*100:.1f}%)")
print()

# Salvar relatório detalhado
with open('relatorio_validacao_completo.json', 'w', encoding='utf-8') as f:
    json.dump({
        'resultados_por_pdf': resultados,
        'totais': {
            'calculado': {
                'aparelhos': total_geral_aparelhos,
                'valor': total_geral_valor
            },
            'esperado': {
                'aparelhos': 32015,
                'valor': 28863997.70
            },
            'diferenca': {
                'aparelhos': dif_final_aparelhos,
                'valor': dif_final_valor
            }
        },
        'acuracia': {
            'pdfs_perfeitos_aparelhos': pdfs_perfeitos_aparelhos,
            'pdfs_perfeitos_valor': pdfs_perfeitos_valor,
            'percentual_aparelhos': pdfs_perfeitos_aparelhos/15*100,
            'percentual_valor': pdfs_perfeitos_valor/15*100
        }
    }, f, ensure_ascii=False, indent=2)

print("Relatório salvo: relatorio_validacao_completo.json")
print("=" * 100)
