#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import os
from collections import defaultdict

def extrair_aparelhos_por_recinto_v2(pdf_file):
    """
    Extrai aparelhos contando os que vêm logo após cada aparição
    do padrão "N - XXXXX Regional DMA - CIDADE/SP"
    """
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    
    linhas = text.split('\n')
    
    # Padrão para detectar recinto
    padrao_recinto = r'^(\d+)\s*-\s*(\d+)\s+Regional DMA\s*-\s*(.+?)/([A-Z]{2})$'
    
    resultado = defaultdict(lambda: {'quantidade': 0, 'aparelhos': []})
    recinto_atual = None
    
    for i, linha in enumerate(linhas):
        # Verificar se é um header de recinto
        match = re.match(padrao_recinto, linha)
        if match:
            codigo = match.group(1)
            unidade = match.group(2)
            cidade = match.group(3).strip()
            estado = match.group(4)
            
            recinto_atual = f'{codigo}-{unidade}-{cidade}'
            continue
        
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
        
        # Se encontra outra estrutura (Unidade:, UA:, outro padrão), e não tem recinto, zera
        if recinto_atual and ('Unidade:' in linha and 'Regional' not in linha):
            if not re.match(padrao_recinto, linha):
                recinto_atual = None
    
    return dict(resultado)

# Processar todos os PDFs
print('='*140)
print('EXTRAÇÃO V2 - CONTANDO APARELHOS APÓS CADA "N - XXXXX Regional DMA - CIDADE/SP"')
print('='*140)
print()

pdf_files = sorted([f for f in os.listdir('.') if f.endswith('.PDF')])

# Dicionário para agregar recintos
recintos_globais = defaultdict(lambda: {
    'quantidade': 0,
    'pdfs': [],
})

for pdf_file in pdf_files:
    recintos_pdf = extrair_aparelhos_por_recinto_v2(pdf_file)
    
    pdf_nome = pdf_file.replace(' de 30_09_2025.PDF', '').replace(' de 30092025.PDF', '')
    
    print(f'{pdf_file}')
    for recinto, info in recintos_pdf.items():
        print(f'  {recinto}: {info["quantidade"]:,} aparelhos')
        
        # Agregar global
        recintos_globais[recinto]['quantidade'] += info['quantidade']
        recintos_globais[recinto]['pdfs'].append(pdf_nome)
    print()

# Resumo final
print('='*140)
print('RESUMO FINAL')
print('='*140)
print()

total_geral = 0
for recinto in sorted(recintos_globais.keys()):
    info = recintos_globais[recinto]
    total_geral += info['quantidade']
    print(f'{recinto}: {info["quantidade"]:,} aparelhos ({len(info["pdfs"])} PDFs)')

print()
print(f'TOTAL GERAL: {total_geral:,} aparelhos')
print(f'Diferença do esperado (32.015): {total_geral - 32015:+d} ({(total_geral-32015)/32015*100:+.2f}%)')
