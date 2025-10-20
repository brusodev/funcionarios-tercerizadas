#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import os

def extract_aparelhos_por_recinto(pdf_file):
    """
    Extrai aparelhos agrupados por recinto, procurando especificamente
    pelo padrão "N - XXXXXX Regional DMA - CIDADE/SP"
    """
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    
    linhas = text.split('\n')
    
    # Padrão para encontrar recintos: "N - XXXXXX Regional DMA - CIDADE/SP"
    padrao_recinto = r'(\d+)\s*-\s*(\d+)\s+Regional DMA\s*-\s*(.+?)/([A-Z]{2})'
    
    recintos_encontrados = {}
    
    # Primeiro, encontrar todos os recintos
    for i, linha in enumerate(linhas):
        match = re.search(padrao_recinto, linha)
        if match:
            codigo_recinto = match.group(1)
            numero_unidade = match.group(2)
            cidade = match.group(3).strip()
            estado = match.group(4)
            
            chave_recinto = f'{codigo_recinto} - {numero_unidade} - {cidade}/{estado}'
            
            if chave_recinto not in recintos_encontrados:
                recintos_encontrados[chave_recinto] = {
                    'linhas_inicio': i,
                    'aparelhos': [],
                    'quantidade': 0,
                    'descricao': f'{codigo_recinto} - {numero_unidade} Regional DMA - {cidade}/{estado}'
                }
    
    # Agora extrair aparelhos de cada seção
    recintos_com_aparelhos = {}
    recinto_atual = None
    
    for i, linha in enumerate(linhas):
        # Verificar se esta é uma linha de recinto
        match = re.search(padrao_recinto, linha)
        if match:
            chave_recinto = f'{match.group(1)} - {match.group(2)} - {match.group(3).strip()}/{match.group(4)}'
            recinto_atual = chave_recinto
            if recinto_atual not in recintos_com_aparelhos:
                recintos_com_aparelhos[recinto_atual] = []
        
        # Se estamos em um recinto e esta é uma linha de aparelho
        if recinto_atual and re.match(r'^(\d+,\d+)\s+un\s+', linha):
            qty_match = re.match(r'^(\d+,\d+)\s+un', linha)
            if qty_match:
                qty_str = qty_match.group(1).replace(',', '.')
                qty = int(float(qty_str))
                recintos_com_aparelhos[recinto_atual].append({
                    'quantidade': qty,
                    'descricao': linha[15:80]
                })
    
    return recintos_com_aparelhos

# Testar com PDF 0738 que tem múltiplos recintos
pdf_file = 'ADM 0800100_0738_2025 de 30_09_2025.PDF'

print('='*140)
print(f'ANÁLISE PROFUNDA: {pdf_file}')
print('='*140)
print()

recintos = extract_aparelhos_por_recinto(pdf_file)

for recinto, aparelhos in recintos.items():
    total_qty = sum(a['quantidade'] for a in aparelhos)
    print(f'Recinto: {recinto}')
    print(f'Total de aparelhos: {total_qty:,}')
    print(f'Linhas de aparelhos: {len(aparelhos)}')
    if len(aparelhos) > 0:
        print(f'Primeiros 5:')
        for ap in aparelhos[:5]:
            print(f'  {ap["quantidade"]} un - {ap["descricao"]}')
    print()

# Agora contar total para este PDF
print('='*140)
print('RESUMO PARA ESTE PDF')
print('='*140)
total_geral = 0
for recinto, aparelhos in recintos.items():
    total_qty = sum(a['quantidade'] for a in aparelhos)
    total_geral += total_qty
    print(f'{recinto}: {total_qty:,} aparelhos')

print(f'\nTotal geral (somando todos os recintos): {total_geral:,}')

# Extrair Total do ADM para comparação
with open(pdf_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

adm_match = re.search(r'Total\s+do\s+ADM\s*:\s*R\$\s*([\d.]+,\d+)', text)
if adm_match:
    valor_str = adm_match.group(1).replace('.', '').replace(',', '.')
    total_adm = float(valor_str)
    print(f'Total do ADM informado no PDF: R$ {total_adm:,.2f}')
