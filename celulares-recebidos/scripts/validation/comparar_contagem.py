#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re

# Seus dados
seus_dados = {
    'ADM 0800100_0733_2025 de 30_09_2025.PDF': 13,
    'ADM 0800100_0734_2025 de 30_09_2025.PDF': 6879,
    'ADM 0800100_0740_2025 de 30_09_2025.PDF': 9,
    'ADM 0800100_0741_2025 de 30_09_2025.PDF': 19,
    'ADM 0800100_0742_2025 de 30_09_2025.PDF': 225,
    'ADM 0800100_0743_2025 de 30_09_2025.PDF': 912,
    'ADM 0800100_0744_2025 de 30_09_2025.PDF': 3457,
    'ADM 0800100_0735_2025 de 30_09_2025.PDF': 3804,
    'ADM 0800100_0736_2025 de 30_09_2025.PDF': 1873,
    'ADM 0800100_0737_2025 de 30_09_2025.PDF': 616,
    'ADM 0800100_0738_2025 de 30_09_2025.PDF': 442,
    'ADM 0800100_0739_2025 de 30_09_2025.PDF': 3708,
    'ADM 0800100_0745_2025 de 30_09_2025.PDF': 3390,
    'ADM 0800100_0746_2025 de 30_09_2025.PDF': 2544,
    'ADM 0800100_0747_2025 de 30092025.PDF': 4124,
}

print('='*120)
print('COMPARAÇÃO: Sua contagem vs Contagem do script')
print('='*120)
print()

total_seu = 0
total_script = 0
diferenca_total = 0
diferenças_encontradas = []

for pdf_file, seu_total in sorted(seus_dados.items()):
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        # Contar aparelhos
        script_total = 0
        for line in text.split('\n'):
            if re.match(r'^(\d+,\d+)\s+un\s+', line):
                qty_match = re.match(r'^(\d+,\d+)\s+un', line)
                if qty_match:
                    qty_str = qty_match.group(1).replace(',', '.')
                    qty = int(float(qty_str))
                    script_total += qty
        
        diferenca = script_total - seu_total
        total_seu += seu_total
        total_script += script_total
        diferenca_total += diferenca
        
        if diferenca != 0:
            diferenças_encontradas.append({
                'pdf': pdf_file,
                'seu': seu_total,
                'script': script_total,
                'diff': diferenca
            })
        
        status = 'OK' if diferenca == 0 else f'DIFERENCA {diferenca:+d}'
        print(f'{pdf_file:<50} Seu: {seu_total:>6,} | Script: {script_total:>6,} | {status}')
    except Exception as e:
        print(f'{pdf_file:<50} ERRO: {e}')

print()
print('='*120)
print(f'TOTAL: Você contou {total_seu:,} | Script contou {total_script:,} | Diferença: {diferenca_total:+d}')
print('='*120)

if diferenças_encontradas:
    print()
    print('PDFs com diferenças:')
    for item in diferenças_encontradas:
        print(f"  {item['pdf']}: Você={item['seu']:,} vs Script={item['script']:,} (Diff: {item['diff']:+d})")
    
    print()
    print('Verificando PDFs com diferenças...')
    for item in diferenças_encontradas:
        pdf_file = item['pdf']
        print()
        print(f'Analisando {pdf_file}')
        print(f'  Seu total: {item["seu"]}')
        print(f'  Script: {item["script"]}')
        print(f'  Diferença: {item["diff"]}')
        
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        # Mostrar primeiras e últimas linhas de aparelhos
        linhas_aparelhos = []
        for line in text.split('\n'):
            if re.match(r'^(\d+,\d+)\s+un\s+', line):
                qty_match = re.match(r'^(\d+,\d+)\s+un', line)
                if qty_match:
                    qty_str = qty_match.group(1).replace(',', '.')
                    qtd = int(float(qty_str))
                    linhas_aparelhos.append((qtd, line[:80]))
        
        print(f'  Total de linhas de aparelho: {len(linhas_aparelhos)}')
        if len(linhas_aparelhos) > 0:
            print(f'  Primeiros 3:')
            for qtd, linha in linhas_aparelhos[:3]:
                print(f'    {qtd} un {linha[15:]}')
