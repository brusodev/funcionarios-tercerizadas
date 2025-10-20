#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import os
import json
from collections import defaultdict

def extrair_aparelhos_por_recinto(pdf_file):
    """
    Extrai aparelhos separando por recinto (16-810900-Araraquara vs 305-810300-Bauru)
    Cada seção começa com o padrão "N - XXXXX Regional DMA - CIDADE/SP"
    """
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    
    linhas = text.split('\n')
    
    # Padrão para detectar início de seção de recinto
    padrao_recinto_header = r'^(\d+)\s*-\s*(\d+)\s+Regional DMA\s*-\s*(.+?)/([A-Z]{2})$'
    
    resultado = {}
    recinto_atual = None
    recinto_info = None
    aparelhos_atuais = []
    
    for linha in linhas:
        # Verificar se é um header de recinto
        match = re.match(padrao_recinto_header, linha)
        if match:
            # Salvar aparelhos do recinto anterior
            if recinto_atual and aparelhos_atuais:
                total_qty = sum(ap['qtd'] for ap in aparelhos_atuais)
                resultado[recinto_atual] = {
                    'descricao': recinto_info,
                    'quantidade': total_qty,
                    'aparelhos': aparelhos_atuais
                }
            
            # Iniciar novo recinto
            codigo = match.group(1)
            unidade = match.group(2)
            cidade = match.group(3).strip()
            estado = match.group(4)
            
            recinto_atual = f'{codigo}-{unidade}-{cidade}'
            recinto_info = f'{codigo} - {unidade} Regional DMA - {cidade}/{estado}'
            aparelhos_atuais = []
        
        # Se estamos em um recinto e a linha é de aparelho
        elif recinto_atual and re.match(r'^(\d+,\d+)\s+un\s+', linha):
            qty_match = re.match(r'^(\d+,\d+)\s+un', linha)
            if qty_match:
                qty_str = qty_match.group(1).replace(',', '.')
                qtd = int(float(qty_str))
                aparelhos_atuais.append({
                    'qtd': qtd,
                    'descricao': linha[15:]
                })
    
    # Salvar último recinto
    if recinto_atual and aparelhos_atuais:
        total_qty = sum(ap['qtd'] for ap in aparelhos_atuais)
        resultado[recinto_atual] = {
            'descricao': recinto_info,
            'quantidade': total_qty,
            'aparelhos': aparelhos_atuais
        }
    
    # Se nenhum recinto foi encontrado, contar tudo como genérico
    if not resultado:
        total_qty = 0
        for linha in linhas:
            if re.match(r'^(\d+,\d+)\s+un\s+', linha):
                qty_match = re.match(r'^(\d+,\d+)\s+un', linha)
                if qty_match:
                    qty_str = qty_match.group(1).replace(',', '.')
                    qtd = int(float(qty_str))
                    total_qty += qtd
        
        if total_qty > 0:
            resultado['DESCONHECIDO'] = {
                'descricao': 'Recinto não identificado',
                'quantidade': total_qty,
                'aparelhos': []
            }
    
    return resultado

# Processar todos os PDFs
print('='*140)
print('EXTRAÇÃO CORRETA - POR RECINTO DENTRO DE CADA PDF')
print('='*140)
print()

pdf_files = sorted([f for f in os.listdir('.') if f.endswith('.PDF')])

# Dicionário para agregar recintos
recintos_globais = defaultdict(lambda: {
    'quantidade': 0,
    'pdfs': [],
    'descricao': ''
})

for pdf_file in pdf_files:
    recintos_pdf = extrair_aparelhos_por_recinto(pdf_file)
    
    pdf_nome = pdf_file.replace(' de 30_09_2025.PDF', '').replace(' de 30092025.PDF', '')
    
    print(f'{pdf_file}')
    for recinto, info in recintos_pdf.items():
        print(f'  {recinto}: {info["quantidade"]:,} aparelhos')
        
        # Agregar global
        recintos_globais[recinto]['quantidade'] += info['quantidade']
        recintos_globais[recinto]['pdfs'].append(pdf_nome)
        recintos_globais[recinto]['descricao'] = info['descricao']
    print()

# Resumo final
print('='*140)
print('RESUMO FINAL - CONTAGEM CORRETA POR RECINTO')
print('='*140)
print()

total_geral = 0
for recinto in sorted(recintos_globais.keys()):
    info = recintos_globais[recinto]
    total_geral += info['quantidade']
    print(f'{recinto}')
    print(f'  Descrição: {info["descricao"]}')
    print(f'  Aparelhos: {info["quantidade"]:,}')
    print(f'  PDFs: {len(info["pdfs"])}')
    print()

print(f'TOTAL GERAL: {total_geral:,} aparelhos')
print()
print(f'Diferença do esperado (32.015): {total_geral - 32015:+d}')
