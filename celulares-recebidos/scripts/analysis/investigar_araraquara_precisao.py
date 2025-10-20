#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import os

# Investigar os PDFs que supostamente são Araraquara
araraquara_pdfs = [
    'ADM 0800100_0734_2025 de 30_09_2025.PDF',
    'ADM 0800100_0735_2025 de 30_09_2025.PDF',
    'ADM 0800100_0736_2025 de 30_09_2025.PDF',
    'ADM 0800100_0738_2025 de 30_09_2025.PDF',
    'ADM 0800100_0739_2025 de 30_09_2025.PDF',
    'ADM 0800100_0740_2025 de 30_09_2025.PDF',
    'ADM 0800100_0741_2025 de 30_09_2025.PDF',
    'ADM 0800100_0742_2025 de 30_09_2025.PDF',
]

print('='*120)
print('BUSCA ESPECÍFICA: "16 - 810900 Regional DMA - Araraquara/SP"')
print('='*120)
print()

for pdf_file in araraquara_pdfs:
    if not os.path.exists(pdf_file):
        continue
    
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    
    # Buscar padrão específico
    encontrou = text.count('16 - 810900 Regional DMA - Araraquara/SP')
    
    # Buscar variações
    tem_araraquara = 'Araraquara' in text
    tem_810900 = '810900' in text
    tem_regional_dma = 'Regional DMA' in text
    
    print(f'{pdf_file}')
    print(f'  "16 - 810900 Regional DMA - Araraquara/SP": {encontrou} ocorrencias')
    print(f'  Tem "Araraquara": {tem_araraquara}')
    print(f'  Tem "810900": {tem_810900}')
    print(f'  Tem "Regional DMA": {tem_regional_dma}')
    
    # Se tem Araraquara, mostrar contexto
    if tem_araraquara:
        linhas_encontradas = []
        for i, line in enumerate(text.split('\n')):
            if 'Araraquara' in line or '810900' in line:
                linhas_encontradas.append(line[:100])
                if len(linhas_encontradas) >= 3:
                    break
        
        if linhas_encontradas:
            print(f'  Contexto encontrado:')
            for linha in linhas_encontradas:
                print(f'    {linha}')
    print()

print()
print('='*120)
print('RESUMO')
print('='*120)
print()
print('Problema identificado:')
print('Os PDFs Araraquara podem estar sendo identificados INCORRETAMENTE.')
print('O script atual está usando APENAS o mapeamento de nome de arquivo.')
print('Mas precisa BUSCAR DENTRO DO PDF pelo padrão "16 - 810900 Regional DMA - Araraquara/SP"')
print()
print('Acao necessaria: Extrair aparelhos SOMENTE da secao Araraquara dentro de cada PDF,')
print('não contar TODO o PDF como Araraquara.')
