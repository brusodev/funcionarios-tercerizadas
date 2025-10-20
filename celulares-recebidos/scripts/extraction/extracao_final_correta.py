#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import os
from collections import defaultdict

def extrair_aparelhos_por_recinto_correto(pdf_file):
    """
    Extrai aparelhos separando pelos 5 recintos reais:
    - 305 - 810300 Regional DMA - Bauru/SP
    - 16 - 810900 Regional DMA - Araraquara/SP
    - 2 - DEPÓSITO SAPOL/DRF/SJR
    - 1 - AEROPORTOS BRASIL VIRACOPOS - ABV
    - 309 - 817900 Regional DMA IPIRANGA
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
    
    resultado = defaultdict(lambda: {'quantidade': 0, 'aparelhos': []})
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
                resultado[recinto_atual]['aparelhos'].append({
                    'qtd': qtd,
                    'descricao': linha[15:]
                })
    
    # Extrair Total do ADM para validação
    adm_match = re.search(r'Total\s+do\s+ADM\s*:\s*R\$\s*([\d.]+,\d+)', text)
    if adm_match:
        valor_str = adm_match.group(1).replace('.', '').replace(',', '.')
        total_adm = float(valor_str)
    else:
        total_adm = 0
    
    return dict(resultado), total_adm

# Processar todos os PDFs
print('='*150)
print('EXTRAÇÃO CORRETA - SEPARANDO PELOS 5 RECINTOS REAIS')
print('='*150)
print()

pdf_files = sorted([f for f in os.listdir('.') if f.endswith('.PDF')])

# Dicionário para agregar recintos
recintos_globais = defaultdict(lambda: {
    'quantidade': 0,
    'valor_total': 0.0,
    'pdfs': [],
})

for pdf_file in pdf_files:
    recintos_pdf, valor_adm = extrair_aparelhos_por_recinto_correto(pdf_file)
    
    pdf_nome = pdf_file.replace(' de 30_09_2025.PDF', '').replace(' de 30092025.PDF', '')
    
    print(f'{pdf_file}')
    
    total_pdf = 0
    for recinto in ['Araraquara', 'Bauru', 'São José do Rio Preto', 'Viracopos', 'Ipiranga']:
        if recinto in recintos_pdf:
            qty = recintos_pdf[recinto]['quantidade']
            total_pdf += qty
            print(f'  {recinto}: {qty:,} aparelhos')
            
            # Agregar global
            recintos_globais[recinto]['quantidade'] += qty
            recintos_globais[recinto]['pdfs'].append(pdf_nome)
    
    if total_pdf == 0:
        print(f'  [Nenhum recinto identificado - {len(recintos_pdf)} recintos encontrados]')
    
    print(f'  Total PDF: {total_pdf:,} | Total do ADM: R$ {valor_adm:,.2f}')
    print()

# Resumo final
print('='*150)
print('RESUMO FINAL - CONTAGEM CORRETA POR RECINTO')
print('='*150)
print()

print(f"{'Recinto':<30} {'Aparelhos':>15} {'PDFs':>8}")
print('-'*150)

total_geral = 0
valor_total_geral = 0.0

for recinto in ['Araraquara', 'Bauru', 'São José do Rio Preto', 'Viracopos', 'Ipiranga']:
    if recinto in recintos_globais:
        info = recintos_globais[recinto]
        total_geral += info['quantidade']
        print(f"{recinto:<30} {info['quantidade']:>15,} {len(info['pdfs']):>8}")

print('-'*150)
print(f"{'TOTAL':<30} {total_geral:>15,}")
print()
print(f'Diferença do esperado (32.015): {total_geral - 32015:+d} ({(total_geral-32015)/32015*100:+.2f}%)')
