#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re

pdf_path = r'c:\Users\bruno.vargas\Desktop\PROJETOS\celulares-recebidos\ADM 0800100_0739_2025 de 30_09_2025.PDF'

with open(pdf_path, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''

lines = text.split('\n')

# Test patterns on the actual PDF lines
pattern1 = r'(\d{7})\s*-\s*([A-ZÁ-Ú\s/]+?)\s+Unidade:'
pattern2 = r'(\d+)\s*-\s*(\d{6})\s+Regional\s+DMA\s*-\s*([A-ZÁ-Ú\s/]+)/[A-Z]{2}'

print("=" * 80)
print("TESTE DE PATTERNS")
print("=" * 80)
print()

unidades_encontradas = []
recintos_encontrados = []

for i, line in enumerate(lines):
    # Check pattern 1
    if re.match(pattern1, line):
        match = re.match(pattern1, line)
        unidade = f"{match.group(1)} - {match.group(2).strip()}"
        unidades_encontradas.append((i, unidade))
        print(f"UNIDADE encontrada na linha {i}: {unidade}")
    
    # Check pattern 2
    if re.match(pattern2, line):
        match = re.match(pattern2, line)
        recinto = f"{match.group(2)} - {match.group(3).strip()}"
        recintos_encontrados.append((i, recinto))
        print(f"RECINTO encontrado na linha {i}: {recinto}")
        print(f"  Linha completa: {line}")

print()
print(f"Total de UNIDADES encontradas: {len(unidades_encontradas)}")
print(f"Total de RECINTOS encontrados: {len(recintos_encontrados)}")

print()
print("=" * 80)
print("Buscando especificamente por '16 - 810900 Regional DMA'")
print("=" * 80)
print()

for i, line in enumerate(lines):
    if '810900' in line and 'Regional DMA' in line and 'Araraquara' in line:
        print(f"Linha {i}: {line}")
        print(f"  Teste pattern2: {bool(re.match(pattern2, line))}")
        
        # Try a simpler pattern
        simple_pattern = r'16\s*-\s*810900\s+Regional\s+DMA.*Araraquara'
        print(f"  Teste simple_pattern: {bool(re.search(simple_pattern, line))}")
