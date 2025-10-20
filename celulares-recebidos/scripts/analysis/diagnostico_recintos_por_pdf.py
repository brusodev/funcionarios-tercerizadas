#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import os

def encontrar_recintos_no_pdf(pdf_file):
    """Encontra todos os recintos dentro de um PDF"""
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    
    padrao_recinto = r'(\d+)\s*-\s*(\d+)\s+Regional DMA\s*-\s*(.+?)/([A-Z]{2})'
    matches = re.finditer(padrao_recinto, text)
    
    recintos_unicos = set()
    for match in matches:
        chave = f'{match.group(1)}-{match.group(2)}-{match.group(3).strip()}'
        recintos_unicos.add(chave)
    
    return sorted(recintos_unicos)

print('='*120)
print('ANÁLISE: QUAIS RECINTOS EXISTEM DENTRO DE CADA PDF?')
print('='*120)
print()

pdf_files = sorted([f for f in os.listdir('.') if f.endswith('.PDF')])

for pdf_file in pdf_files:
    recintos = encontrar_recintos_no_pdf(pdf_file)
    
    if recintos:
        print(f'{pdf_file}')
        for recinto in recintos:
            print(f'  ✓ {recinto}')
    else:
        print(f'{pdf_file}')
        print(f'  ✗ Nenhum recinto encontrado')
    print()

print()
print('='*120)
print('CONCLUSÃO')
print('='*120)
print("""
A contagem de Araraquara está POSSIVELMENTE INCORRETA porque:

1. O PDF 0739 contém TANTO Araraquara QUANTO Bauru
2. O mapeamento atual atribui TODO o PDF para um recinto
3. Precisamos extrair APENAS os aparelhos da seção Araraquara/810900

Solução necessária: Extrair aparelhos POR SEÇÃO DE RECINTO dentro de cada PDF,
não contar todo o PDF para um único recinto.
""")
