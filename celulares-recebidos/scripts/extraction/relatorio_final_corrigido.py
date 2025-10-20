#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import os
import json
from collections import defaultdict

def extrair_aparelhos_por_recinto_completo(pdf_file):
    """
    Extrai aparelhos separando pelos 5 recintos reais e também extrai o valor total do ADM
    """
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    
    linhas = text.split('\n')
    
    # Padrões para detectar cada recinto
    padroes_recinto = {
        'Bauru': r'305\s*-\s*810300\s+Regional DMA\s*-\s*Bauru/SP',
        'Araraquara': r'16\s*-\s*810900\s+Regional DMA\s*-\s*Araraquara/SP',
        'São José do Rio Preto': r'2\s*-\s*DEPÓSITO SAPOL/DRF/SJR',
        'Viracopos': r'1\s*-\s*AEROPORTOS BRASIL VIRACOPOS\s*-\s*ABV',
        'Ipiranga': r'309\s*-\s*817900\s+Regional DMA IPIRANGA',
    }
    
    resultado = defaultdict(lambda: {'quantidade': 0})
    recinto_atual = None
    
    for i, linha in enumerate(linhas):
        # Verificar se esta linha contém algum marcador de recinto
        for nome_recinto, padrao in padroes_recinto.items():
            if re.search(padrao, linha):
                recinto_atual = nome_recinto
                break
        
        # Se temos um recinto ativo e esta é uma linha de aparelho
        if recinto_atual and re.match(r'^(\d+,\d+)\s+un\s+', linha):
            qty_match = re.match(r'^(\d+,\d+)\s+un', linha)
            if qty_match:
                qty_str = qty_match.group(1).replace(',', '.')
                qtd = int(float(qty_str))
                resultado[recinto_atual]['quantidade'] += qtd
    
    # Extrair Total do ADM
    adm_match = re.search(r'Total\s+do\s+ADM\s*:\s*R\$\s*([\d.]+,\d+)', text)
    total_adm = 0
    if adm_match:
        valor_str = adm_match.group(1).replace('.', '').replace(',', '.')
        total_adm = float(valor_str)
    
    return dict(resultado), total_adm

# Processar todos os PDFs
print('Processando todos os PDFs para gerar relatório final corrigido...\n')

pdf_files = sorted([f for f in os.listdir('.') if f.endswith('.PDF')])

# Dicionários para agregar
recintos_globais = defaultdict(lambda: {
    'quantidade': 0,
    'valor_total': 0.0,
    'pdfs': [],
    'pdf_detalhes': {}
})

for pdf_file in pdf_files:
    recintos_pdf, valor_adm = extrair_aparelhos_por_recinto_completo(pdf_file)
    pdf_nome = pdf_file.replace(' de 30_09_2025.PDF', '').replace(' de 30092025.PDF', '')
    
    # Distribuir o valor total do ADM proporcionalmente entre os recintos encontrados
    total_aparelhos_pdf = sum(r['quantidade'] for r in recintos_pdf.values())
    
    if total_aparelhos_pdf > 0:
        for recinto, info in recintos_pdf.items():
            proporcao = info['quantidade'] / total_aparelhos_pdf
            valor_recinto = valor_adm * proporcao
            
            recintos_globais[recinto]['quantidade'] += info['quantidade']
            recintos_globais[recinto]['valor_total'] += valor_recinto
            recintos_globais[recinto]['pdfs'].append(pdf_nome)
            recintos_globais[recinto]['pdf_detalhes'][pdf_nome] = {
                'quantidade': info['quantidade'],
                'valor': valor_recinto
            }

# Preparar dados para salvar em JSON
descricoes = {
    'Araraquara': 'Regional DMA - Araraquara/SP',
    'Bauru': 'Regional DMA - Bauru/SP',
    'São José do Rio Preto': 'DEPÓSITO SAPOL/DRF/SJR',
    'Viracopos': 'AEROPORTOS BRASIL VIRACOPOS - ABV',
    'Ipiranga': 'Regional DMA IPIRANGA'
}

output_data = {}
for recinto in ['Araraquara', 'Bauru', 'São José do Rio Preto', 'Viracopos', 'Ipiranga']:
    if recinto in recintos_globais:
        info = recintos_globais[recinto]
        output_data[recinto] = {
            'descricao': descricoes[recinto],
            'quantidade': info['quantidade'],
            'valor_total': round(info['valor_total'], 2),
            'num_pdfs': len(info['pdfs']),
            'pdfs': sorted(info['pdfs'])
        }

# Salvar JSON
folder_path = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_CORRIGIDO.json')
os.makedirs(os.path.dirname(json_path), exist_ok=True)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

# Salvar CSV
csv_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_CORRIGIDO.csv')
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write('Recinto;Descrição;Quantidade;Valor Total;Número de PDFs;PDFs\n')
    for recinto in ['Araraquara', 'Bauru', 'São José do Rio Preto', 'Viracopos', 'Ipiranga']:
        if recinto in output_data:
            data = output_data[recinto]
            valor_fmt = str(data['valor_total']).replace('.', ',')
            pdfs_str = '|'.join(data['pdfs'])
            f.write(f'{recinto};{data["descricao"]};{data["quantidade"]};{valor_fmt};{data["num_pdfs"]};{pdfs_str}\n')

# Imprimir resumo
print('='*120)
print('RELATÓRIO FINAL CORRIGIDO - CONTAGEM REAL POR RECINTO')
print('='*120)
print()

print(f"{'Recinto':<30} {'Aparelhos':>15} {'Valor Total':>20} {'PDFs':>8}")
print('-'*120)

total_geral = 0
valor_total_geral = 0.0

for recinto in ['Araraquara', 'Bauru', 'São José do Rio Preto', 'Viracopos', 'Ipiranga']:
    if recinto in output_data:
        data = output_data[recinto]
        total_geral += data['quantidade']
        valor_total_geral += data['valor_total']
        print(f"{recinto:<30} {data['quantidade']:>15,} R$ {data['valor_total']:>18,.2f} {data['num_pdfs']:>8}")

print('-'*120)
print(f"{'TOTAL':<30} {total_geral:>15,} R$ {valor_total_geral:>18,.2f}")

print()
print(f'Diferença do esperado: {total_geral - 32015:+d} aparelhos ({(total_geral-32015)/32015*100:+.2f}%)')
print()
print(f'✅ JSON salvo: {json_path}')
print(f'✅ CSV salvo: {csv_path}')
